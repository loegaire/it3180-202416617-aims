# Lab 01 — Câu hỏi thảo luận

Nhánh nộp bài: `release/lab01`. Các thay đổi của Lab 01 đi vào `master` qua PR #1
(`refactor/apply-release-flow`); tệp trả lời này vào qua PR #2 (`topic/lab01-answers`).

---

## 1. Câu hỏi nhanh — cấu hình `--global` được lưu ở đâu? Khác gì `--local`?

`git config` có 3 tầng và mỗi tầng ghi vào một tệp khác nhau:

| Tầng | Cờ | Tệp lưu | Phạm vi |
|---|---|---|---|
| System | `--system` | `/etc/gitconfig` | mọi người dùng trên máy |
| Global | `--global` | `~/.gitconfig` (hoặc `$XDG_CONFIG_HOME/git/config`) | mọi repository của **một người dùng** |
| Local | `--local` (mặc định) | `<repo>/.git/config` | **chỉ repository hiện tại** |

Thứ tự ưu tiên khi Git đọc giá trị: **system < global < local < worktree < dòng lệnh (`git -c ...`)** —
tầng sau ghi đè tầng trước. Vì vậy cùng một khoá có thể tồn tại ở nhiều tệp, và giá trị "đang có hiệu lực"
là giá trị của tầng ưu tiên cao nhất.

Lệnh kiểm toán cấu hình (dùng `--show-origin` để biết giá trị đến từ tệp nào):

```
$ git config --list --show-origin
file:/home/thinh/.gitconfig      user.email=tquangthinh2006@gmail.com
file:/home/thinh/.gitconfig      user.name=loegaire
file:/home/thinh/.gitconfig      credential.https://github.com.helper=!/usr/bin/gh auth git-credential
file:.git/config                 core.autocrlf=input
file:.git/config                 user.name=Tô Quang Thịnh
file:.git/config                 user.email=202416617@sis.hust.edu.vn
file:.git/config                 remote.origin.url=git@github.com:loegaire/it3180-202416617-aims.git
```

Ý nghĩa thực tế trong bài này: máy vẫn giữ danh tính cá nhân ở tầng global
(`~/.gitconfig`), còn repository bài tập khai báo danh tính sinh viên ở tầng **local**
(`.git/config`) nên mọi commit của bài nộp mang đúng `Tô Quang Thịnh <202416617@sis.hust.edu.vn>`
mà không phải sửa cấu hình của cả máy. Đây cũng là một ví dụ của hoạt động
**định danh cấu hình (Configuration Identification)**: cấu hình của môi trường cũng là một CI
cần được xác định rõ nguồn.

---

## 2. Vì sao dùng `git mv`?

`git mv <nguồn> <đích>` thực chất là 2 việc gộp trong 1 lệnh: di chuyển tệp trên đĩa **và**
cập nhật luôn index (xoá đường dẫn cũ + thêm đường dẫn mới). Nếu chỉ dùng `mv` rồi quên
`git add`, index vẫn giữ tệp cũ ở trạng thái cũ và bạn rất dễ commit một trạng thái
"vừa thiếu tệp mới vừa thừa tệp cũ". `git mv` làm thao tác này thành một bước duy nhất, đọc
là hiểu ngay ý đồ "đổi tên/di chuyển", và không thể quên staged phần xoá.

Lợi ích quan sát được trong bài:

* PR #1 hiển thị `renamed: dvd.py → aims/dvd.py` và `renamed: cart.py → aims/cart.py`
  (kiểm tra bằng `gh api repos/<owner>/<repo>/pulls/1/files`), **không** phải "1 tệp bị xoá + 1 tệp mới
  được thêm". Người review thấy ngay đây là thao tác di chuyển.
* Lịch sử vẫn đi xuyên qua lần đổi tên: `git log --oneline --follow -- aims/cart.py`
  vẫn thấy commit `feat: add initial DVD, Cart and demo program` ở thư mục gốc.

Cần nói chính xác một điểm: Git **không** lưu "rename" như một thuộc tính của commit. Việc nhận diện
đổi tên là *suy đoán ở thời điểm diff* dựa trên độ giống nhau của nội dung (mặc định 50%). Nghĩa là
`mv` + `git add -A` cũng cho kết quả tương đương. Giá trị thật của `git mv` là **tính tường minh và
an toàn của thao tác**, còn `--follow`/`blame` chỉ hoạt động khi phần nội dung đủ giống để Git nhận ra.

