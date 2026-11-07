# Lab 04 — Câu hỏi thảo luận

Nhánh nộp bài: `release/lab04`, baseline được định danh bằng tag annotated `v1.0.0` và
GitHub Release `v1.0.0`. Các bản cũ được gắn tag hồi tố: `v0.1.0` (Lab 01), `v0.2.0` (Lab 02),
`v0.3.0` (Lab 03).

---

## 1. Vì sao `release/*` không merge ngược vào `master`?

Vì `release/*` là **dòng hạ nguồn (downstream)**, không phải một dòng phát triển song song.
Trộn ngược lại phá ba thứ:

1. **Phá chiều một của đồ thị.** `master` là nguồn sự thật (source of truth) cho mã nguồn;
   `release/*` được *sinh ra từ* một commit của `master` và sau đó chỉ nhận các bản vá nhỏ
   được truyền xuống. Nếu merge ngược, đồ thị có chu trình `master → release/lab04 → master`,
   và mọi câu hỏi kiểu "cái gì có trên nhánh này mà không có trên nhánh kia" (`git log A..B`,
   `git diff --stat A B`, `git describe`) trở nên mập mờ — mất luôn khả năng *status accounting*.
2. **Mang ngược các "thay đổi chỉ thuộc về dòng bảo trì".** Trên `release/lab04` có những commit
   *cố ý* không có trên `master`: bump `__version__ = "1.0.1"`, mục `[1.0.1]` trong CHANGELOG,
   tag `v1.0.1`. Merge ngược sẽ kéo chúng vào `master` — nơi phiên bản đã là `1.1.0` — và tạo ra
   đúng loại xung đột mà Lab 05 gặp phải:
   `compare/master...hotfix/... → "Can't automatically merge: commit 2 đặt 1.0.1, xung đột với 1.1.0"`.
3. **Phá tính bất biến của baseline.** Một baseline chỉ có nghĩa khi nó bị "đóng băng": nội dung của
   `release/lab04` tại thời điểm nộp = nội dung của tag `v1.0.0`. Nếu nó còn bị dùng để "đẩy về"
   `master`, người ta sẽ bắt đầu commit lên đó, và baseline biến thành một nhánh phát triển thứ hai.

Quy tắc 4 của Release Flow phát biểu đúng điều này: **`release/*` không bao giờ merge ngược vào
`master`**. Thay vào đó, khi một bản sửa trên dòng phát hành cần có mặt ở `master`, ta tạo nhánh
`hotfix/*` **từ `master`** và **`git cherry-pick -x`** đúng commit sửa lỗi — nghĩa là `master` nhận
*mã sửa lỗi*, không nhận *danh tính phiên bản* của dòng 1.0.x (Lab 05).

Kiểm chứng trạng thái bằng (Phần F, status accounting):

```
$ git log --oneline master..release/lab04    # kỳ vọng: rỗng, release không có gì master chưa có
$ git log --oneline release/lab04..master    # master đi trước release những commit nào
```

---

## 2. So sánh với GitFlow

| | Release Flow (học phần) | GitFlow |
|---|---|---|
| Nhánh tích hợp | `master` (duy nhất) | `develop` (tích hợp) **và** `main` (phát hành) |
| Nhánh phát hành | `release/labXX` cắt từ `master`, **không merge ngược** | `release/*` cắt từ `develop`, **merge vào `main` và `develop`** |
| Nơi "đánh bóng" bản phát hành | trên `master`, **trước khi** cắt baseline | **trên chính nhánh `release/*`** (sửa lỗi, tăng version) |
| Hotfix tạo từ | `release/*` (bản đã phát hành) | `main` |
| Hotfix đi về đâu | `release/*` + `master` (qua `cherry-pick`) | `main` + `develop` (merge trực tiếp cả hai) |
| Số dòng tồn tại song song | nhiều (`release/lab04`, `release/lab05`, …) để nộp theo tuần | thường 1 bản đang phát hành + 1 đang phát triển |

Điểm khác biệt gốc rễ: **GitFlow cần nhánh `release/*` merge ngược** vì đó là nơi công việc hoàn
thiện cuối cùng diễn ra (tăng version, viết release note, sửa lỗi nhỏ) — nếu không merge ngược thì
`develop` sẽ thiếu những sửa đổi đó ở lần phát hành sau. **Release Flow của học phần không cần điều
đó** vì mọi công việc hoàn thiện đều đã làm trên `master` trước khi cắt baseline: `release/labXX`
chỉ còn là *ảnh chụp* (snapshot) + dòng bảo trì, nên nó chỉ nhận thêm chứ không bao giờ trả về.
Vì vậy GitFlow có luồng **hai chiều** (`develop ⇄ release → main`) còn học phần có luồng **một chiều**
(`master → release/*`, và bản vá quay lại `master` bằng `cherry-pick`, không bằng merge nhánh).

Cũng vì vậy `hotfix` khác nhau: GitFlow tạo `hotfix` từ `main` (upstream-first), học phần tạo từ
`release/*` (release-first) rồi mới lan truyền lên `master`.

---

## 3. Vì sao lên `1.0.0` mà không phải `0.4.0`?

Vì **số phiên bản nói về chính sách tương thích, không phải về số thứ tự bài học.**

