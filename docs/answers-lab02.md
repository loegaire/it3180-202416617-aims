# Lab 02 — Câu hỏi thảo luận

Nhánh nộp bài: `release/lab02`. Template PR vào qua PR `topic/pr-template`, tính năng
`print_cart()` vào qua PR `feature/cart-print`, `search_by_title()` vào qua PR
`feature/search-by-title` (Squash), use case vào qua PR `topic/use-case-diagram` (Rebase).

---

## 1. Vì sao phải đồng bộ `master` trước khi gửi PR?

Vì **PR luôn được so với nhánh đích tại thời điểm merge, không phải tại thời điểm bạn tạo
nhánh**. Bỏ qua bước đồng bộ là giao lại việc tích hợp — và mọi rủi ro của nó — cho nhánh đích.

1. **Xử lý xung đột ở nơi có ngữ cảnh.** Xung đột chỉ xuất hiện khi hai bên sửa cùng vùng.
   Nếu bạn tự `git merge origin/master` vào nhánh của mình, bạn giải quyết xung đột khi vẫn còn
   trong đầu ngữ cảnh của thay đổi; nếu để đến lúc merge PR, người/ngày khác phải đoán ý bạn.
   Bài thực hành nói rõ quy tắc 1 của Release Flow: *giữ nhánh càng gần `master` càng tốt, tránh
   "merge hell"*.
2. **Bạn phải là người kiểm tra được trạng thái tích hợp.** CI trên PR chỉ chạy khi PR được tạo,
   và nó kiểm thử `branch + base`. Nếu `base` đã cũ, kết quả đó không nói lên điều gì về trạng thái
   sẽ có trên `master` sau khi merge. Đồng bộ trước rồi chạy test tại máy là cách duy nhất bạn tự
   xác nhận "merge vào là xanh".
3. **Giữ diff đọc được.** Người review đọc `Files changed` so với base. Base cũ ⇒ diff lẫn cả
   thay đổi không liên quan (hoặc che mất thay đổi thật), review mất giá trị.
4. **Giữ được khả năng hoàn tác theo đơn vị.** Một tính năng nằm gọn trong một nhánh đã đồng bộ
   thì có thể `revert` cả tính năng bằng một lệnh; tính năng bị trộn với merge muộn thì khó tách.
5. **Tôn trọng thứ tự merge.** PR nào merge trước sẽ trở thành "sự thật" trên `master`; nhánh còn lại
   buộc phải chấp nhận điều đó. Chủ động đồng bộ = chủ động chấp nhận, thay vì bị động bị đẩy vào
   xung đột ngay trên PR.

**Bằng chứng trong bài này.** Dev 2 tạo `feature/search-by-title` từ `master` lúc đó chưa có
`print_cart()`. Sau khi Dev 1 merge PR `feature/cart-print`, Dev 2 làm:

```
$ git fetch origin
$ git log --oneline --graph --all
*   <merge> Merge pull request #<n> from .../feature/cart-print
...
$ git merge origin/master        # tích hợp trước khi gửi PR
$ python3 main.py                # Total cost: 63.89 $
$ git push -u origin feature/search-by-title
```

Nhờ vậy PR của Dev 2 được merge bằng **Squash and merge** mà không có xung đột nào, và
`master` sau khi merge vẫn chạy đúng `Total cost: 63.89 $`.

---

## 2. Khi nào KHÔNG được rebase?

Rebase tạo **commit mới (SHA mới)**: nó không di chuyển commit, nó *sao chép* commit sang một nền
mới. Vì vậy rebase tương đương với việc **viết lại lịch sử**, và chỉ an toàn với lịch sử chưa chia sẻ.
Các trường hợp tuyệt đối không rebase:

| Tình huống | Vì sao không |
|---|---|
| Commit **đã push** và người khác có thể đã `pull` | SHA đổi ⇒ bản của họ và bản của bạn tách đôi; hợp nhất lại phải force-push, dễ đè mất commit của người khác |
| Trên **`master`** | Lịch sử chung, đã được nhiều người dựa vào; sửa lại sẽ phá mọi fork/branch |
| Trên **`release/*`** | Baseline đã giao/đang được dùng; thay đổi phải là commit mới (`revert`, `hotfix`) |
| Commit **đã có tag phát hành** | Tag trỏ tới object cũ; rebase làm tag treo lơ lửng, không tái tạo được phiên bản |
| PR **đang được review** mà bạn muốn giữ nguyên kết quả review | Rebase đổi commit ⇒ `Dismiss stale approvals` kích hoạt, người review mất mốc để đối chiếu comment |
| Nhánh đang được **nhiều người dùng chung** (feature chung, integrate) | Cùng lý do như commit đã push |

