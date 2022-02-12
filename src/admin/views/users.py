from flask_admin.contrib.sqla import ModelView


class UsersView(ModelView):
    can_create = False
    can_view_details = True
    can_edit = False
    can_delete = False

    column_list = ["username", "is_admin"]
    column_details_list = ["username", "is_admin"]
