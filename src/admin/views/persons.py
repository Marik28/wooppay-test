from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import macro


class PersonsView(ModelView):
    can_view_details = True
    column_searchable_list = ["fullname"]
    column_default_sort = "fullname"
    column_details_list = ["fullname", "starred_in", "directed"]
    form_columns = ["fullname"]
    column_formatters_detail = {
        "starred_in": macro("render_shows"),
        "directed": macro("render_shows"),
    }
    column_formatters = {
        "fullname": macro("render_person_fullname"),
    }

    form_ajax_refs = {
        "directed": {
            "fields": ["title"],
            "page_size": 10,
        },
        "starred_in": {
            "fields": ["title"],
            "page_size": 10,
        },
    }

    list_template = "persons/list.html"
    details_template = "persons/details.html"
