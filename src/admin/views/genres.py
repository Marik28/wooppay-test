from .protected import ProtectedView


class GenresView(ProtectedView):
    can_view_details = True
    column_default_sort = "name"
