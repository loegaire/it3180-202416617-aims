# Lab 05 — Câu hỏi thảo luận

Nhánh nộp bài: `release/lab05` (tag `v1.1.0`), dòng bảo trì `release/lab04` nhận tag `v1.0.1`.
Bản vá `search_by_title()` không phân biệt chữ hoa/thường được tạo trên `hotfix/search-case-insensitive`
(từ `release/lab04`) rồi lan truyền sang `master` và `release/lab05` bằng `git cherry-pick -x`.

---

## 1. Ưu, nhược điểm của *upstream first* so với *release first*?

| | **Release first** (học phần) | **Upstream first** (Microsoft) |
|---|---|---|
| Nhánh hotfix tạo từ | `release/*` — dòng **đã phát hành** | `master` — dòng **nguồn** |
| Sửa và kiểm thử trên | đúng artifact đã phát hành (v1.0.0) | mã mới nhất trên `master` |
| Cách lan truyền | `cherry-pick` **lên** `master` và sang các dòng release khác | `cherry-pick` **xuống** các dòng `release/*` bị ảnh hưởng |
| Chiều của sự thật | mỗi dòng tự sửa, `master` nhận bản sao | `master` là nơi duy nhất sửa, các dòng nhận bản sao |

**Release first — ưu điểm**

* **Tái hiện và sửa trên đúng thứ đã hỏng.** Lỗi được báo trên `v1.0.0`; sửa trên `v1.0.0` loại bỏ
  hẳn lớp rủi ro "chạy được trên master nhưng vẫn hỏng trên bản phát hành" (do API mới, do hành vi
  khác đi sau này). Diff nhỏ và dễ review: chỉ 4 tệp, không lẫn tính năng mới.
* **Phát hành bản vá ngay, không phụ thuộc `master`.** Trong Lab 05, `master` đang chuẩn bị `1.1.0`
  (có `search_by_category`, có `sort_*`). Nếu buộc phải sửa trên `master` rồi mới đóng gói `1.0.1`,
  ta sẽ phải tạm dừng/ổn định `master` — điều không thể khi `1.1.0` đang dở. Release first cắt đứt
  phụ thuộc đó: dòng 1.0.x có bản vá riêng, phát hành riêng.
* **An toàn cho người dùng dòng cũ.** Người dùng `1.0.0` nhận `1.0.1` với thay đổi tối thiểu, đúng
  nghĩa PATCH; không bị kéo theo tính năng mới (đúng nguyên tắc SemVer).

**Release first — nhược điểm**

* **Phải nhớ lan truyền.** Bản sửa nằm trên một dòng phụ trước, nên `master` (và mọi dòng release
  khác) chỉ có nó nếu ta chủ động `cherry-pick`. Quên ⇒ lỗi tái xuất hiện trong bản phát hành sau.
  Đây là rủi ro *lớn nhất* và cũng là lý do phải có phần kiểm toán (câu 2 dưới đây).
* **Chi phí cherry-pick gia tăng.** Số dòng bảo trì song song càng nhiều thì càng nhiều lần
  cherry-pick, càng nhiều SHA khác nhau cho cùng một nội dung ⇒ khó trả lời "bản sửa này đã có ở
  mọi dòng chưa?" nếu không có quy ước (`-x` + `git cherry` + `git tag --contains`).
* **Nguy cơ phân kỳ.** Nếu sau này `master` có cách sửa khác cho cùng lỗi, hai "bản sửa" cùng tồn tại
  và dễ xung đột về hành vi.

**Upstream first — ưu điểm**

* **Một nơi sửa duy nhất.** Sửa trên `master` rồi rải xuống ⇒ không bao giờ có chuyện "quên sửa ở
  dòng chính"; chiều lan truyền chỉ còn một hướng (xuống).
* **Sửa trên mã mới nhất.** Bản sửa không bị "lỗi thời ngay" sau khi `master` đổi; chỉ cần một lần
  review, một lần CI chạy toàn bộ test suite trên mã mới.
* **Không chặn `master`.** `master` vẫn là dòng tích hợp thật; không sinh nhánh phụ chứa mã của bản
  phát hành cũ.

**Upstream first — nhược điểm**

* **Bản vá bị chặn bởi trạng thái `master`.** Nếu `master` đang giữa một thay đổi lớn/chưa xanh test,
  không thể phát hành hotfix — không chấp nhận được với lỗi nghiêm trọng trên production.
* **Kiểm thử sai đối tượng.** Test đầu tiên chạy trên `master` (khác bản phát hành), nên vẫn phải
  cherry-pick xuống rồi chạy lại trên dòng cũ ⇒ thực chất *vẫn phải* kiểm thử hai lần.
* **Cherry-pick xuống nhiều dòng vẫn phải làm, và dễ xung đột hơn** vì bản sửa được viết dựa trên mã
  mới (ví dụ bản sửa dùng một hàm chỉ có trên `master`).

