from .generic import GenericCRUDService
from .. import tables


class GenresService(GenericCRUDService):
    model = tables.Genre
    order_by = tables.Genre.name.asc()
