"""Kiểm thử Cart - regression test cho Issue giới hạn 20 đĩa."""
import unittest

from aims.cart import MAX_NUMBERS_ORDERED, Cart
from aims.dvd import DigitalVideoDisc


def make_dvd(index):
    return DigitalVideoDisc(f"DVD {index}", "Test", 1.0, "Test", 100)


class CartLimitTest(unittest.TestCase):
    def test_add_dvd_until_full(self):
        cart = Cart()
        for index in range(MAX_NUMBERS_ORDERED):
            self.assertTrue(cart.add_dvd(make_dvd(index)), f"đĩa thứ {index + 1}")
        # Đĩa thứ 21 phải bị từ chối
        self.assertFalse(cart.add_dvd(make_dvd(21)))
        self.assertEqual(len(cart.items), MAX_NUMBERS_ORDERED)


if __name__ == "__main__":
    unittest.main()
