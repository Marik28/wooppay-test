def to_list_of_strings(objects: list, field_name: str) -> list[str]:
    return [str(getattr(obj, field_name)) for obj in objects]