---

## 3. `release/lab01` có phải là một baseline không?

**Có.** Theo định nghĩa trong bài giảng, baseline là một trạng thái (configuration item) đã được
thống nhất và giao cho một mục đích cụ thể. `release/lab01` thoả các điều kiện đó:

* Nó được tạo **từ `master` sau khi PR #1 đã được review và merge** — tức là từ một trạng thái đã
  qua kiểm soát thay đổi, không phải từ nhánh đang làm dở.
* Nó là **bất biến theo quy ước**: không commit trực tiếp lên `release/*`; mọi thay đổi sau này (nếu có)
  phải đi qua `hotfix/*` và PR.
* Nó là thứ được nộp/đánh giá cho Lab 01, và ta chứng minh được nó **trùng khít** với trạng thái
  `master` đã merge tại thời điểm cắt nhánh:

```
$ git rev-parse origin/master origin/release/lab01
cb64178df40b81f29bc3ba4f9c286460b95c618c
cb64178df40b81f29bc3ba4f9c286460b95c618c
```

Tuy nhiên cần phân biệt **baseline theo quy ước** và **định danh bất biến**:

| | Nhánh `release/lab01` | Tag `v0.1.0` |
|---|---|---|
| Bản chất | con trỏ **di động** | con trỏ **bất biến** |
| Có thể đổi được không | có (nhánh là dòng bảo trì) | không bao giờ |
| Vai trò | dòng bảo trì/nộp bài | định danh chính xác một phiên bản |

Vì vậy ở Lab 01, `release/lab01` là baseline *đang sống*; đến Lab 04 ta gắn thêm tag `v0.1.0`
lên chính commit đó để có định danh bất biến, và lúc đó mới trả lời được câu hỏi
"chính xác thì Lab 01 là phiên bản nào".

---

## 4. Vì sao không commit thẳng lên `master` dù làm một mình?

Vì **quy trình không phụ thuộc vào số người**. Lý do cụ thể:

1. **PR là bản ghi kiểm soát thay đổi (Change Control).** Commit chỉ nói *cái gì* đổi; PR mới là nơi
   ghi *vì sao* đổi, ai đã xem, đã kiểm thử thế nào, và liên kết Issue ⇄ nhánh ⇄ commit ⇄ PR.
   Không có PR thì mất luôn hồ sơ đó — đúng thứ mà môn học này muốn dạy.
2. **`master` phải luôn ở trạng thái phát hành được.** Nếu ai cũng commit thẳng, không ai
   đảm bảo commit trên `master` đã xanh test; ngược lại, khi mọi thay đổi đi qua PR thì mỗi commit
   trên `master` là một trạng thái đã được tích hợp và (từ Lab 05) đã qua CI.
3. **Bảo vệ được chính mình.** Khi làm một mình, người review chính là mình: bước tạo PR buộc bạn
   đọc lại diff (`Files changed`), viết cách kiểm thử, và phát hiện lỗi trước khi nó thành lịch sử chung.
   Đó cũng là bước chuẩn bị "review" trước khi có partner thật.
4. **Tính đồng nhất của lịch sử.** Cùng một quy tắc cho mọi người (kể cả người làm một mình) thì
   lịch sử mới đọc được như nhau ở mọi lab; về sau khi ghép nhóm, quy ước và branch protection
   đã sẵn sàng, không phải "chuyển đổi" lại cách làm việc.
5. **Sửa sai rẻ hơn.** Một thay đổi sai đã merge qua PR thì hoàn tác bằng `git revert` qua một PR khác
   (Lab 03) — có hồ sơ, có review. Commit thẳng lên `master` mà sai thì lựa chọn duy nhất là viết lại
   lịch sử đã chia sẻ, điều bị cấm.

Bằng chứng gián tiếp: sau khi bật branch protection ở Lab 02 (Require a pull request before merging),
việc push thẳng bị GitHub từ chối:

```
$ git push
remote: error: GH006: Protected branch update failed for refs/heads/master.
remote:
remote: - Changes must be made through a pull request.
```
