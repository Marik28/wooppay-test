from typing import (
    Union,
)

import sqlalchemy.exc
import sqlalchemy.orm
import sqlalchemy.sql.elements
from sqlalchemy.orm import Query
from werkzeug.exceptions import (
    NotFound,
    Conflict,
)

from .. import tables
from ..utils.pagination import (
    paginate,
    Page,
)

Lookup = Union[int, str]


class GenericCRUDService:
    """
    You should inherit from this class and at least override class attribute `model`.

    order_by_field - if None, ordering is not applied to query. Example: User.username.asc().
    """
    model = None
    order_by: Union[sqlalchemy.sql.elements.UnaryExpression, str, None] = None
    lookup_field: str = "id"

    def __init__(self, session: sqlalchemy.orm.Session) -> None:
        self.session = session

    def _get_model(self):
        if self.model is None or not issubclass(self.model, tables.Base):
            class_name = self.__class__.__name__
            raise ValueError(f"{class_name}.model attribute must be inheritance class of table.Base!")
        return self.model

    def _add(self, instance_to_add):
        self.session.add(instance_to_add)
        try:
            self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            self.session.rollback()
            raise Conflict

    def _get(self, lookup: Lookup):
        query = self.get_detail_query()
        filter_criteria = {self.lookup_field: lookup}
        obj = query.filter_by(**filter_criteria).first()
        if obj is None:
            raise NotFound
        return obj

    def _get_order_by(self):
        return self.order_by

    def get_detail_query(self) -> Query:
        return self.get_default_query()

    def get_default_query(self) -> Query:
        model = self._get_model()
        order_by = self._get_order_by()
        query = self.session.query(model).order_by(order_by)
        return query

    def get_list_query(self, **filters) -> Query:
        """
        Override this method to implement custom filtration and searching logic for `get_list` and `get_page`.

        Recommend using * in method declaration for compatibility like this:

        >>> class MyService(GenericCRUDService):
        ...     def get_list_query(self, *, search: str):
        ...         ...
        """
        query = self.get_default_query()
        query = query.filter_by(**filters)
        return query

    def get(self, lookup: Lookup):
        return self._get(lookup)

    def get_list(self, **filters) -> list:
        """:return: by default - list of all objects"""
        query = self.get_list_query(**filters)
        return query.all()

    def get_page(self, page: int, per_page: int, **filters) -> Page:
        query = self.get_list_query(**filters)
        return paginate(query, page, per_page)
