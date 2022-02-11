from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import IntegerField
from wtforms.widgets import NumberInput


# TODO: this definitely won't work after inheritance
class PaginationParamsForm(FlaskForm):
    min_per_page = 1
    max_per_page = 100

    page = IntegerField(default=1)
    per_page = IntegerField(default=10, widget=NumberInput(min=min_per_page, max=max_per_page))

    @staticmethod
    def validate_per_page(form, field):
        if field.data is None:
            return
        min_value = form.min_per_page
        max_value = form.max_per_page
        if not (min_value <= field.data <= max_value):
            raise ValidationError(f"Value must be between {min_value} and {max_value}")
