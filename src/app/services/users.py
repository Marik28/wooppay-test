from typing import Optional

import sqlalchemy.exc
from loguru import logger
from werkzeug.exceptions import (
    Conflict,
    NotFound,
)

from .generic import GenericCRUDService
from .. import tables
from ..app import bcrypt


class UsersService(GenericCRUDService):
    model = tables.User

    def create(self, username: str, password: str) -> tables.User:
        model = self._get_model()
        password_hash = bcrypt.generate_password_hash(password)
        user_to_create = model(username=username, password_hash=password_hash)
        self.session.add(user_to_create)
        try:
            self.session.commit()
        except sqlalchemy.exc.InternalError:
            self.session.rollback()
            raise Conflict(description="Username is already taken")
        return user_to_create

    def get_by_username(self, username: str) -> tables.User:
        user = self.get_default_query().filter(tables.User.username == username).first()
        if user is None:
            raise NotFound
        logger.debug(f"{user=}")
        return user

    def get_or_none(self, lookup: int) -> Optional[tables.User]:
        logger.debug(F"{lookup=}")
        return self.get_detail_query().filter(tables.User.id == lookup).first()
