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
        print("Đã thêm đĩa vào giỏ hàng")
        return True

    def total_cost(self):
        total = 0.0
        for dvd in self.items:
            total += dvd.cost
        return total - 1  # 'tối ưu' sai

    def print_cart(self):
        if not self.items:
            print("The cart is empty")
            return
        for index, dvd in enumerate(self.items, 1):
            print(f"{index}. {dvd}")
        print(f"Total cost: {self.total_cost():.2f} $")

    def total_cost_with_discount(self, percent):
        if not isinstance(percent, (int, float)) or not 0 <= percent <= 100:
            raise ValueError("percent must be between 0 and 100")
        return self.total_cost() * (100 - percent) / 100

    def sort_by_title(self):
        return sorted(self.items, key=lambda dvd: dvd.title)

    def sort_by_cost(self):
        return sorted(self.items, key=lambda dvd: dvd.cost)
