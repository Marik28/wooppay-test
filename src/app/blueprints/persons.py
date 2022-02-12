from flask import (
    Blueprint,
    render_template, request,
)
from werkzeug.datastructures import MultiDict

from ..database import Session
from ..forms.persons import PersonsSearchForm
from ..services.persons import PersonsService

blueprint = Blueprint('persons', __name__, template_folder='templates')


# TODO: add reset filters button
@blueprint.get("/")
def get_persons():
    query = MultiDict(request.args)
    query.pop("page", None)
    form = PersonsSearchForm(request.args)
    if form.validate():
        with Session() as session:
            service = PersonsService(session)
            page = service.get_page(**form.data)
            persons = page.items
    else:
        persons = []
        page = None
    return render_template(
        "persons/list.html",
        page=page,
        persons=persons,
        form=form,
        query=query,
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
