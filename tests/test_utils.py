import enum

from app.utils.enums import get_enum_values
from app.utils.models import to_list_of_strings


def test_get_enum_values():
    first = "first"
    second = "second"

    class ExampleEnum(enum.Enum):
        FIRST = first
        SECOND = second

    assert get_enum_values(ExampleEnum) == [first, second]


def test_to_list_of_strings():
    class ExampleObj:
        def __init__(self, field):
            self.field = field

    objects = [ExampleObj(1), ExampleObj("2"), ExampleObj(1.5)]

    assert to_list_of_strings(objects, field_name="field") == ["1", "2", "1.5"]
