from .generic import GenericCRUDService
from .. import tables


class RatingsService(GenericCRUDService):
    model = tables.Rating
    lookup_field = "id"
    order_by = tables.Rating.code.asc()
