from flask_admin.contrib.sqla import ModelView
from flask_admin.model.template import macro

from ..formatters.shows import (
    format_date,
    format_duration,
    format_rating,
    format_type,
    format_title,
)


class ShowsView(ModelView):
    # Access
    can_create = True
    can_view_details = True
    can_edit = True
    can_delete = True
    can_export = True

    # Templates
    details_template = "shows/details.html"
    list_template = "shows/list.html"

    # Columns
    form_columns = ["show_id", "title", "type", "listed_in", "country", "duration", "date_added",
                    "release_year", "director", "cast"]
    column_sortable_list = ["title", "release_year"]
    column_details_list = ["show_id", "title", "type", "listed_in", "country", "duration", "date_added", "release_year",
                           "director", "cast"]
    column_export_list = ["show_id", "title", "type", "listed_in", "country", "duration", "date_added", "release_year",
                          "director", "cast"]
    column_list = ["title", "type", "rating", "release_year", "duration"]
    column_searchable_list = ["show_id", "title", "rating.code", "release_year"]

    # Formatters
    column_formatters = {
        "duration": format_duration,
        "rating": format_rating,
        "type": format_type,
        "title": macro("render_title"),
    }
    column_formatters_detail = {
        "duration": format_duration,
        "rating": format_rating,
        "type": format_type,
        "director": macro("render_persons"),
        "cast": macro("render_persons"),
        "date_added": format_date,
    }
    column_formatters_export = {
        "title": format_title,
    }

    # Customization
    column_default_sort = "title"
    form_ajax_refs = {
        "director": {
            "page_size": 10,
            "fields": ["fullname"],
        },
        "cast": {
            "page_size": 10,
            "fields": ["fullname"],
        },
    }
    export_types = ["csv"]
