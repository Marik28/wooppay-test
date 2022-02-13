from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
)
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from . import tables
from .database import Session
from .settings import settings

csrf = CSRFProtect()
bcrypt = Bcrypt()
db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    csrf.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)

    # Admin application
    admin = Admin(app, template_mode="bootstrap4")

    from admin.views.shows import ShowsView
    admin.add_view(ShowsView(tables.Show, db.session))

    from admin.views.persons import PersonsView
    admin.add_view(PersonsView(tables.Person, db.session))

    from admin.views.genres import GenresView
    admin.add_view(GenresView(tables.Genre, db.session))

    from admin.views.countries import CountriesView
    admin.add_view(CountriesView(tables.Country, db.session))

    from admin.views.ratings import RatingsView
    admin.add_view(RatingsView(tables.Rating, db.session))

    from admin.views.users import UsersView
    admin.add_view(UsersView(tables.User, db.session))

    # Blueprints
    from .blueprints import shows
    app.register_blueprint(shows.blueprint, url_prefix="/shows")

    from .blueprints import persons
    app.register_blueprint(persons.blueprint, url_prefix="/persons")

    from .blueprints import auth
    app.register_blueprint(auth.blueprint)

    @app.get("/")
    def index():
        return redirect(url_for("shows.get_shows"))

    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .services.users import UsersService
        with Session() as session:
            user = UsersService(session).get_or_none(int(user_id))
            return user

    from werkzeug.exceptions import Unauthorized
    from flask.typing import GenericException

    @app.errorhandler(Unauthorized)
    def handle_unauthorized(error: GenericException):
        return render_template("errors/401.html", error=error), 401

    return app
