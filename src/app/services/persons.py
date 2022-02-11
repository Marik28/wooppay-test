from typing import Optional

from sqlalchemy.orm import (
    Query,
    joinedload,
)

from .generic import GenericCRUDService
from .. import tables


class PersonsService(GenericCRUDService):
    model = tables.Person
    order_by = tables.Person.fullname.asc()

    def get_list_query(self, *, search: Optional[str] = None) -> Query:
        query = self.get_default_query()
        if search:
            query = query.filter(tables.Person.fullname.ilike(f"%{search}%"))
        return query

    def get_detail_query(self) -> Query:
        return (
            self.get_default_query()
                .options(
                joinedload(tables.Person.directed).load_only(tables.Show.title, tables.Show.show_id),
                joinedload(tables.Person.starred_in).load_only(tables.Show.title, tables.Show.show_id),
            )
        )