Hệ quả thực hành:

* Cần đưa nhánh lên theo `master` **đã chia sẻ** ⇒ dùng `git merge origin/master` (tạo merge commit,
  không đổi SHA cũ) — đây là cách dùng ở Phần E của Lab 02 và Phần C của Lab 03.
* Nếu buộc phải rebase một nhánh riêng tư, chỉ được đẩy lại bằng
  `git push --force-with-lease` (kiểm tra remote chưa bị người khác đẩy thêm) — **không** dùng
  `git push --force`.
* Trên `master` / `release/*`, muốn "undo" một thay đổi đã chia sẻ thì dùng `git revert`
  (sinh commit đảo ngược, lịch sử chỉ dài thêm chứ không bị viết lại) — xem Lab 03 Phần D.

---

## 3. `feature/*` khác `topic/*` ra sao?

Hai loại nhánh **giống nhau về cơ chế** (đều cắt từ `master`, đều sống ngắn, đều phải đi qua
PR và review) và **khác nhau về ngữ nghĩa**:

| | `feature/<tên>` | `topic/<mô-tả>` |
|---|---|---|
| Bản chất | một **năng lực của sản phẩm** sẽ được phát hành | một **chủ đề công việc**: tài liệu, quy trình, chuẩn bị phát hành, CI |
| Tiêu chí hoàn thành | có hành vi quan sát được + test + (thường) mục trong `CHANGELOG` | hoàn thành khi nội dung/chủ đề được chốt |
| Type commit điển hình | `feat:` | `docs:`, `chore:`, `ci:`, `test:` |
| Ví dụ trong repo | `feature/cart-print`, `feature/search-by-title`, `feature/sort-cart`, `feature/search-by-category` | `topic/pr-template`, `topic/use-case-diagram`, `topic/prepare-release-1.0.0`, `topic/ci-unit-tests` |
| Xuất hiện trong release notes | có (Added/Changed/Fixed) | thường không sinh mục phiên bản |

Cách quyết định nhanh: nếu thay đổi **làm người dùng thấy khác** thì gọi là `feature/`;
nếu thay đổi **làm cách làm việc rõ hơn** (tài liệu, use case, template, chuẩn bị release, CI)
thì gọi là `topic/`. Việc đặt tên đúng giúp "một nhánh, một mục đích" trở nên **kiểm toán được**:
chỉ cần đọc tên nhánh là biết nó có cần test/CHANGELOG hay không, và người review biết phải soi gì.

---

## Phụ lục — So sánh 3 kiểu merge (Phần F, G)

| Tiêu chí | Merge commit | Squash | Rebase |
|---|---|---|---|
| Giữ nguyên commit chi tiết của nhánh | ✔ | ✘ (gộp thành 1 commit) | ✔ nhưng **SHA mới** |
| Lịch sử tuyến tính | ✘ (có merge commit) | ✔ | ✔ |
| Truy vết "commit này thuộc tính năng nào" | thấy rõ bằng merge commit | ✘ (chỉ còn 1 commit `(#PR)`) | phải suy từ vị trí |
| Revert cả tính năng | 1 lệnh `git revert -m 1 <merge-sha>` | 1 lệnh `git revert <sha>` | phải revert nhiều commit |
| `git branch -d` sau khi merge | dùng được `-d` | phải dùng `-D` (Git không nhận ra "đã merge") | phải dùng `-D` |
| Phù hợp khi | tính năng nhiều commit, muốn giữ lịch sử phát triển | nhánh lộn xộn ("wip", "fix typo") cần dọn | muốn `master` phẳng, commit sạch |

Trong bài này cả ba kiểu đều có thật trên cùng một `master`:
PR `feature/cart-print` merge bằng **Merge commit** (giữ 3 commit chi tiết của vòng review),
PR `feature/search-by-title` bằng **Squash**, PR `topic/use-case-diagram` bằng **Rebase**.
Kiểm chứng bằng `git log --oneline --graph` trên `master`.
