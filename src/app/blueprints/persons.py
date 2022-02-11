from flask import (
    Blueprint,
    render_template,
)
from loguru import logger

from ..database import Session
from ..services.persons import PersonsService

blueprint = Blueprint('persons', __name__, template_folder='templates')


@blueprint.get("/")
def get_persons():
    with Session() as session:
        service = PersonsService(session)
        page = service.get_page(1, 10)
        logger.debug(page)
    return render_template(
        "persons/list.html",
        page=page,
        persons=page.items,
    )
