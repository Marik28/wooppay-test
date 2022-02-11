from .generic import GenericCRUDService
from .. import tables


class CountriesService(GenericCRUDService):
    model = tables.Country
    order_by = tables.Country.name.asc()
