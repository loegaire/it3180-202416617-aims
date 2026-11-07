"""Các hàm tìm kiếm DVD trong danh sách."""


def search_by_title(items, keyword):
    """Trả về các DVD có tiêu đề chứa keyword."""
    return [dvd for dvd in items if keyword in dvd.title]
