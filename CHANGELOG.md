# Changelog

Mọi thay đổi đáng chú ý của AIMS-mini được ghi lại trong tệp này.
Định dạng dựa trên [Keep a Changelog](https://keepachangelog.com/vi/1.1.0/)
và dự án tuân theo [Semantic Versioning](https://semver.org/lang/vi/).

## [Unreleased]

## [1.1.0] - 2026-11-06

### Added

- `search_by_category()` — tìm DVD theo thể loại (không phân biệt hoa/thường).
- `Cart.sort_by_title()` và `Cart.sort_by_cost()`.

### Fixed

- `search_by_title()` phân biệt chữ hoa/chữ thường (lan truyền từ bản vá v1.0.1
  bằng `git cherry-pick -x`).

## [1.0.0] - 2026-11-06

Ấn bản đầu tiên được định danh bằng tag và GitHub Release: dòng bảo trì `release/lab04`.

### Added

- `Cart.print_cart()` — in nội dung giỏ hàng và tổng tiền.
- `search_by_title()` trong gói `aims` (tìm theo tiêu đề).
- `Cart.total_cost_with_discount(percent)` — tính số tiền phải trả sau giảm giá.

### Fixed

- Giỏ hàng nhận đĩa thứ 21 dù giới hạn là 20 (`MAX_NUMBERS_ORDERED`).
