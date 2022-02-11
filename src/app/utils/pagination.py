import math

from sqlalchemy.orm import Query


class Page:

    def __init__(self, items: list, page: int, page_size: int, total: int):
        self.items = items
        self.page = page
        self.first_page = self.page == 1
        self.previous_page = None
        self.next_page = None
        self.has_previous = page > 1
        if self.has_previous:
            self.previous_page = page - 1
        previous_items = (page - 1) * page_size
        self.has_next = previous_items + len(items) < total
        if self.has_next:
            self.next_page = page + 1
        self.total = total
        self.pages = int(math.ceil(total / float(page_size)))
        self.last_page = page == self.pages


def paginate(query: Query, page: int, page_size: int) -> Page:
    if page <= 0:
        raise AttributeError('page needs to be >= 1')
    if page_size <= 0:
        raise AttributeError('page_size needs to be >= 1')
    items = query.limit(page_size).offset((page - 1) * page_size).all()
    total: int = query.order_by(None).count()
    return Page(items, page, page_size, total)
