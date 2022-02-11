from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    Date,
    SmallInteger,
    Text,
    CheckConstraint,
    Table,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .models.shows import ShowType

Base = declarative_base()


def get_enum_values(enum) -> list[str]:
    return [str(e.value) for e in enum]


actors_shows_association_table = Table(
    "actors_shows_association",
    Base.metadata,
    Column("show_id", ForeignKey("shows.show_id")),
    Column("actor_id", ForeignKey("persons.id")),
)

directors_shows_association_table = Table(
    "directors_shows_association",
    Base.metadata,
    Column("show_id", ForeignKey("shows.show_id")),
    Column("director_id", ForeignKey("persons.id")),
)

countries_shows_association_table = Table(
    "countries_shows_association",
    Base.metadata,
    Column("show_id", ForeignKey("shows.show_id")),
    Column("country_id", ForeignKey("countries.id")),
)

genres_shows_association_table = Table(
    "genres_shows_association",
    Base.metadata,
    Column("show_id", ForeignKey("shows.show_id")),
    Column("genre_id", ForeignKey("genres.id")),
)


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    fullname = Column(String(255), nullable=False)

    starred_in = relationship(
        "Show",
        secondary=actors_shows_association_table,
        back_populates="cast",
    )

    directed = relationship(
        "Show",
        secondary=directors_shows_association_table,
        back_populates="director",
    )

    def __str__(self) -> str:
        return self.fullname


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

    def __str__(self) -> str:
        return self.name


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)

    def __str__(self) -> str:
        return self.name


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    code = Column(String(20), nullable=False, unique=True)

    def __str__(self) -> str:
        return self.code


class Show(Base):
    __tablename__ = "shows"

    show_id = Column(String(8), primary_key=True)
    type = Column(
        Enum(ShowType, create_constraint=True, values_callable=get_enum_values),
        nullable=False,
    )
    title = Column(String(255), nullable=False)
    description = Column(Text(), nullable=False)
    date_added = Column(Date(), nullable=True)
    release_year = Column(SmallInteger(), nullable=False)
    rating_id = Column(ForeignKey("ratings.id"), nullable=True)
    duration = Column(SmallInteger(), nullable=False)

    rating = relationship("Rating", backref="shows")
    director = relationship(
        "Person",
        secondary=directors_shows_association_table,
        back_populates="directed",
    )
    cast = relationship(
        "Person",
        secondary=actors_shows_association_table,
        back_populates="starred_in",
    )
    listed_in = relationship(
        "Genre",
        secondary=genres_shows_association_table,
    )
    country = relationship(
        "Country",
        secondary=countries_shows_association_table,
    )

    table_args = (
        CheckConstraint("release_year >= 0", name="positive_release_year_constraint"),
        CheckConstraint("duration >= 0", name="positive_duration_constraint")
    )

    def __str__(self) -> str:
        return f"{self.title} ({self.release_year})"
