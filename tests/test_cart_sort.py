"""Kiểm thử sắp xếp giỏ hàng."""
import unittest

from aims.cart import Cart
from aims.dvd import DigitalVideoDisc


class CartSortTest(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()
        self.cart.add_dvd(DigitalVideoDisc("Star Wars", "Science Fiction", 24.95, "George Lucas", 124))
        self.cart.add_dvd(DigitalVideoDisc("Blade Runner", "Science Fiction", 18.99, "Ridley Scott", 117))
        self.cart.add_dvd(DigitalVideoDisc("The Lion King", "Animation", 19.95, "Roger Allers", 87))

    def test_sort_by_title(self):
        self.assertEqual(
            [dvd.title for dvd in self.cart.sort_by_title()],
            ["Blade Runner", "Star Wars", "The Lion King"],
        )

    def test_sort_by_cost(self):
        self.assertEqual(
            [dvd.cost for dvd in self.cart.sort_by_cost()], [18.99, 19.95, 24.95]
        )


if __name__ == "__main__":
    unittest.main()
