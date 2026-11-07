"""Giỏ hàng chứa các DVD khách muốn thuê/mua."""
from aims.dvd import DigitalVideoDisc

MAX_NUMBERS_ORDERED = 20


class Cart:
    def __init__(self):
        self.items = []

    def add_dvd(self, dvd):
        if len(self.items) >= MAX_NUMBERS_ORDERED:
            return False
        self.items.append(dvd)
        print("The disc has been added")
        return True

    def total_cost(self):
        total = 0.0
        for dvd in self.items:
            total += dvd.cost
        return total

    def print_cart(self):
        if not self.items:
            print("The cart is empty")
            return
        for index, dvd in enumerate(self.items, 1):
            print(f"{index}. {dvd}")
        print(f"Total cost: {self.total_cost():.2f} $")
