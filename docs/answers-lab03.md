# Lab 03 — Câu hỏi thảo luận

Nhánh nộp bài: `release/lab03`. Bugfix đi từ `master` qua `bugfix/cart-limit-off-by-one`,
bugfix đi từ nhánh tính năng qua `bugfix/discount-calculation` (PR có base là `feature/discount`),
xung đột được xử lý trên `feature/show-added-title`, hoàn tác lịch sử chung qua
`bugfix/revert-show-added-title`.

---

## 1. Merge base là gì?

**Merge base** (cơ sở hợp nhất) của hai commit A và B là **tổ tiên chung gần nhất (best common
ancestor)** của chúng — chính là điểm mà hai dòng lịch sử tách ra.

```
$ git merge-base HEAD origin/master
7c1d9e0...
```

Vai trò của nó:

1. **Là mốc để tính "phần của tôi" và "phần của người khác".** `git merge` (và mọi PR) thực hiện
   *three-way merge*: nó so `merge-base → HEAD` (thay đổi của tôi) với `merge-base → origin/master`
   (thay đổi của người kia) rồi kết hợp hai tập thay đổi đó. Vì vậy:

   * `git log origin/master..HEAD` = "các commit của tôi kể từ merge base" — đúng bằng những gì PR
     sẽ mang đi. Cú pháp `A..B` nghĩa là *các commit có trong B mà không có trong A*.
   * GitHub `Files changed` chỉ hiển thị diff so với merge base, nên diff của bạn sạch, không lẫn
     thay đổi của người khác.

2. **Là mốc để xác định xung đột.** Xung đột chỉ xảy ra khi **cả hai bên cùng thay đổi cùng một vùng
   tính từ merge base**. Nếu chỉ một bên thay đổi một dòng, bên kia giữ nguyên (so với base), Git
   tự động lấy thay đổi đó — đó là lý do phần lớn merge diễn ra im lặng.

   Trong Phần C của bài, cả hai nhánh đều sửa **cùng một dòng** thông báo thêm đĩa tính từ base
   chung, nên Git không thể quyết định và sinh ra dấu xung đột:

   ```
   <<<<<<< HEAD                                  # nhánh của tôi (show-added-title)
           print(f"The disc '{dvd.title}' has been added")
   =======
           print("Đã thêm đĩa vào giỏ hàng")      # đã có trên master (vietnamese-messages)
   >>>>>>> origin/master
   ```

   `HEAD` trong xung đột **luôn là nhánh đang đứng** (nhánh đích của lệnh merge), không phải
   "nhánh mới hơn". Giải quyết xung đột = quyết định nội dung đúng cho vùng đó rồi xoá ba dấu.

3. **Là mốc để rebase.** `git rebase origin/master` thực chất là: tính `merge-base`, lấy các commit
   *của tôi* kể từ đó, rồi lần lượt áp lại chúng lên `origin/master`. Vì vậy rebase cũng "biết" phần
   nào là của mình nhờ merge base — nhưng nó **sinh SHA mới** cho từng commit.

4. **Trường hợp đặc biệt:** nếu hai nhánh đã từng merge qua lại (criss-cross), có thể tồn tại *nhiều*
   merge base; Git khi đó tạo một "virtual base" từ các base đó (`git merge-base --all` để xem).
   Đây là một lý do nữa để giữ lịch sử tuyến tính và đồng bộ thường xuyên.

Cách kiểm tra nhanh khi review:

```
$ git merge-base --is-ancestor origin/master HEAD && echo "đã chứa master"
$ git log --oneline origin/master..HEAD        # những gì PR sẽ mang đi
$ git log --oneline HEAD..origin/master        # những gì master hơn mình
```

---

## 2. Vì sao `master` / `release/*` phải dùng `revert`?

Vì đó là **lịch sử đã chia sẻ và đã được định danh**. Hai lệnh làm hai việc khác nhau về bản chất:

| | `reset` / `amend` / `rebase` | `revert` |
|---|---|---|
| Cơ chế | **dời con trỏ nhánh** sang commit khác (bỏ commit khỏi lịch sử) | **tạo commit mới** đảo ngược thay đổi |
| Viết lại lịch sử | Có (SHA của các commit bị bỏ/mới thay đổi) | Không |
| Những người đã `pull` | Lịch sử của họ lệch; hợp nhất lại phải `push --force` | Chỉ cần `git pull` — lịch sử chỉ dài thêm |
| Dùng cho | commit **chưa push** (nhánh riêng, `topic/undo-practice`) | `master`, `release/*`, mọi thứ đã công bố |

Lý do cụ thể trong ngữ cảnh SCM:

1. **`master` và `release/*` là thứ người khác đang dựa vào.** Mọi bản clone khác (Dev 2, CI,
   máy chủ build) đang giữ đúng các SHA cũ. Viết lại lịch sử làm chúng trở thành "commit mồ côi":
   `git pull` của họ sẽ thất bại hoặc tạo lịch sử chẻ đôi; cách duy nhất để đồng bộ là `--force`,
   và `--force` chính là cách đè mất commit của người khác.
2. **Xoá được commit không có nghĩa là xoá được hậu quả.** Một merge commit đã nằm trên `master`
   (như merge của `feature/show-added-title`) thì muốn "bỏ" nó bằng `reset` phải viết lại *mọi*
   commit sau nó — trong khi những commit sau nó là do người khác tạo.
3. **Định danh đã công bố phải còn giá trị.** Tag `v1.0.0`, số hiệu PR, liên kết Issue ⇄ commit đều
   trỏ tới SHA cụ thể. Rewrite lịch sử làm tag trỏ vào commit không còn tồn tại trong nhánh,
   `git tag --contains` / `git describe` mất ý nghĩa, và **kiểm toán cấu hình** (Lab 04–05) không
   còn tái tạo được phiên bản đã phát hành.
4. **`revert` để lại dấu vết "vì sao".** Lịch sử ghi rõ: đã thêm X ở commit A, và ở commit B đã đảo
   ngược X với lý do trong message. Đó là bằng chứng kiểm toán; `reset` thì im lặng.
5. **Branch protection biến điều này thành luật kỹ thuật.** Rule trên `master` và `release/*` ở bài
   này bật *Do not allow force pushes* và *Do not allow deletions*, nên ngay cả khi muốn viết lại
   lịch sử, GitHub cũng từ chối.

Chi tiết phải nhớ: revert một **merge commit** thì phải chỉ định *mainline* —

```
$ git revert -m 1 <sha-merge-commit>
```

`-m 1` nói "giữ cha thứ nhất (nhánh đích, tức `master`) làm trục chính, và đảo ngược mọi thay đổi
mà merge đã mang vào". Nếu quên, Git báo `commit ... is a merge but no -m option was given`.

Và quan trọng: **bản thân việc revert cũng phải đi qua PR** (`bugfix/revert-show-added-title`) —
"hoàn tác" là một thay đổi như mọi thay đổi khác, vẫn cần review và vẫn để lại hồ sơ.

*Lưu ý thực hành:* sau khi revert một merge, nhánh gốc vẫn được coi là "đã merge" — muốn áp dụng lại
tính năng sau này thì phải `revert` chính commit revert đó (revert of the revert) chứ không merge lại
nhánh cũ một cách đơn giản.
