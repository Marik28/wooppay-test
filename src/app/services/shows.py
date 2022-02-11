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
