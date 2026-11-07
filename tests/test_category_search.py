"""Kiểm thử search_by_category."""
import unittest

from aims.dvd import DigitalVideoDisc
from aims.search import search_by_category


class SearchByCategoryTest(unittest.TestCase):
    def test_search_by_category(self):
        items = [
            DigitalVideoDisc("The Lion King", "Animation", 19.95, "Roger Allers", 87),
            DigitalVideoDisc("Star Wars", "Science Fiction", 24.95, "George Lucas", 124),
            DigitalVideoDisc("Blade Runner", "Science Fiction", 18.99, "Ridley Scott", 117),
        ]
        self.assertEqual(
            [dvd.title for dvd in search_by_category(items, "science fiction")],
            ["Star Wars", "Blade Runner"],
        )


if __name__ == "__main__":
    unittest.main()
