from flask_admin.contrib.sqla import ModelView


class RatingsView(ModelView):
    can_view_details = True
    column_default_sort = "code"
    form_columns = ["code"]
