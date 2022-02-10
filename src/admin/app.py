import sqlalchemy.orm
from flask import Flask
from flask_admin import Admin

from app import tables


def create_app(session: sqlalchemy.orm.Session) -> Flask:
    app = Flask(__name__)

    admin = Admin(app, template_mode="bootstrap4")
    from .views.shows import ShowsView
    admin.add_view(ShowsView(tables.Show, session))

    return app
