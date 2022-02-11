from wtforms.fields import (
    StringField,
)

from .pagination import PaginationParamsForm


class PersonsSearchForm(PaginationParamsForm):
    search = StringField("Search")

    class Meta:
        csrf = False
