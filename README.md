# AIMS-mini — IT3180

Bài thực hành **Quản lý cấu hình phần mềm với Git & GitHub** (chuỗi Lab 01–05) — học phần IT3180,
Trường Công nghệ Thông tin và Truyền thông, Đại học Bách khoa Hà Nội.

- Sinh viên: **Tô Quang Thịnh** — MSSV **202416617**
- Repository: `it3180-202416617-aims` (public)
- Dự án mẫu: **AIMS-mini** — ứng dụng dòng lệnh Python mô phỏng một cửa hàng bán đĩa DVD,
  chỉ dùng thư viện chuẩn, kiểm thử bằng `unittest`.

---

## 📌 Câu trả lời câu hỏi thảo luận (Lab 01–05)

Đây là phần **bắt buộc của bài nộp**: các câu hỏi thảo luận ở cuối mỗi bài và các "câu hỏi nhanh"
trong bài đều được trả lời trong `docs/`, và **mỗi tệp được đưa vào `master` qua một Pull Request**
theo đúng yêu cầu của học phần.

| Lab | Nội dung thảo luận | Tệp trả lời | Đưa vào qua PR |
|---|---|---|---|
| **Lab 01** — Thiết lập môi trường & Refactor flow | `--global` lưu ở đâu, khác gì `--local` · vì sao dùng `git mv` · `release/lab01` có phải baseline · vì sao không commit thẳng `master` dù làm một mình | **[`docs/answers-lab01.md`](docs/answers-lab01.md)** | `topic/lab01-answers` |
| **Lab 02** — Feature/Topic flow & Pull Request | vì sao phải đồng bộ `master` trước khi PR · khi nào **không** được rebase · `feature/*` khác `topic/*` ra sao · *(phụ lục)* so sánh 3 kiểu merge | **[`docs/answers-lab02.md`](docs/answers-lab02.md)** | `topic/lab02-answers` |
| **Lab 03** — Bugfix flow, xung đột & hoàn tác | **merge base** là gì · vì sao `master`/`release/*` phải dùng `revert` | **[`docs/answers-lab03.md`](docs/answers-lab03.md)** | `topic/lab03-answers` |
| **Lab 04** — Release flow & phiên bản phát hành | vì sao `release/*` không merge ngược vào `master` · so sánh với GitFlow · vì sao lên `1.0.0` mà không phải `0.4.0` · *(phụ lục)* chuẩn bị phát hành trên `master`; tag vs nhánh release | **[`docs/answers-lab04.md`](docs/answers-lab04.md)** | `topic/lab04-answers` |
| **Lab 05** — Hotfix flow & bảo trì nhiều phiên bản | ưu/nhược điểm **upstream first** vs **release first** · lệnh nào ở Phần F phát hiện việc quên lan truyền · vì sao chưa gắn tag `v1.1.0` ở Phần A · vì sao không merge cả nhánh hotfix vào `master` và vì sao tách commit sửa lỗi khỏi commit bump version · *(phụ lục)* CI & AI trong CI/CD | **[`docs/answers-lab05.md`](docs/answers-lab05.md)** | `topic/lab05-answers` |

> Tài liệu kèm theo: [`docs/use-case.md`](docs/use-case.md) (sơ đồ & đặc tả use case AIMS-mini, Lab 02)
> và [`docs/submission-report.md`](docs/submission-report.md) (báo cáo tổng hợp: PR, tag, kết quả kiểm thử,
> các lệnh kiểm toán và những điểm còn hạn chế).

---

## Chức năng

- Quản lý DVD (`DigitalVideoDisc`) và giỏ hàng (`Cart`) — **tối đa 20 đĩa** (`MAX_NUMBERS_ORDERED`).
- Tính tổng tiền (`total_cost`), áp dụng giảm giá có kiểm tra hợp lệ (`total_cost_with_discount`).
- In nội dung giỏ hàng (`print_cart`) — in `The cart is empty` khi giỏ trống.
- Sắp xếp giỏ hàng (`sort_by_title`, `sort_by_cost`).
- Tìm DVD theo tiêu đề (`search_by_title`) và theo thể loại (`search_by_category`) —
  **không phân biệt chữ hoa/chữ thường**.

## Yêu cầu & cách chạy

- Python **≥ 3.10** (CI dùng 3.12). Không cần cài thư viện ngoài.
- Trên Fedora không có lệnh `python`, dùng `python3`.

```bash
git clone git@github.com:loegaire/it3180-202416617-aims.git
cd it3180-202416617-aims
python3 main.py
```

Kết quả mong đợi (dùng để kiểm tra nhanh sau mỗi thay đổi):

```
AIMS-mini v1.1.0
...
1. DVD - The Lion King - Animation - 19.95 $
2. DVD - Star Wars - Science Fiction - 24.95 $
3. DVD - Blade Runner - Science Fiction - 18.99 $
Total cost: 63.89 $
```

## Kiểm thử

```bash
python3 -m unittest discover -s tests -v     # 8 test, chạy từ thư mục gốc repo
```

Từ Lab 05, GitHub Actions chạy đúng bộ test này cho mọi `push` vào `master` và mọi Pull Request
nhắm tới `master` / `release/**` (`.github/workflows/ci.yml`, check tên `test`).
Trên `master`, check này là **bắt buộc** ("Require status checks to pass").

---

## Quy trình nhánh (Release Flow)

