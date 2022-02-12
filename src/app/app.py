from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from loguru import logger

from .database import Session
from .settings import settings

csrf = CSRFProtect()
bcrypt = Bcrypt()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.secret_key

    from .blueprints import shows
    app.register_blueprint(shows.blueprint, url_prefix="/shows")

    from .blueprints import persons
    app.register_blueprint(persons.blueprint, url_prefix="/persons")

    from .blueprints import auth
    app.register_blueprint(auth.blueprint)

    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        logger.debug(f"{user_id=}")
        from .services.users import UsersService
        with Session() as session:
            user = UsersService(session).get_or_none(int(user_id))
            logger.debug(user.username)
            return user

    from werkzeug.exceptions import Unauthorized
    from flask.typing import GenericException

    @app.errorhandler(Unauthorized)
    def handle_unauthorized(error: GenericException):
        return render_template("errors/401.html", error=error)

    csrf.init_app(app)
    bcrypt.init_app(app)

    return app
