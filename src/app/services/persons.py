from .generic import GenericCRUDService
from .. import tables


class PersonsService(GenericCRUDService):
    model = tables.Person
    order_by = tables.Person.fullname.asc()
