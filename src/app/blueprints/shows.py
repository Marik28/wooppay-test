from flask import (
    Blueprint,
    render_template,
    request,
)
from flask_login import login_required
from werkzeug.datastructures import MultiDict

from ..database import Session
from ..forms.shows import ShowsSearchForm
from ..services.countries import CountriesService
from ..services.genres import GenresService
from ..services.ratings import RatingsService
from ..services.shows import ShowsService
from ..utils.models import to_list_of_strings

blueprint = Blueprint('shows', __name__, template_folder='templates')


# TODO: add reset filters button

@blueprint.get("/")
@login_required
def get_shows():
    query = MultiDict(request.args)
    query.pop("page", None)
    with Session() as session:
        form = ShowsSearchForm(request.args, active=True)
        available_ratings = RatingsService(session).get_list()
        form.rating.choices = to_list_of_strings(available_ratings, "code")
        available_countries = CountriesService(session).get_list()
        form.countries.choices = to_list_of_strings(available_countries, "name")
        available_genres = GenresService(session).get_list()
        form.genres.choices = to_list_of_strings(available_genres, "name")
        if form.validate():
            page = ShowsService(session).get_page(**form.data)
            shows = page.items
        else:
            page = None
            shows = []
    context = {
        "shows": shows,
        "page": page,
        "form": form,
        "query": query,
    }
    return render_template("shows/list.html", **context)


@blueprint.get("/<show_id>")
@login_required
def get_show(show_id):
    with Session() as session:
        service = ShowsService(session)
        show = service.get(show_id)
    return render_template("shows/detail.html", show=show)
