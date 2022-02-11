from sqlalchemy.orm import (
    Query,
    joinedload,
)

from .. import tables
from ..services.generic import GenericCRUDService


class ShowsService(GenericCRUDService):
    model = tables.Show
    lookup_field = "show_id"
    order_by = tables.Show.title.asc()

    def get_default_query(self) -> Query:
        return (
            self.session.query(tables.Show).options(
                joinedload(tables.Show.cast),
                joinedload(tables.Show.director),
                joinedload(tables.Show.country),
                joinedload(tables.Show.listed_in),
                joinedload(tables.Show.rating),
            )
        )

    def get_list_query(self,
                       *,
                       search: str = None,
                       show_type: str = None,
                       rating: str = None,
                       duration_min: int = None,
                       duration_max: int = None,
                       release_year: int = None,
                       genres: list[str] = None,
                       countries: list[str] = None,
                       ) -> Query:
        query = self.get_default_query()
        if search:
            query = self.add_search(query, search)

        if show_type is not None:
            query = query.filter(tables.Show.type == show_type)

        if rating is not None:
            query = query.filter(tables.Show.rating.has(code=rating))

        if duration_min is not None:
            query = query.filter(tables.Show.duration >= duration_min)

        if duration_max is not None:
            query = query.filter(tables.Show.duration <= duration_max)

        if release_year is not None:
            query = query.filter(tables.Show.release_year == release_year)

        if genres:
            query = query.filter(tables.Show.listed_in.any(tables.Genre.name.in_(genres)))

        if countries:
            query = query.filter(tables.Show.country.any(tables.Country.name.in_(countries)))
        return query

    @staticmethod
    def add_search(query: Query, search_query: str) -> Query:
        matching_string = f"%{search_query}%"
        return (
            query.filter(
                tables.Show.title.ilike(matching_string) |
                tables.Show.description.ilike(matching_string)
            )
        )
