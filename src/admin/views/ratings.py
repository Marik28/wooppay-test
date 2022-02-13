from .protected import ProtectedView


class RatingsView(ProtectedView):
    can_view_details = True
    column_default_sort = "code"
    form_columns = ["code"]
