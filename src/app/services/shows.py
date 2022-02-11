from .. import tables
from ..services.generic import GenericCRUDService


class ShowsService(GenericCRUDService):
    model = tables.Show
    order_by = tables.Show.title
