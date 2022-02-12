from flask_login import login_user
from flask_wtf import FlaskForm
from werkzeug.exceptions import (
    Conflict,
    NotFound,
)
from wtforms.fields import (
    StringField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import (
    InputRequired,
    Length,
    Regexp,
    ValidationError,
)

from ..app import bcrypt
from ..database import Session
from ..services.users import UsersService
from ..settings import settings


class RegistrationForm(FlaskForm):

    def __init__(self, formdata=None, **kwargs):
        super().__init__(formdata=formdata, **kwargs)
        self._user = None

    username = StringField(
        "Username: ",
        validators=[
            InputRequired(),
            Length(min=settings.username_min_len, max=settings.username_max_len),
            Regexp(r"[A-Za-z0-9_ -]+", message="Only latin characters, '-_' and spaces are allowed "),
        ],
    )
    password = PasswordField(
        "Password: ",
        validators=[
            InputRequired(),
            Length(min=settings.password_min_len, max=settings.password_max_len)
        ],
    )
    submit = SubmitField("Register")

    @staticmethod
    def validate_username(form, field):
        with Session() as session:
            try:
                created_user = UsersService(session).create(field.data, form.password.data)
            except Conflict as exc:
                raise ValidationError(message=exc.description)
            # TODO: think of better solution
            login_user(created_user, remember=True)


class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired()])
    submit = SubmitField("Login")

    @staticmethod
    def validate_username(form, field):
        from loguru import logger
        logger.debug(f"{field.data=}")
        with Session() as session:
            error = ValidationError("Invalid username or password")
            try:
                user = UsersService(session).get_by_username(field.data)
                logger.debug(f"{user.password_hash=}")
            except NotFound:
                raise error

            if not bcrypt.check_password_hash(user.password_hash, form.password.data):
                raise error
            # TODO: think of better solution
            logger.debug(f"{user=}")
            login_user(user, remember=True)

            from flask_login import current_user
            logger.debug("---LOGGED---")
            logger.debug(f"{current_user=}")
