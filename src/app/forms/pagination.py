from flask_wtf import FlaskForm
from wtforms.fields import IntegerField
from wtforms.validators import NumberRange


# TODO: this definitely won't work after inheritance
class PaginationParamsForm(FlaskForm):
    min_per_page = 1
    max_per_page = 100

    page = IntegerField(default=1)
    per_page = IntegerField(
        default=10,
        validators=[NumberRange(min=min_per_page, max=max_per_page)]
    )
