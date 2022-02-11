import sqlalchemy.orm
from flask import Flask
from flask_admin import Admin

from app import tables


def create_app(session: sqlalchemy.orm.Session) -> Flask:
    app = Flask(__name__)

    admin = Admin(app, template_mode="bootstrap4")
    from .views.shows import ShowsView
    admin.add_view(ShowsView(tables.Show, session))
    from .views.persons import PersonsView
    admin.add_view(PersonsView(tables.Person, session))
    from .views.genres import GenresView
    admin.add_view(GenresView(tables.Genre, session))
    from .views.countries import CountriesView
    admin.add_view(CountriesView(tables.Country, session))
    from .views.ratings import RatingsView
    admin.add_view(RatingsView(tables.Rating, session))

    return app
