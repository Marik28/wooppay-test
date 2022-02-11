from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    from .blueprints import shows
    app.register_blueprint(shows.blueprint, url_prefix="/shows")

    from .blueprints import persons
    app.register_blueprint(persons.blueprint, url_prefix="/persons")

    return app
