from flask_admin.contrib.sqla import ModelView


class GenresView(ModelView):
    can_view_details = True
    column_default_sort = "name"
