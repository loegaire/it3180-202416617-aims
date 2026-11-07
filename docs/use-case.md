# AIMS-mini — Sơ đồ ca sử dụng (Use Case Diagram)

Tài liệu này mô tả phạm vi chức năng của AIMS-mini, làm cơ sở cho các test và cho
`search_by_title()` / `print_cart()` được phát triển ở Lab 02.

## Tác nhân (Actors)

| Tác nhân | Mô tả |
|---|---|
| Khách hàng (Customer) | Người muốn xem/thuê đĩa DVD |
| Nhân viên cửa hàng (Staff) | Người thao tác giỏ hàng, in hoá đơn, tra cứu đĩa |

## Sơ đồ (dạng văn bản)

```
                       +---------------- ---------------+
                       |          AIMS-mini            |
                       |                               |
   +-----------+       |  (UC01) Xem danh sách DVD     |
   |           |------>|  (UC02) Thêm DVD vào giỏ      |
   | Khách     |       |  (UC03) Xem giỏ hàng          |
   | hàng      |       |  (UC04) Tính tổng tiền        |
   +-----------+       |  (UC05) Áp dụng giảm giá      |
                       |  (UC06) Tìm đĩa theo tiêu đề  |
   +-----------+       |  (UC07) Tìm đĩa theo thể loại |
   | Nhân viên |------>|  (UC08) Sắp xếp giỏ hàng      |
   | cửa hàng  |       |                               |
   +-----------+       +-------------------------------+
                                |
                                |  <<include>>
                                v
                       +-----------------------+
                       | (UC09) Kiểm tra giới  |
                       | hạn 20 đĩa mỗi giỏ    |
                       +-----------------------+
```

## Đặc tả các ca sử dụng

| Mã | Ca sử dụng | Điều kiện trước | Luồng chính | Điều kiện sau | Mã nguồn |
|---|---|---|---|---|---|
| UC01 | Xem danh sách DVD | Chương trình đã khởi động | Hệ thống hiển thị các DVD mẫu | Danh sách hiển thị | `main.py` |
| UC02 | Thêm DVD vào giỏ | Giỏ chưa đủ 20 đĩa | `add_dvd(dvd)` → thêm vào `items`, trả `True` | Giỏ có thêm 1 đĩa | `aims/cart.py` |
| UC03 | Xem giỏ hàng | – | `print_cart()` in từng đĩa và tổng tiền; nếu giỏ trống in `The cart is empty` | Nội dung giỏ hiển thị | `aims/cart.py` |
| UC04 | Tính tổng tiền | – | `total_cost()` cộng `cost` của mọi đĩa | Trả về tổng tiền | `aims/cart.py` |
| UC05 | Áp dụng giảm giá | `0 ≤ percent ≤ 100` | `total_cost_with_discount(percent)` trả về số tiền phải trả | Nếu `percent` ngoài khoảng → `ValueError` | `aims/cart.py` |
| UC06 | Tìm đĩa theo tiêu đề | – | `search_by_title(items, keyword)` lọc theo tiêu đề | Danh sách đĩa khớp | `aims/search.py` |
| UC07 | Tìm đĩa theo thể loại | – | `search_by_category(items, category)` lọc theo thể loại | Danh sách đĩa khớp | `aims/search.py` |
| UC08 | Sắp xếp giỏ hàng | – | `sort_by_title()` / `sort_by_cost()` trả về danh sách đã sắp | Danh sách đã sắp | `aims/cart.py` |
| UC09 | Kiểm tra giới hạn 20 đĩa | – | Khi giỏ đã đủ `MAX_NUMBERS_ORDERED` đĩa, `add_dvd` trả `False` | Giỏ không vượt quá 20 đĩa | `aims/cart.py` |

## Quy tắc nghiệp vụ

1. Một giỏ hàng chứa **tối đa 20 đĩa** (`MAX_NUMBERS_ORDERED = 20`); đĩa thứ 21 bị từ chối.
2. `total_cost_with_discount(percent)` trả về **số tiền phải trả** (không phải số tiền được giảm)
   và **phải** ném `ValueError` khi `percent` không hợp lệ.
3. Tìm kiếm theo tiêu đề **không phân biệt chữ hoa/chữ thường** (yêu cầu nghiệp vụ — đây chính là
   lỗi được tìm thấy và sửa ở Lab 05 bằng hotfix).
