# Báo cáo thực hành — AIMS-mini (IT3180, MSSV 202416617)

Sinh viên: **Tô Quang Thịnh** — MSSV **202416617** · Repository: `it3180-202416617-aims` (public)

Tài liệu này tổng hợp bằng chứng cho chuỗi **Lab 01–05** (Quản lý cấu hình phần mềm với Git & GitHub).
Các câu trả lời thảo luận nằm trong `docs/answers-lab01.md` … `docs/answers-lab05.md`
(xem bảng liên kết ở [README](../README.md#-câu-trả-lời-câu-hỏi-thảo-luận-lab-01-05)).

---

## 1. Tổng quan

| Hạng mục | Giá trị |
|---|---|
| Nhánh mặc định | `master` |
| Số Pull Request | **29** (đã merge: 28) |
| Số Issue | **3** (đã đóng: 3, đóng tự động bằng `Fixes #N`) |
| Tag annotated | `v0.1.0`, `v0.2.0`, `v0.3.0`, `v1.0.0`, `v1.0.1`, `v1.1.0` |
| GitHub Release | `v1.0.0` (target `release/lab04`) |
| Số nhánh trên remote | 6 |
| Kiểm thử trên `master` | `Ran 8 tests in 0.000s | OK` |
| CI | GitHub Actions, workflow `CI`, check tên `test` — **bắt buộc** với `master` |

Branch protection đang áp dụng:

```
master     : {"deletion":false,"dismiss_stale":true,"enforce_admins":true,"force_push":false,"required_checks":["test"],"reviews":0,"strict":false}
release/*  : {"data":{"repository":{"branchProtectionRules":{"nodes":[{"pattern":"release/*","requiredApprovingReviewCount":0,"dismissesStaleReviews":true,"isAdminEnforced":true,"allowsForcePushes":false,"allowsDeletions":false},{"pattern":"master","requiredApprovingReviewCount":0,"dismissesStaleReviews":true,"isAdminEnforced":true,"allowsForcePushes":false,"allowsDeletions":false}]}}}}
```

Thực nghiệm kiểm chứng checklist Lab 04 — tạo một commit rỗng trên dòng bảo trì rồi push trực tiếp:

```
$ git switch release/lab04 && git commit --allow-empty -m "chore: test release branch protection"
$ git push
remote: error: GH006: Protected branch update failed for refs/heads/release/lab04.
remote: - Changes must be made through a pull request.
 ! [remote rejected]  release/lab04 -> release/lab04 (protected branch hook declined)
```

Sau khi kiểm chứng, nhánh được trả về đúng commit trên remote (`git reset --hard origin/release/lab04`)
nên baseline không bị thay đổi.

## 2. Nhánh nộp bài & tag

| Lab | Nhánh nộp bài | Tag | Tệp trả lời thảo luận |
|---|---|---|---|
| 01 | `release/lab01` | `v0.1.0` | `docs/answers-lab01.md` |
| 02 | `release/lab02` | `v0.2.0` | `docs/answers-lab02.md` |
| 03 | `release/lab03` | `v0.3.0` | `docs/answers-lab03.md` |
| 04 | `release/lab04` | `v1.0.0` (+ `v1.0.1` bản vá) | `docs/answers-lab04.md` |
| 05 | `release/lab05` | `v1.1.0` | `docs/answers-lab05.md` |

`git tag -n`:

```
v0.1.0          Lab 01 release
v0.2.0          Lab 02 release
v0.3.0          Lab 03 release
v1.0.0          AIMS-mini 1.0.0 - Lab 04 release
v1.0.1          AIMS-mini 1.0.1 - hotfix search_by_title
v1.1.0          AIMS-mini 1.1.0 - Lab 05 release
```

Các tag annotated: `master` `release/lab01` `release/lab02` `release/lab03` `release/lab04` `release/lab05`

## 3. Pull Request

| PR | Nhánh → base | Tiêu đề | Trạng thái | Merge commit |
|---|---|---|---|---|
| #1 | `refactor/apply-release-flow` → `master` | refactor: move sources into aims package | MERGED | `cb64178` |
| #2 | `topic/lab01-answers` → `master` | docs: add lab 01 discussion answers | MERGED | `3ef3c3d` |
| #3 | `topic/pr-template` → `master` | docs: add pull request template | MERGED | `171f7dd` |
| #4 | `feature/cart-print` → `master` | feat: add print_cart to Cart | MERGED | `b3c4985` |
| #5 | `feature/search-by-title` → `master` | feat: add search_by_title | MERGED | `e1801c7` |
| #6 | `topic/use-case-diagram` → `master` | docs: add use case diagram | MERGED | `f32f8bf` |
| #7 | `topic/lab02-answers` → `master` | docs: add lab 02 discussion answers | MERGED | `c7edc57` |
| #9 | `bugfix/cart-limit-off-by-one` → `master` | fix: reject DVDs beyond MAX_NUMBERS_ORDERED | MERGED | `8ba15cf` |
| #11 | `bugfix/discount-calculation` → `feature/discount` | fix: return discounted total and validate percent | MERGED | `b0e0673` |
| #12 | `feature/discount` → `master` | feat: add validated cart discounts | MERGED | `b146f61` |
| #13 | `topic/search-test` → `master` | test: cover search_by_title | MERGED | `db540dc` |
| #14 | `feature/vietnamese-messages` → `master` | feat: use Vietnamese message when adding a disc | MERGED | `5290f3d` |
| #15 | `feature/show-added-title` → `master` | feat: show disc title when adding to cart | MERGED | `91ea0e5` |
| #16 | `bugfix/revert-show-added-title` → `master` | revert: undo the show-added-title merge | MERGED | `95f2f81` |
| #17 | `topic/lab03-answers` → `master` | docs: add lab 03 discussion answers | MERGED | `12ec7e5` |
| #18 | `topic/prepare-release-1.0.0` → `master` | chore: prepare release 1.0.0 | MERGED | `55f8588` |
| #19 | `feature/sort-cart` → `master` | feat: add sort_by_title and sort_by_cost to Cart | MERGED | `32bf8c3` |
| #20 | `topic/changelog-1.0.0-release` → `release/lab04` | docs: add CHANGELOG.md to the 1.0.0 baseline | MERGED | `85222ca` |
| #21 | `topic/lab04-answers` → `master` | docs: add lab 04 discussion answers | MERGED | `d3f4bf0` |
| #22 | `feature/search-by-category` → `master` | feat: add search_by_category | MERGED | `74c2cfb` |
| #23 | `topic/prepare-release-1.1.0` → `master` | chore: prepare release 1.1.0 | MERGED | `9e60812` |
| #25 | `hotfix/search-case-insensitive` → `release/lab04` | fix: make search_by_title case-insensitive | MERGED | `b8ceefb` |
| #26 | `hotfix/search-case-insensitive-master` → `master` | fix: make search_by_title case-insensitive | MERGED | `8ae1162` |
| #27 | `hotfix/search-case-insensitive-lab05` → `release/lab05` | fix: make search_by_title case-insensitive | MERGED | `454c341` |
| #28 | `topic/ci-unit-tests` → `master` | ci: run unit tests on pull requests | MERGED | `ebd97c4` |
| #29 | `bugfix/ci-demo` → `master` | fix: make total_cost faster (demo CI) | CLOSED | `—` |
| #30 | `topic/lab05-answers` → `master` | docs: add lab 05 discussion answers | MERGED | `3702805` |
| #31 | `topic/sync-lab05-docs` → `release/lab05` | docs: add lab 05 discussion answers to release/lab05 | MERGED | `f72cbe2` |
| #32 | `topic/final-readme` → `master` | docs: rewrite README with lab answers and flow overview | MERGED | `be111e9` |

Cả **ba kiểu merge** đều được dùng thật trên `master`:
PR `feature/cart-print` (Merge commit, giữ 3 commit của vòng review),
PR `feature/search-by-title` (**Squash** → 1 commit `feat: add search_by_title (#5)`),
PR `topic/use-case-diagram` (**Rebase** → lịch sử tuyến tính, SHA mới).
Kiểm chứng: `git log --oneline --graph` trên `master`.

## 4. Issue (truy vết Issue ⇄ nhánh ⇄ commit ⇄ PR)

| Issue | Tiêu đề | Trạng thái |
|---|---|---|
| #8 | Cart accepts the 21st DVD although the limit is 20 | CLOSED |
| #10 | Discount calculation returns the discount amount instead of the payable total | CLOSED |
| #24 | search_by_title is case-sensitive (affects v1.0.0) | CLOSED |

Hai Issue lỗi được xử lý theo đúng vòng đời SCM: nhánh `bugfix/*` (hoặc `hotfix/*`) → commit test tái hiện
**fail trước khi sửa** → commit fix có `Fixes #N` (với hotfix thì `Refs #N` ở nhánh release và `Fixes #N`
ở PR vào `master`) → PR → merge → Issue tự đóng.

## 5. GitHub Actions (CI)

| Thời điểm | Sự kiện | Nhánh | Tiêu đề | Kết quả |
|---|---|---|---|---|
| 2026-11-07T08:19:15Z | push | `master` | Merge pull request #32 from loegaire/topic/final-readme | success |
| 2026-11-07T08:19:00Z | pull_request | `topic/final-readme` | docs: rewrite README with lab answers and flow overview | success |
| 2026-11-07T08:03:33Z | push | `master` | Merge pull request #30 from loegaire/topic/lab05-answers | success |
| 2026-11-07T07:54:51Z | pull_request | `topic/lab05-answers` | docs: add lab 05 discussion answers | success |
| 2026-11-07T07:54:31Z | pull_request | `bugfix/ci-demo` | fix: make total_cost faster (demo CI) | failure |
| 2026-11-07T07:45:50Z | push | `master` | Merge pull request #28 from loegaire/topic/ci-unit-tests | success |
| 2026-11-07T07:45:46Z | pull_request | `topic/ci-unit-tests` | ci: run unit tests on pull requests | success |

* PR `bugfix/ci-demo` (cố ý làm hỏng `total_cost`) → CI **failure** ⇒ `mergeStateStatus = BLOCKED`,
  merge thủ công bị từ chối: *"the base branch policy prohibits the merge"*. PR đã được **đóng, không merge**.
* Mọi PR hợp lệ sau đó đều phải có check `test` **xanh** mới merge được (bắt buộc bởi branch protection).

## 6. Status accounting & kiểm toán cấu hình (Lab 04–05)

```
$ git log --oneline --no-merges v0.3.0..v1.0.0          # nguyên liệu CHANGELOG 1.0.0
bf8d296 docs: add CHANGELOG.md to the 1.0.0 baseline
478ce2c chore: prepare release 1.0.0

$ git log --oneline release/lab04..master               # master đi trước baseline những commit nào
be111e9 Merge pull request #32 from loegaire/topic/final-readme
96a24fc docs: rewrite README with lab answers and flow overview
3702805 Merge pull request #30 from loegaire/topic/lab05-answers
d7d1f77 docs: add lab 05 discussion answers
ebd97c4 Merge pull request #28 from loegaire/topic/ci-unit-tests
f5eaa3d ci: run unit tests on pull requests
8ae1162 Merge pull request #26 from loegaire/hotfix/search-case-insensitive-master
d7c87bd docs: add 1.0.1 to changelog
a4325fe fix: make search_by_title case-insensitive
9e60812 Merge pull request #23 from loegaire/topic/prepare-release-1.1.0
8a9dd62 chore: prepare release 1.1.0
74c2cfb Merge pull request #22 from loegaire/feature/search-by-category
42ce3eb feat: add search_by_category
d3f4bf0 Merge pull request #21 from loegaire/topic/lab04-answers
af7e190 docs: add lab 04 discussion answers
32bf8c3 Merge pull request #19 from loegaire/feature/sort-cart
be95d2e feat: add sort_by_title and sort_by_cost to Cart

$ git diff --stat v0.3.0 v1.0.0
CHANGELOG.md     | 21 +++++++++++++++++++++
 aims/__init__.py |  2 ++
 main.py          |  3 +++
 3 files changed, 26 insertions(+)

$ git diff --stat v1.0.0 v1.0.1                         # một bản PATCH chỉ 4 tệp
CHANGELOG.md         |  8 ++++++++
 aims/__init__.py     |  2 +-
 aims/search.py       |  4 ++--
 tests/test_search.py | 10 ++++++++++
 4 files changed, 21 insertions(+), 3 deletions(-)

$ git describe --tags
v0.3.0-19-gbe111e9

$ git ls-tree -r --name-only v1.0.0                     # không có tệp rác
.gitattributes
.github/pull_request_template.md
.gitignore
CHANGELOG.md
README.md
aims/__init__.py
aims/cart.py
aims/dvd.py
aims/search.py
docs/answers-lab01.md
docs/answers-lab02.md
docs/answers-lab03.md
docs/use-case.md
main.py
tests/test_cart.py
tests/test_discount.py
tests/test_search.py
$ (tệp rác) (không có tệp rác)
```

Kiểm toán đa phiên bản của hotfix (Lab 05, Phần F):

```
$ git log --all --oneline --grep "cherry picked from commit c1e538dd97a54c64c264c6fa070ee8341de692af"
d3e72f6 fix: make search_by_title case-insensitive
a4325fe fix: make search_by_title case-insensitive          # 2 bản cherry-pick: master và release/lab05

$ git tag --contains c1e538dd97a54c64c264c6fa070ee8341de692af
v1.0.1          # commit gốc chỉ nằm trên dòng 1.0.x

$ git cherry -v origin/master origin/release/lab04
+ bf8d29651f92b9e897383b28a195a7c4d9c1f9e6 docs: add CHANGELOG.md to the 1.0.0 baseline
- c1e538dd97a54c64c264c6fa070ee8341de692af fix: make search_by_title case-insensitive
+ 5291f7f76a25cffbb789d161566d11a68abdedfb chore: bump version to 1.0.1
# '-' = master đã có bản tương đương (nhờ cherry-pick)
# '+' = commit chỉ thuộc dòng 1.0.x (đúng chủ đích: bump 1.0.1, CHANGELOG của dòng bảo trì)
```

Kiểm tra hành vi trên cả ba dòng phiên bản — kết quả **1 / 1 / 1**:

```
$ for ref in v1.0.1 v1.1.0 master; do git switch --detach -q $ref; ...; done
v1.0.1   1
v1.1.0   1
master   1
```

Tái tạo phiên bản cũ (Configuration Audit):
`git switch --detach v0.2.0 && python3 main.py` → `Total cost: 63.89 $`;
`git worktree add ../aims-v1.0.0 v1.0.0` → 4 test OK; `git archive --format=zip --prefix=aims-1.0.0/ -o ../aims-1.0.0.zip v1.0.0`.

## 7. Việc đã làm, và điều học được từ hai sai sót thật

**Đã làm:** 5 nhánh `release/labXX` (baseline nộp bài, tag tương ứng), 6 tag annotated, 1 GitHub Release,
29 PR (có PR review với comment trên dòng `def print_cart:` và yêu cầu sửa trước khi merge),
3 Issue, xung đột được tạo và giải quyết thật (giữ cả hai ý đồ), một PR `revert` cho lịch sử đã chia sẻ,
hotfix được lan truyền bằng `cherry-pick -x` sang hai dòng phiên bản, CI bắt buộc cho `master`.

**Sai sót 1 — `git commit -am` bỏ sót tệp mới.** Commit chuẩn bị phát hành dùng `git commit -am`, mà `-a`
chỉ gom các tệp **đã được track**; `CHANGELOG.md` khi đó còn là tệp mới nên **không** vào commit ⇒
baseline `v1.0.0` ban đầu thiếu CHANGELOG. Phát hiện bằng chính lệnh kiểm toán
(`git show v1.0.0:CHANGELOG.md` báo lỗi). Vì tag chưa được công bố/dùng ở đâu (mới tạo trong cùng buổi),
cách xử lý là **sửa tiến, không viết lại lịch sử**: thêm `CHANGELOG.md` bằng một PR vào chính `release/lab04`
(`topic/changelog-1.0.0-release`), rồi tạo lại tag + GitHub Release tại đầu nhánh đã đầy đủ.
Từ đó về sau, mọi commit dùng `git add` tường minh hoặc `git add -A`.
*Bài học:* `-a` ≠ `-A`; và một baseline phải được kiểm toán (`git show <tag>:<file>`) ngay sau khi tạo.

**Sai sót 2 (hệ quả của cách sửa ở trên).** Vì `release/lab04` nhận thêm một commit tài liệu mà `master`
không có, tag `v1.0.0` **không còn là cha của `master`**, nên `git describe --tags` trên `master`
trả về `v0.3.0-…` thay vì `v1.0.0-…`, và `git log master..release/lab04` khác rỗng. Đây là minh hoạ thật
cho khác biệt **tag bất biến** vs **nhánh bảo trì di động**: tag định danh đúng *nội dung* 1.0.0,
còn nhánh release có thể còn nhận commit (tài liệu, bản vá) sau khi đã cắt.

**Hạn chế của bài nộp.** Làm một mình nên `Require approvals = 0` (đúng như hướng dẫn: "làm một mình: 0"),
do đó **không** có approval thật của partner: GitHub chặn tự approve
(*"Review Can not request changes on your own pull request"* / *"Can not approve your own pull request"*),
nên vòng review được thực hiện bằng review dạng **COMMENT** kèm comment đúng dòng code trong `Files changed`
(ngoài ra review tự động của GitHub Copilot cũng xuất hiện trên PR). Repo là public nên branch protection
dùng được ngay trên GitHub Free.
