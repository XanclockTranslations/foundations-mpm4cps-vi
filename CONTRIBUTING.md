# Đóng góp / Contributing

## Tiếng Việt

[Báo lỗi hoặc đề xuất sửa](https://github.com/XanclockTranslations/foundations-mpm4cps-vi/issues)
bằng cách nêu chương, mục, số hình hoặc phương trình,
vị trí trong bản dịch, và đoạn nguồn cần đối chiếu. Khi có thể, ghi cả trang
in và trang PDF của sách gốc. Mô tả vấn đề, đề xuất sửa và căn cứ kỹ thuật;
không coi một báo cáo AI là sự xác nhận của chuyên gia.

Đọc [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md) và
[license.md](license.md) trước khi sửa. Nguồn tiếng Anh được xác định trong
[source/manifest.json](source/manifest.json) và có thể tìm qua DOI của sách.

1. Sửa nguồn chuẩn trong `translation/`; `output/` là kết quả được sinh lại.
   Lưu văn bản bằng UTF-8, kết thúc dòng LF.
2. Giữ số mục, trích dẫn, mã, định danh hình thức, ký hiệu và dữ liệu nguồn.
   Ghi chú biên tập phải có đánh dấu; không âm thầm sửa lỗi của tác giả.
3. Khi đổi hình trong `assets/clean/`, giữ ghi công và cấu trúc khoa học.
   Cập nhật có chủ ý thông tin nguồn và dấu vân tay trong danh mục tài sản,
   rồi đối chiếu lại với nguồn và kiểm tra trang có hình đó.
4. Cài phụ thuộc, kiểm tra dự án và dựng PDF từ thư mục gốc:

```text
python -m pip install -r requirements.txt
python tools/check_project.py
python tools/build_book.py
```

Xem các trang bị ảnh hưởng ở kích thước đọc được, đặc biệt nhãn hình, công thức,
mã, ngắt trang và ghi công. Nêu những gì đã kiểm tra cùng giới hạn còn lại trong
mô tả thay đổi. Giữ tệp thực thi trình biên dịch, bộ nhớ đệm và dữ liệu rà soát
thô ngoài Git.

Các dấu vân tay hiện có trong `release/release-manifest.json` thuộc bản phát
hành đã kiểm tra ngày 14-10-2026. Gói ZIP đó chứa nguồn lịch sử, gồm bản LaTeX
CRLF. Nguồn và bộ lắp ghép hiện dùng UTF-8/LF; dữ liệu phụ trong PDF mới dựng
cũng có thể khác. Không ghi đè tệp phát hành cũ hay dùng báo cáo cũ để chứng nhận
đầu ra mới. Với bản phát hành mới, rà soát lại phần thay đổi, ghi dấu vân tay mới
và đính kèm PDF cùng gói nguồn tương ứng vào GitHub Releases.

## English

[Report an issue or proposed correction](https://github.com/XanclockTranslations/foundations-mpm4cps-vi/issues)
with the chapter, section, figure or
equation number, its location in the translation, and the source passage to
compare. Include printed and PDF page numbers when available. Describe the
problem, proposed correction and technical evidence; an AI report does not
establish expert approval.

Read [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md) and
[license.md](license.md) before editing. The original is identified in
[source/manifest.json](source/manifest.json) and can be obtained through its DOI.

1. Edit canonical sources in `translation/`; `output/` is regenerated. Save text
   as UTF-8 with LF line endings.
2. Preserve source numbering, citations, code, formal identifiers, notation and
   data. Mark editorial notes explicitly; do not silently correct author errors.
3. For changes to `assets/clean/`, retain credits and scientific structure.
   Deliberately update provenance and asset-inventory fingerprints, compare
   against the original, and review the affected rendered pages.
4. Install dependencies, check the project and build from the root using the
   three commands above.

Inspect affected pages at a readable size, especially artwork labels, equations,
code, page breaks and credits. State what was checked and remaining limitations
in the change description. Keep compiler executables, caches and raw review
data outside Git.

Existing fingerprints in `release/release-manifest.json` identify the release
verified on 2026-10-14. Its ZIP contains historical sources, including a CRLF
LaTeX master. Current sources and assembly use UTF-8/LF; newly compiled PDF
metadata may also differ. Preserve old release files, and do not certify new
output with old reports. For a new release, review the changes, record new
fingerprints, and attach the PDF and matching source package to GitHub Releases.