**Kết luận có lập luận.** Hai mô hình tối ưu cho hai mục tiêu khác nhau: *release first* tối ưu cho
"phát hành ngay, đúng thứ đã hỏng, thay đổi tối thiểu"; *upstream first* tối ưu cho "chỉ sửa ở một nơi,
không bao giờ quên". Trong học phần, các bản nộp là baseline theo tuần và **nhiều dòng tồn tại song song**
(nộp Lab 04 xong vẫn phải giữ để nhận hotfix), lỗi lại được phát hiện *trên bản đã phát hành*, nên
release-first là lựa chọn đúng. Cách giảm nhược điểm của release-first — và cũng là điều bài này làm —
là **chuẩn hóa quy trình lan truyền**: tách commit sửa lỗi khỏi commit bump version, dùng
`git cherry-pick -x` để lưu lại nguồn gốc, rồi kiểm toán bằng `git log --grep` + `git cherry` +
`git tag --contains` + kiểm tra hành vi trên cả ba dòng phiên bản.

---

## 2. Nếu quên lan truyền bản sửa sang `release/lab05`, lệnh nào ở Phần F sẽ phát hiện?

**Lệnh phát hiện trực tiếp:**

```
$ git log --all --oneline --grep "cherry picked from commit <FIX_SHA>"
```

Vì `git cherry-pick -x` **ghi lại nguồn gốc** vào cuối commit message
(`(cherry picked from commit <FIX_SHA>)`), nên mỗi lần lan truyền thành công sinh **đúng một dòng**
chứa chuỗi đó. Kỳ vọng của Phần F là **2 dòng** — một cho `master`
(`hotfix/search-case-insensitive-master`) và một cho `release/lab05`
(`hotfix/search-case-insensitive-lab05`) — vì bản trên `release/lab04` là **commit gốc**, không phải
cherry-pick. Nếu quên `release/lab05`, lệnh chỉ trả về **1 dòng** ⇒ phát hiện ngay.

Hai lệnh còn lại là các chốt kiểm tra bổ trợ, mỗi lệnh bắt một loại sai khác nhau:

| Lệnh | Kỳ vọng | Nếu quên lab05 |
|---|---|---|
| `git log --all --oneline --grep "cherry picked from commit <FIX_SHA>"` | **2** dòng (master + lab05) | chỉ **1** dòng → *bắt trực tiếp* |
| `git tag --contains <FIX_SHA>` | `v1.0.1` | vẫn `v1.0.1` — **không** bắt được, vì cherry-pick tạo SHA mới, tag `v1.1.0` chứa *bản sao* chứ không chứa `<FIX_SHA>` |
| `git cherry -v origin/master origin/release/lab04` | dấu `-` cho commit sửa lỗi (master đã có bản tương đương), dấu `+` cho commit bump version (chưa có, đúng chủ đích) | không đổi — đây là kiểm tra *nội dung đã lan truyền*, không kiểm tra *đích đến* |
| Vòng lặp hành vi `for ref in v1.0.1 v1.1.0 master; do ... print(len(search_by_title([D('The Lion King')], 'lion')))` | `1`, `1`, `1` | `v1.1.0` in **0** → *bắt được bằng hành vi* |

Vậy: chỉ huy **`git log --all --grep`** (số dòng cherry-pick) là lệnh trả lời trực tiếp câu hỏi
"đã lan truyền tới **những dòng nào**"; còn vòng lặp kiểm tra hành vi là lưới an toàn cuối cùng vì nó
kiểm chứng *triệu chứng* chứ không kiểm chứng *lịch sử*. Cách đúng là dùng cả hai: grep để biết
"đã làm chưa", vòng lặp để biết "có thật sự chạy đúng không".

---

## 3. Vì sao ở Phần A chưa gắn tag `v1.1.0`?

Vì **cắt nhánh release chưa phải là phát hành**. Ở Phần A, `release/lab05` được tạo từ `master` để
chuẩn bị nộp bài — nhưng **chưa ai biết là còn phải vá gì**. Tag là con trỏ **bất biến**: một khi đã
`git push` tag đi, bạn không được xoá và không được tạo lại (`git push origin <tag>` sẽ báo
`tag 'v1.1.0' already exists`). Hai hệ quả:

1. Nếu tag `v1.1.0` ngay ở Phần A, rồi Phần B–E phát hiện lỗi và đưa bản sửa vào `release/lab05`,
   thì nội dung của `v1.1.0` đã đổi **sau khi công bố** — tag trỏ vào commit cũ không còn là nội dung
   thật. Muốn công bố bản có bản sửa, bạn buộc phải phát hành **`v1.1.1`**, tức "phiên bản 1.1.0" trên
   thực tế chứa lỗi mà không có bản vá nào mang số 1.1.0 đúng nghĩa.
2. Ngược lại, nhánh `release/lab05` **có thể** còn thay đổi qua PR (đó là điều đã xảy ra: PR
   `hotfix/search-case-insensitive-lab05` merge vào nó). Nhánh là dòng bảo trì — di động; tag là định
   danh — bất biến.

