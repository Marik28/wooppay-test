from flask_admin.model.template import macro

from .protected import ProtectedView


class PersonsView(ProtectedView):
    # Access
    can_view_details = True

    # Templates
    list_template = "admin/persons/list.html"
    details_template = "admin/persons/details.html"

    # Columns
    column_searchable_list = ["fullname"]
    column_default_sort = "fullname"
    column_details_list = ["fullname", "starred_in", "directed"]
    form_columns = ["fullname"]

    # Formatters

    column_formatters_detail = {
        "starred_in": macro("render_shows"),
        "directed": macro("render_shows"),
    }
    column_formatters = {
        "fullname": macro("render_person_fullname"),
    }

    # Customization

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
