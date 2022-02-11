from flask import (
    Blueprint,
    render_template,
)


blueprint = Blueprint('persons', __name__, template_folder='templates')