1. **SemVer định nghĩa `0.y.z` là giai đoạn đầu, chưa ổn định.** Trong miền `0.y.z`, mọi thứ có thể
   thay đổi bất kỳ lúc nào, kể cả phá vỡ tương thích, mà không cần tăng `0`. Khi bạn phát hành `1.0.0`,
   bạn đang **hứa**: từ đây trở đi, chỉ `MAJOR` mới được tăng khi có thay đổi phá vỡ tương thích;
   `MINOR` là thêm tính năng tương thích ngược; `PATCH` là chỉ sửa lỗi. Đó là một *cam kết*,
   không phải một con số đếm.
2. **Ở Lab 04, cam kết đó đã có cơ sở.** Bề mặt công khai của thư viện đã được định hình và kiểm thử:
   `DigitalVideoDisc`, `Cart` (`add_dvd`, `total_cost`, `total_cost_with_discount`, `print_cart`),
   `aims.search.search_by_title`, có use case (UC01–UC09), có test hồi quy cho lỗi giới hạn 20 đĩa,
   và baseline lần đầu tiên được đóng băng + định danh bằng tag/GitHub Release. Đó chính là mốc
   "API đã ổn định".
3. **`0.4.0` sẽ nói sai sự thật.** Nó ngụ ý "phiên bản thứ tư, vẫn đang thử nghiệm" — trong khi thứ
   tự bài học là chuyện của *quy trình*, còn phiên bản là chuyện của *sản phẩm*. Người dùng chỉ quan
   tâm "tôi có thể dựa vào API này không".
4. **Không dùng lại miền `0.y.z` đã cấp cho Lab 01–03.** Ba lab đầu *đúng là* giai đoạn chưa ổn định,
   và chúng đã được định danh hồi tố bằng `v0.1.0`, `v0.2.0`, `v0.3.0` — tức miền `0.y.z` đã được dùng
   hết cho "chưa ổn định". Nếu Lab 04 cũng là `0.4.0` thì không còn gì phân biệt lần đóng băng đầu tiên
   với các mốc thử nghiệm trước đó; còn `1.0.0` nói ngay: *đây là bản ổn định đầu tiên*.
5. **Mở đường cho bảo trì song song (Lab 05).** Chính vì đã có `1.0.0` (một baseline ổn định, được bảo
   vệ, có tag không thể di chuyển) mà Lab 05 mới làm được bài toán đa phiên bản: `1.0.1` là bản vá
   tương thích ngược trên dòng 1.0.x, `1.1.0` là MINOR trên `master`. Nếu mọi thứ vẫn còn `0.x.y` thì
   quy tắc "PATCH thì phải tương thích ngược" không có giá trị ràng buộc nào.

---

## Phụ lục — Vì sao chuẩn bị phát hành (bump version + CHANGELOG) trên `master` trước, không sửa trên nhánh `release`?

Vì `release/lab04` phải là **một ảnh chụp của một commit đã được duyệt trên `master`**. Cụ thể:

* **"Thứ được duyệt = thứ được phát hành" (nguyên tắc SCM).** Nếu bạn sửa `__version__` và CHANGELOG
  *trên* nhánh release, thì commit chứa nội dung thực sự được phát hành **không tồn tại trong lịch sử
  của `master`** — không ai review nó, CI chưa từng chạy trên nó, và lần phát hành sau phải làm lại
  từ đầu (hoặc tệ hơn: `master` và `release/*` mang hai chuỗi phiên bản khác nhau, đúng cái xung đột
  `1.0.1` vs `1.1.0` ở Lab 05 nhưng vĩnh viễn).
* **Cắt baseline trở thành thao tác "trỏ tới", không phải thao tác "sửa".** Sau khi PR chuẩn bị phát
  hành được merge, `release/lab04` chỉ là `git switch -c release/lab04` tại một commit đã biết —
  không sinh thay đổi mới, nên baseline trùng khít với trạng thái đã duyệt.
* **Nó cho ta nguyên liệu viết CHANGELOG.** Chính vì mọi thay đổi đều đã nằm trên `master` theo thứ
  tự thời gian, lệnh
  `git log --oneline --no-merges origin/release/lab01..master` trả về **đúng** danh sách những gì
  đã thay đổi kể từ baseline trước — đó là bản nháp của mục `[1.0.0]`. Nếu bạn sửa trực tiếp trên
  nhánh release, danh sách này sẽ thiếu chính những thay đổi đó.
* **Bảo vệ `release/*` không cản trở gì.** Rule trên `release/*` bật "Require a pull request" và
  "không force push / không xoá"; nhánh vẫn nhận commit qua PR khi cần (hotfix ở Lab 05). Việc chuẩn bị
  trên `master` giúp nhánh release giữ đúng vai trò: **dòng bảo trì**, không phải nơi phát triển.

## Phụ lục — Tag và nhánh release khác nhau ở đâu?

| | Tag `v1.0.0` | Nhánh `release/lab04` |
|---|---|---|
| Bản chất | con trỏ **bất biến** tới một commit | con trỏ **di động** |
| Di chuyển được không | Không bao giờ (đã chia sẻ ⇒ không xoá, không tạo lại) | Có (khi hotfix) |
| `git push` có tự đẩy không | **Không** — phải `git push origin v1.0.0` | Có (theo `git push` của nhánh) |
| Vai trò | định danh **chính xác** một phiên bản (nguyên liệu cho Configuration Audit) | dòng bảo trì của bản phát hành |

Vì tag không tự đi theo `git push`, sau khi tạo annotated tag phải đẩy riêng — và vì tag đã chia sẻ
thì không được xoá/di chuyển, nên phải kiểm tra kỹ trước khi push (`git tag -n`, `git show v1.0.0`).