| Nhánh | Đặt tên | Tạo từ | Merge vào | Mục đích |
|---|---|---|---|---|
| feature / topic | `feature/<tên>`, `topic/<mô-tả>` | `master` | `master` | tính năng / chủ đề công việc |
| bugfix | `bugfix/<mô-tả>` | `master` / `feature/*` | `master` / `feature/*` | sửa lỗi khi phát triển |
| refactor | `refactor/<mô-tả>` | `master` | `master` | tái cấu trúc |
| release | `release/labXX` | `master` | **không** | baseline nộp bài |
| hotfix | `hotfix/<mô-tả>` | `release/*` | `release/*` **và** `master` (cherry-pick) | sửa bài đã nộp |

Nguyên tắc được **thực thi bằng branch protection**, không chỉ bằng quy ước:

- `master`: *Require a pull request before merging* (0 approval vì làm một mình — vẫn bắt buộc đi qua PR),
  *Dismiss stale approvals when new commits are pushed*, *Require status checks to pass* (`test`),
  *Do not allow bypassing* (kể cả admin), cấm force-push và cấm xoá nhánh.
- `release/*`: cấu hình tương tự (rule dạng mẫu nhánh), cấm force-push và cấm xoá.

Không commit trực tiếp lên `master` và `release/*` — thử push thẳng sẽ bị GitHub từ chối:

```
$ git push
remote: error: GH006: Protected branch update failed for refs/heads/master.
remote: - Changes must be made through a pull request.
```

## Các mốc thực hành: nhánh nộp bài & tag

| Lab | Nhánh nộp bài | Tag | Nội dung chính | PR tiêu biểu |
|---|---|---|---|---|
| 01 | `release/lab01` | `v0.1.0` | Cài đặt, commit đầu tiên, `git mv` vào gói `aims/`, PR đầu tiên | `refactor/apply-release-flow`, `topic/lab01-answers` |
| 02 | `release/lab02` | `v0.2.0` | Branch protection, PR template, review có yêu cầu sửa, 3 kiểu merge | `topic/pr-template`, `feature/cart-print`, `feature/search-by-title` (squash), `topic/use-case-diagram` (rebase) |
| 03 | `release/lab03` | `v0.3.0` | Issue ⇄ nhánh ⇄ commit ⇄ PR, regression test fail-trước-fix-sau, xung đột & `revert` | `bugfix/cart-limit-off-by-one`, `bugfix/discount-calculation`, `feature/show-added-title`, `bugfix/revert-show-added-title` |
| 04 | `release/lab04` | `v1.0.0` | SemVer, CHANGELOG, annotated tag, GitHub Release, status accounting, kiểm toán baseline | `topic/prepare-release-1.0.0`, `feature/sort-cart` |
| 05 | `release/lab05` | `v1.1.0` | Hotfix từ `release/lab04`, phát hành `v1.0.1`, lan truyền bằng `cherry-pick -x`, CI chặn lỗi | `hotfix/search-case-insensitive`, `hotfix/search-case-insensitive-master`, `hotfix/search-case-insensitive-lab05`, `topic/ci-unit-tests` |

GitHub Release `v1.0.0` được tạo từ tag có sẵn, target `release/lab04`.

## Cấu trúc repository

```
.
├── .github/
│   ├── pull_request_template.md   # template mô tả PR (Lab 02)
│   └── workflows/ci.yml           # CI: chạy unittest cho push/PR (Lab 05)
├── aims/
│   ├── __init__.py                # __version__
│   ├── cart.py                    # Cart: add_dvd, total_cost, giảm giá, in giỏ, sắp xếp
│   ├── dvd.py                     # DigitalVideoDisc
│   └── search.py                  # search_by_title, search_by_category
├── docs/
│   ├── answers-lab01.md … answers-lab05.md   # câu trả lời thảo luận
│   ├── submission-report.md       # báo cáo & bằng chứng
│   └── use-case.md                # sơ đồ & đặc tả use case
├── tests/
│   ├── test_cart.py               # regression test giới hạn 20 đĩa
│   ├── test_cart_sort.py
│   ├── test_category_search.py
│   ├── test_discount.py
│   └── test_search.py             # gồm test tìm kiếm không phân biệt hoa/thường
├── .gitattributes
├── .gitignore
├── CHANGELOG.md                   # Keep a Changelog + SemVer
├── main.py
└── README.md
```

## Quy ước commit & Pull Request

Conventional Commits: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `ci`.
Tiêu đề ≤ 50 ký tự, thể mệnh lệnh; phần thân giải thích **vì sao**; từ khoá `Fixes #N` để tự đóng Issue
(dùng `Refs #N` khi bản vá chỉ vào `release/*`, vì từ khoá đóng Issue chỉ có hiệu lực khi merge vào
nhánh mặc định). Mọi PR đều dùng `.github/pull_request_template.md` (Mục đích · Thay đổi · Cách kiểm thử · Checklist).

## Báo cáo và bằng chứng

Xem **[`docs/submission-report.md`](docs/submission-report.md)** để có: danh sách Pull Request và Issue,
các tag/GitHub Release, kết quả kiểm thử và CI, các lệnh status accounting / kiểm toán đã chạy,
cùng **hai điểm bất thường đã gặp và cách xử lý** (một tệp bị `git commit -am` bỏ sót khi chuẩn bị
baseline 1.0.0, và hệ quả của nó đối với `git describe`).
