"""Lớp biểu diễn một đĩa DVD của cửa hàng AIMS-mini."""


class DigitalVideoDisc:
    def __init__(self, title, category="", cost=0.0, director="", length=0):
        self.title = title
        self.category = category
        self.cost = cost
        self.director = director
        self.length = length

    def get_title(self):
        return self.title

    def get_category(self):
        return self.category

    def get_cost(self):
        return self.cost

    def get_director(self):
        return self.director

    def get_length(self):
        return self.length

    def set_title(self, title):
        self.title = title

    def set_category(self, category):
        self.category = category

    def set_cost(self, cost):
        self.cost = cost

    def set_director(self, director):
        self.director = director

    def set_length(self, length):
        self.length = length

    def __str__(self):
        return f"DVD - {self.title} - {self.category} - {self.cost} $"
