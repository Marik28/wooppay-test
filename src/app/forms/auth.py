from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import (
    InputRequired,
    Length,
    Regexp,
)

from ..settings import settings


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username: ",
        validators=[
            InputRequired(),
            Length(min=settings.password_min_len, max=settings.password_max_len),
            Regexp(r"[A-Za-z0-9_ -]+"),
        ]
    )
    password = PasswordField(
        "Password: ",
        validators=[
            InputRequired(),
            Length(min=settings.username_min_len, max=settings.username_max_len)
        ]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired()])
    submit = SubmitField("Login")
