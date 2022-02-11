from flask_admin.contrib.sqla import ModelView


class CountriesView(ModelView):
    can_view_details = True
    column_default_sort = "name"
