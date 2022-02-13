from .protected import ProtectedView


class UsersView(ProtectedView):
    can_create = False
    can_view_details = True
    can_edit = False
    can_delete = False

    column_list = ["username", "is_admin"]
    column_details_list = ["username", "is_admin"]
