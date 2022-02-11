from flask import Flask
from flask_wtf.csrf import CSRFProtect

from .settings import settings

csrf = CSRFProtect()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.secret_key

    from .blueprints import shows
    app.register_blueprint(shows.blueprint, url_prefix="/shows")

    from .blueprints import persons
    app.register_blueprint(persons.blueprint, url_prefix="/persons")

    csrf.init_app(app)

    return app
