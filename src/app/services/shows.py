from .. import tables
from ..services.generic import GenericCRUDService


class ShowsService(GenericCRUDService):
    model = tables.Show
    lookup_field = "show_id"
    order_by = tables.Show.title.asc()
