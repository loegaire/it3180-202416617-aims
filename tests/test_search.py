"""Kiểm thử search_by_title."""
import unittest

from aims.dvd import DigitalVideoDisc
from aims.search import search_by_title


class SearchByTitleTest(unittest.TestCase):
    def test_search_by_title(self):
        items = [
            DigitalVideoDisc("The Lion King", "Animation", 19.95, "Roger Allers", 87),
            DigitalVideoDisc("Star Wars", "Science Fiction", 24.95, "George Lucas", 124),
        ]
        self.assertEqual(
            [dvd.title for dvd in search_by_title(items, "Lion")], ["The Lion King"]
        )


if __name__ == "__main__":
    unittest.main()
