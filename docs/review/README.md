# Kiểm chứng ấn bản / Edition verification

**[Machine Translated, Not Reviewed]** — Hồ sơ này ghi các lượt kiểm tra bằng AI;
bản dịch chưa được con người rà soát chuyên môn. This record documents AI
checks; the translation has not received human scholarly review.

## Phạm vi

Ấn bản máy tiếng Việt năm 2026 gồm 355 trang A4, chín chương, 157 hình đánh số,
11 bảng, sáu sơ đồ bài tập và 310 tài liệu tham khảo. Bộ đầu vào dàn trang có
181 PDF: các hình đánh số, sơ đồ bài tập, bảy phần hình phóng lớn và 13 ô hình
của Bảng 4.1. Ảnh bìa JPEG là tài sản thứ 182.

Nguồn: *Foundations of Multi-Paradigm Modelling for Cyber-Physical Systems*,
Springer, 2020, [DOI 10.1007/978-3-030-43946-0](https://doi.org/10.1007/978-3-030-43946-0).
LaTeX ở đây được dựng lại từ PDF; đây không phải bộ nguồn LaTeX của nhà xuất bản.

[Hồ sơ ghi công tài sản](asset-rights.md) giữ các ghi công riêng của hình/bảng,
căn cứ thông báo giấy phép trong sách và phạm vi lượt rà soát quyền sử dụng.

## Rà soát hình

Lượt rà soát theo phản hồi người đọc đã đối chiếu đủ 181 tài sản PDF trực tiếp
với nét vẽ hoặc bitmap nguồn. Có 13 hình được sửa:

- 2.8, 2.14: bỏ chữ tiếng Anh còn sót dưới nhãn Việt.
- 2.11, 2.20, 4.1, 4.2: khôi phục nét nguồn bị nền nhãn che; dời nhãn khi cần.
- 2.12: thay chữ bitmap MSe mờ bằng chữ vector; giữ Ugen, ảnh xung, mũi tên và khung.
- 2.19: dời nhãn tránh đường nguồn.
- 5.3, 5.5, 5.7, 5.9: bỏ phần nền nhãn chạm trục hoặc đầu mũi tên.
- 9.4: khôi phục hàng pixel trên của viền chú giải.

168 PDF còn lại giữ nguyên byte. Các khối mã nguyên văn và ký hiệu hình thức
được giữ nguyên trong lượt sửa này. Một số ảnh bitmap nhỏ, nét nhạt và nhãn bị
cắt đã có trong sách gốc; không suy đoán dữ liệu để vẽ thêm.

Bản PDF cuối được đối chiếu toàn trang: 49 trang thay đổi pixel đã được xem
lại trực tiếp; 304 trang còn lại khớp RGB và kích thước với bản đã kiểm tra.
Có 51 lượt xem riêng trang ở kích thước gốc. Gói nguồn ZIP sau đó được biên dịch
độc lập: đủ 355 trang, văn bản và pixel RGB của mọi trang khớp bản phát hành.

## Dấu vân tay bản phát hành

[release-manifest.json](../../release/release-manifest.json) ghi bản phát hành
đã kiểm chứng trước đợt chuẩn bị Git. PDF và ZIP giữ nguyên byte:

| Tệp | SHA-256 |
| --- | --- |
| `foundations-mpm4cps-vi.pdf` | `007d2b11243a695baa14058a294ca1e9132d92da30ab02bd856b6fb5f78243de` |
| `foundations-mpm4cps-vi-source.zip` | `3cd9f4252604b12f30cbb269860d2b7ba7b66fe8606dc128f92c6e9c851fde72` |
| Master LaTeX lịch sử, CRLF | `059827b1d55663d161268a967444610ddc79041135c7bc9bfb1d9f343b59326f` |

Kho Git dùng UTF-8 và LF. Master được tạo lại trong lượt kiểm chứng đó dùng LF, có SHA-256
`91496bb8362e9eca25000657c5e3da735392f34693ee8df4f6b181e1ae5f2ebc`;
nội dung khớp master lịch sử sau khi chuẩn hóa CRLF thành LF. Tài liệu và công
cụ trong kho Git đã được cập nhật cho việc công bố; ZIP trên là ảnh chụp nguồn
của bản phát hành đã kiểm chứng, nên không chứa các thay đổi tài liệu Git này.

## Lưu trữ chứng cứ và tái kiểm tra

Các bản chụp, ảnh so sánh, log, PDF nguồn và công cụ xử lý lịch sử đã chuyển
sang kho lưu trữ cục bộ ngoài thư mục dự án, giữ nguyên nội dung chứng cứ.
Một số trường trong JSON nguồn/hình vẫn trỏ tới tên tệp lịch sử như `review/`
hoặc `source/original.pdf`; đó là thông tin xuất xứ, không phải đầu vào cần cho
biên dịch. Các đường dẫn máy tuyệt đối đã được đổi thành đường dẫn tương đối.
Bản gốc của metadata được giữ trong kho lưu trữ.

[asset-inventory.json](../../source/asset-inventory.json) liệt kê đường dẫn,
kích thước và SHA-256 của 182 đầu vào media hiện tại. `tools/check_project.py`
kiểm tra các tệp đó, tham chiếu LaTeX và quy ước văn bản. Hash chứng minh tính
toàn vẹn tệp; việc thay hình cần được rà soát trực quan riêng trước khi cập nhật
inventory. Chạy lại biên dịch và rà soát PDF sau mỗi thay đổi nội dung.

## English

This is a curated summary of the completed 355-page edition review. All 181 PDF
artwork inputs were compared against source geometry or bitmap material; 13
figures were repaired. An independent rebuild of the released source ZIP matched
the text and decoded RGB pixels of every released page. Small or faint details
in the original source remain documented limitations.

The release manifest describes the preserved PDF and source ZIP, including the
historical CRLF master hash. Git sources and newly assembled masters use LF.
At that verification, the LF master had identical content after newline normalization. Repository
documentation and build tooling have changed since the released ZIP snapshot.
Full historical evidence is preserved in a separate local archive; historical
metadata references are provenance, not missing build dependencies. The public
asset inventory checks file integrity and does not replace visual review.
