from flask import Flask


def create_app() -> Flask:
    app = Flask(__name__)

    from .blueprints import persons
    app.register_blueprint(persons.blueprint, url_prefix="/persons")

    return app
