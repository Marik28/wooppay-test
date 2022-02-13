from .protected import ProtectedView


class CountriesView(ProtectedView):
    can_view_details = True
    column_default_sort = "name"
