"""Kiểm thử total_cost_with_discount."""
import unittest

from aims.cart import Cart
from aims.dvd import DigitalVideoDisc


def cart_of(cost):
    cart = Cart()
    cart.add_dvd(DigitalVideoDisc("Test disc", "Test", cost, "Test", 100))
    return cart


class DiscountTest(unittest.TestCase):
    def test_total_cost_with_discount(self):
        # 100 giảm 20% -> phải trả 80
        self.assertAlmostEqual(cart_of(100.0).total_cost_with_discount(20), 80.0)

    def test_total_cost_with_discount_rejects_invalid_percent(self):
        with self.assertRaises(ValueError):
            cart_of(100.0).total_cost_with_discount(150)


if __name__ == "__main__":
    unittest.main()
