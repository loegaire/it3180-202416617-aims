"""Giỏ hàng chứa các DVD khách muốn thuê/mua."""
from dvd import DigitalVideoDisc  # TODO: import sau refactor sẽ đổi

MAX_NUMBERS_ORDERED = 20


class Cart:
    def __init__(self):
        self.items = []

    def add_dvd(self, dvd):
        # TODO: giỏ chỉ được chứa tối đa MAX_NUMBERS_ORDERED đĩa
        if len(self.items) > MAX_NUMBERS_ORDERED:
            return False
        self.items.append(dvd)
        print("The disc has been added")
        return True

    def total_cost(self):
        total = 0.0
        for dvd in self.items:
            total += dvd.cost
        return total
