from flask import (
    Blueprint,
    render_template,
)

from ..database import Session
from ..services.persons import PersonsService

blueprint = Blueprint('persons', __name__, template_folder='templates')


@blueprint.get("/")
def get_persons():
    with Session() as session:
        service = PersonsService(session)
        page = service.get_page(1, 10)
    return render_template(
        "persons/list.html",
        page=page,
        persons=page.items,
    )


@blueprint.get("/<int:person_id>")
def get_person(person_id: int):
    with Session() as session:
        service = PersonsService(session)
        person = service.get(person_id)
    return render_template(
        "persons/detail.html",
        person=person,
    )
