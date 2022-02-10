from pathlib import Path
from typing import Iterable

import pandas as pd
import sqlalchemy.orm
import typer
from loguru import logger

from app import tables
from app.database import Session

app = typer.Typer()


def to_1D(series: Iterable) -> pd.Series:
    """Creates flat array from all given arrays values"""
    return pd.Series([x for _list in series for x in _list])


def get_unique_values(df: pd.DataFrame) -> list:
    return list(to_1D(df.dropna()).unique())


def split_strings(column: pd.Series, separator: str = ",") -> pd.Series:
    """Splits all strings and casts NaN's to empty lists"""
    return (
        column.fillna("")
            .apply(lambda value: value.strip(separator).split(separator) if value != "" else [])
            .apply(lambda values: [value.strip() for value in values])
    )


def create_shows_to_add(
        df: pd.DataFrame,
        added_objects_info: dict[str, dict[str]],
) -> list[tables.Show]:
    shows_to_add = []
    logger.info("Creating shows list...")
    for _, row in df.iterrows():
        show_id = str(row["show_id"])
        type_ = row["type"]
        title = row["title"]
        description = row["description"]
        date_added = row["date_added"] if not pd.isnull(row["date_added"]) else None
        release_year = row["release_year"]
        rating_code = row["rating"] if not pd.isnull(row["rating"]) else None
        duration = row["duration"]

        rating = added_objects_info["ratings"].get(rating_code)
        director = [added_objects_info["persons"][person] for person in row["director"]]
        cast = [added_objects_info["persons"][actor] for actor in row["cast"]]
        listed_in = [added_objects_info["genres"][genre] for genre in row["listed_in"]]
        country = [added_objects_info["countries"][country_name] for country_name in row["country"]]
        shows_to_add.append(
            tables.Show(
                show_id=show_id,
                type=type_,
                title=title,
                description=description,
                date_added=date_added,
                release_year=release_year,
                rating=rating,
                duration=duration,
                director=director,
                cast=cast,
                listed_in=listed_in,
                country=country,
            )
        )

    return shows_to_add


def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    """Prepares raw csv data for inserting to database"""
    df['cast'] = split_strings(df['cast'])
    df['director'] = split_strings(df['director'])
    df['country'] = split_strings(df['country'])
    df['listed_in'] = split_strings(df['listed_in'])
    df['duration'] = df['duration'].apply(lambda duration: int(duration.split(" ")[0]))
    return df


def add_list(objects_to_add: list, session: sqlalchemy.orm.Session, name: str):
    logger.info(f"Adding {name} ...")
    session.add_all(objects_to_add)
    session.commit()
    logger.info(f"{name} added!")
    return objects_to_add


def insert_data(df: pd.DataFrame, session: sqlalchemy.orm.Session):
    unique_genres = get_unique_values(df["listed_in"])
    unique_persons = []
    unique_persons.extend(get_unique_values(df["director"]))
    unique_persons.extend(get_unique_values(df["cast"]))
    unique_countries = get_unique_values(df["country"])
    unique_ratings = df["rating"].dropna().unique()

    added_ratings = add_list([tables.Rating(code=code) for code in unique_ratings], session, "ratings")
    added_genres = add_list([tables.Genre(name=genre) for genre in unique_genres], session, "genres")
    added_persons = add_list([tables.Person(fullname=person) for person in unique_persons], session, "persons")
    added_countries = add_list([tables.Country(name=country) for country in unique_countries], session, "countries")

    logger.info("creating help dicts ...")
    genres_dict = {genre.name: genre for genre in added_genres}
    rating_dict = {rating.code: rating for rating in added_ratings}
    persons_dict = {person.fullname: person for person in added_persons}
    countries_dict = {country.name: country for country in added_countries}

    added_objects = {
        "genres": genres_dict,
        "ratings": rating_dict,
        "persons": persons_dict,
        "countries": countries_dict,
    }
    add_list(create_shows_to_add(df, added_objects), session, "shows")


@app.command()
def main(
        csv_file: Path = typer.Argument(
            ...,
            resolve_path=True,
            exists=True,
            readable=True,
            help="Csv file with shows data",
        )
):
    """Takes data from csv file and inserts it to database"""
    df = normalize_data(pd.read_csv(csv_file, parse_dates=["date_added"]))
    with Session() as session:
        insert_data(df, session)


if __name__ == '__main__':
    app()
