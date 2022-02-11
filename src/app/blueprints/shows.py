from flask import (
    Blueprint,
    render_template,
)

from ..database import Session
from ..services.shows import ShowsService

blueprint = Blueprint('shows', __name__, template_folder='templates')


@blueprint.get("/")
def get_shows():
    with Session() as session:
        shows_service = ShowsService(session)
        page = shows_service.get_page(1, 10)
    context = {
        "shows": page.items,
        "page": page,
    }
    return render_template("shows/list.html", **context)


@blueprint.get("/<show_id>")
def get_show(show_id):
    with Session() as session:
        service = ShowsService(session)
        show = service.get(show_id)
    return render_template("shows/detail.html", show=show)