Nguyên tắc rút ra: **tag chỉ được tạo ở thời điểm "nội dung đã chốt"**, và luôn phải đặt câu hỏi
"còn bản vá nào đang chờ cho phiên bản này không?" trước khi tạo. Trong bài này ta cố ý chờ: tạo
`release/lab05` → nhận bản vá → **rồi mới** gắn `v1.1.0` và đẩy tag.

---

## 4. Vì sao không merge **cả nhánh** hotfix vào `master`?

Vì nhánh hotfix chứa **hai loại thay đổi khác nhau về phạm vi áp dụng**, và chỉ một loại đúng cho `master`:

* **Commit 1 — `fix: make search_by_title case-insensitive`**: đúng cho *mọi* dòng (đây là lỗi mã nguồn).
* **Commit 2 — `chore: bump version to 1.0.1`** (+ mục `[1.0.1]` trong CHANGELOG): chỉ đúng cho *dòng 1.0.x*.

`master` lúc này đã ở `1.1.0`, nên đưa commit 2 vào là **sai về mặt ngữ nghĩa phiên bản** và làm phát
sinh xung đột — đúng như thông báo GitHub khi so sánh:

```
compare/master...hotfix/search-case-insensitive
→ "Can't automatically merge": commit 2 đặt 1.0.1, xung đột với 1.1.0 trên master
```

Về mặt kỹ thuật, merge cả nhánh **không thể** thực hiện sạch (xung đột ở `aims/__init__.py` và
`CHANGELOG.md`), và nếu cố giải quyết thì kết quả là `master` bị "hạ" phiên bản hoặc CHANGELOG bị
sai thứ tự. Cách đúng là tạo một nhánh mới **từ `master`** và **`git cherry-pick -x <FIX_SHA>`** —
chỉ mang theo *mã sửa lỗi*, để lại phần bookkeeping của dòng 1.0.x ở đúng chỗ của nó.

**Vì sao lại tách commit sửa lỗi khỏi commit bump version ngay từ đầu?**
Vì `cherry-pick` hoạt động **theo từng commit**, không theo "phần thay đổi". Nếu gộp chung một commit,
việc lan truyền bản sửa buộc phải mang luôn cả thao tác bump `1.0.1` sang `master` — tạo xung đột với
`1.1.0` và/hoặc ghi sai số phiên bản. Tách ra thì:

* phần cần lan truyền (`FIX_SHA`) là một commit *nguyên tử*, đi được tới mọi nơi một cách sạch sẽ;
* phần chỉ thuộc dòng 1.0.x (bump + CHANGELOG) ở lại đúng nơi cần nó.

Đây là nguyên tắc chung "một commit, một thay đổi logic" nhưng nhìn từ góc độ **bảo trì đa phiên bản**:
thiết kế đơn vị commit chính là thiết kế đơn vị lan truyền. Và vì ta dùng `-x`, mỗi bản sao vẫn ghi lại
nguồn gốc `(cherry picked from commit <FIX_SHA>)` — biến cherry-pick từ một thao tác "mất dấu" thành
một thao tác **truy vết được**.

---

## Phụ lục — CI cơ bản và "thứ được duyệt = thứ được tích hợp"

`.github/workflows/ci.yml` (thêm qua `topic/ci-unit-tests`) chạy
`python -m unittest discover -s tests -v` trên Python 3.12 cho mọi `push` vào `master` và mọi
`pull_request` nhắm tới `master` hoặc `release/**`. Sau đó rule của `master` được bật thêm
**Require status checks to pass** với check tên `test`.

Kiểm chứng CI thực sự **chặn** được lỗi: trên nhánh thử nghiệm `bugfix/ci-demo`, `total_cost()`
được sửa cố ý cho sai; PR tương ứng có CI **đỏ** và nút Merge ở trạng thái bị khoá
(`mergeStateStatus = BLOCKED`) — PR đó đã được **đóng, không merge**.

Điều này khép kín nguyên tắc SCM: mỗi commit trên `master` là một trạng thái **đã qua review và
đã qua kiểm thử tự động**, tức "thứ được duyệt = thứ được tích hợp = thứ được phát hành".

## Phụ lục — Bước tiếp theo: AI trong CI/CD

Luồng CI hiện tại mới tự động hóa khâu **test**. Các khâu tiếp theo có thể tích hợp AI:
sinh mã (Copilot/Codeium), review PR tự động (Snyk Code, CodeGuru), sinh test case và tìm edge case,
cập nhật dependency (Dependabot/Renovate), dự đoán build lỗi, quét lỗ hổng và secret scanning
(tham khảo *AI Infusion in Software Build and Development*). Với cấu trúc hiện tại, mỗi khâu như vậy
chỉ cần thêm một job vào `.github/workflows/` và (nếu muốn) một status check bắt buộc cho `master`.
