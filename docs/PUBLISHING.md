# Công bố lên GitHub / Publishing to GitHub

Kho Git chứa nguồn dịch, artwork cần để biên dịch, tài liệu và công cụ portable.
Các PDF/ZIP phát hành, thư mục `output/`, log, cache và chứng cứ rà soát cục bộ
được bỏ qua bằng `.gitignore`.

Đích công bố: [XanclockTranslations/foundations-mpm4cps-vi](https://github.com/XanclockTranslations/foundations-mpm4cps-vi).
Mô tả repository: `[Machine Translated, Not Reviewed] Vietnamese translation of Foundations of Multi-Paradigm Modelling for Cyber-Physical Systems.`
Giữ nhãn này trong mô tả và README cho đến khi có rà soát chuyên môn của con người.

1. Đọc [README.md](../README.md), [license.md](../license.md) và bản PDF trước
   khi chọn phiên bản công bố. Kiểm tra nguồn bằng `python tools/check_project.py`.
2. Kiểm tra danh sách với `git status --short` và `git add --dry-run .`.
   Tạo commit đầu tiên từ thư mục dự án sau khi bạn đã rà soát nội dung.
3. Tạo repository `foundations-mpm4cps-vi` trong tổ chức `XanclockTranslations`
   rồi dùng `https://github.com/XanclockTranslations/foundations-mpm4cps-vi.git` làm remote.
   Nếu đẩy kho cục bộ hiện có, tạo repository từ xa trống để tránh hai commit
   khởi đầu khác nhau. Nhánh mặc định cục bộ là `main`.
4. Tạo GitHub Release và đính kèm `foundations-mpm4cps-vi.pdf`,
   `foundations-mpm4cps-vi-source.zip` cùng `release-manifest.json` từ thư mục
   `release/`. Các hash đã kiểm chứng nằm trong manifest và
   [báo cáo rà soát](review/README.md).

ZIP được giữ là ảnh chụp nguồn của ấn bản PDF đã kiểm chứng. Các README và công
cụ Git mới thuộc kho hiện tại; khi làm một bản phát hành mới từ kho này, hãy
biên dịch, rà soát và ghi manifest mới, giữ lại chứng cứ của bản trước.

## English

Run `python tools/check_project.py`, review `git status --short` and
`git add --dry-run .`, then make the initial commit when ready. Create an empty
GitHub repository named `foundations-mpm4cps-vi` in `XanclockTranslations`, add
`https://github.com/XanclockTranslations/foundations-mpm4cps-vi.git` as the remote,
and push `main`. Set the repository description to the text above and retain
the warning until human scholarly review has occurred. Upload the
preserved PDF, source ZIP and release manifest as GitHub Release assets.

The ZIP is the verified PDF edition's historical source snapshot. The current
Git repository also contains updated publishing documentation and portable build
tools. A future edition should receive a fresh build, review and manifest.
