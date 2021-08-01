import math


class paginate:
    def __init__(self, **arg):
        self.limit = arg.get('limit', 15)
        self.page = arg.get('page', 1)
        self.total_item = arg.get('total_item', 0)
        self.total_page = math.ceil(self.total_item / self.limit)
        self.offset = ((self.page * self.limit) - self.limit)

    def toMap(self):
        return {"total_page": self.total_page, "total_item": self.total_item, "page": self.page, "limit": self.limit}
