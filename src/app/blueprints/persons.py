from flask import (
    Blueprint,
    render_template, request,
)

from ..app import csrf
from ..database import Session
from ..forms.persons import PersonsSearchForm
from ..services.persons import PersonsService

blueprint = Blueprint('persons', __name__, template_folder='templates')


@blueprint.get("/")
@csrf.exempt
def get_persons():
    form = PersonsSearchForm(request.args)
    if form.validate():
        with Session() as session:
            service = PersonsService(session)
            page = service.get_page(form.page.data, form.per_page.data, search=form.search.data)
            persons = page.items
    else:
        persons = []
        page = None
    return render_template(
        "persons/list.html",
        page=page,
        persons=persons,
        form=form,
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
