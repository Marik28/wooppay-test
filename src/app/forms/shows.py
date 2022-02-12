from wtforms import ValidationError
from wtforms.fields import (
    StringField,
    RadioField,
    IntegerField,
)
from wtforms.validators import (
    NumberRange,
    Optional,
)

from .fields.checkbox_list import MultiCheckboxField
from .pagination import PaginationParamsForm
from ..models.shows import ShowType
from ..utils.enums import get_enum_values


class ShowsSearchForm(PaginationParamsForm):
    search = StringField("Search", validators=[Optional()])
    show_type = RadioField(
        "Show type",
        choices=get_enum_values(ShowType),
        validators=[Optional()],
    )
    rating = RadioField("Rating", validators=[Optional()])
    duration_min = IntegerField(
        "Minimal duration",
        validators=[NumberRange(min=0), Optional()],
    )
    duration_max = IntegerField(
        "Maximal duration",
        validators=[NumberRange(min=1), Optional()],
    )
    release_year = IntegerField(
        "Release year",
        validators=[NumberRange(min=1888, max=2022), Optional()],
    )
    countries = MultiCheckboxField("Countries", validators=[Optional()])
    genres = MultiCheckboxField("Genres", validators=[Optional()])

    @staticmethod
    def validate_duration_min(form, field):
        duration_min = field.data
        duration_max = form.duration_max.data

        if duration_min is None or duration_max is None:
            return

        if duration_min > duration_max:
            raise ValidationError("Minimal duration must be less than maximal.")

    class Meta:
        csrf = False
