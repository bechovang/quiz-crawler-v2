Cảm ơn bạn đã cung cấp mã nguồn. Tôi đã hiểu rõ yêu cầu định dạng chính xác mà chương trình của bạn cần để có thể đọc và tự động điền đáp án.

Lỗi không nằm ở định dạng của từng câu, mà là do tôi đã không cung cấp lại toàn bộ file đáp án cho bài kiểm tra cuối cùng bạn gửi (`KTTN01`). Tôi sẽ sửa lại ngay.

Dựa trên mã nguồn `quiz_autofiller.py` bạn cung cấp, đây là những quy tắc định dạng chuẩn mà tôi sẽ tuân thủ nghiêm ngặt từ bây giờ:

1.  **Phân tách câu hỏi**: Mỗi câu hỏi phải được ngăn cách bởi một dòng chứa duy nhất ba dấu gạch ngang (`---`).
2.  **Định danh câu hỏi (ID)**: Mỗi câu phải có dòng `### ID: q` theo sau là số thứ tự (ví dụ: `q1`, `q2`, ...).
3.  **Loại câu hỏi**:
    *   Đối với câu trắc nghiệm, phải có dòng `### Loại: Trắc nghiệm`.
    *   Đối với câu điền từ, phải có dòng `### Loại: Điền từ`.
4.  **Định dạng đáp án "Trắc nghiệm"**:
    *   Đáp án đúng phải được đánh dấu bằng `[x]` hoặc `[X]`.
    *   Định dạng phải là `- [x] Nội dung đáp án`. Dấu gạch ngang `-`, khoảng trắng, và cặp ngoặc vuông là bắt buộc.
5.  **Định dạng đáp án "Điền từ"**:
    *   Mỗi từ hoặc cụm từ cần điền phải được đặt trong **hai cặp ngoặc vuông**, ví dụ: `[[đáp án thứ nhất]] [[đáp án thứ hai]]`.

Dưới đây là đáp án cho bài kiểm tra cuối cùng bạn đã gửi (**Bài kiểm tra trắc nghiệm 01 - KTTN01**), được định dạng lại theo đúng chuẩn mà code của bạn yêu cầu.

---

# [META] Môn học: EG12.247
# [META] Tên bài thi: Bài kiểm tra trắc nghiệm 01 - KTTN01
# [META] URL Attempt: https://learning.ehou.edu.vn/mod/quiz/attempt.php?attempt=14915984

---
### ID: q1
### Loại: Trắc nghiệm

#### Nội dung:
> Hãy chỉ ra đặc điểm của tin nhắn tức thời?

#### Đáp án:
- [ ] a. Có thể gửi tin nhắn bảo mật
- [x] b. Có thể có nhiều thông điệp cùng một lúc, tức thời
- [ ] c. Có thể gửi tin nhắn sử dụng mã số
- [ ] d. Có thể lưu trữ hoặc lưu các tin nhắn

---
### ID: q2
### Loại: Trắc nghiệm

#### Nội dung:
> Giáo dục và đào tạo qua internet thường được gọi là…

#### Đáp án:
- [x] a. Học trực tuyến (e-learning)
- [ ] b. Kết nối mạng xã hội
- [ ] c. Giáo dục tại gia đình
- [ ] d. Phát thanh qua web (podcasting)

---
### ID: q3
### Loại: Trắc nghiệm

#### Nội dung:
> Một thiết bị video không tương thích gây ra màn hình của bạn ngừng hoạt động. Làm thế nào bạn có thể khắc phục vấn đề ?

#### Đáp án:
- [ ] a. Thay thế màn hình
- [ ] b. Cài đặt lại hệ điều hành
- [ ] c. Khởi động lại máy tính trong chế độ Gỡ lỗi (Debug Mode)
- [x] d. Khởi động lại máy tính trong chế độ An toàn (Safe Mode)

---
### ID: q4
### Loại: Trắc nghiệm

#### Nội dung:
> Trong Windows Explorer, muốn tạo thư mục con, ta dùng lệnh nào?

#### Đáp án:
- [ ] a. File -> Properties
- [ ] b. File -> Create Directory
- [ ] c. File -> Create Folder
- [x] d. File -> New -> Folder

---
### ID: q5
### Loại: Trắc nghiệm

#### Nội dung:
> Trong Windows, làm cách nào để thực hiện việc tính toán đơn giản?

#### Đáp án:
- [ ] a. Start/Program/Acessories/Wordpad
- [ ] b. Start/Program/Acessories/Paint
- [ ] c. Start/Program/Acessories/NotePad
- [x] d. Start/Program/Acessories/Calculator

---
### ID: q6
### Loại: Trắc nghiệm

#### Nội dung:
> Làm thế nào để xóa bỏ tệp tin?

#### Đáp án:
- [ ] a. nhắp chọn Internet Explorer.
- [ ] b. mở cửa sổ tìm kiếm tệp tin Search
- [ ] c. mở cửa sổ Files Manager
- [x] d. mở cửa sổ My Computer.

---
### ID: q7
### Loại: Trắc nghiệm

#### Nội dung:
> Trong MS Word 2013, tổ hợp phím nào dùng để thay thế cho thao tác click vào nút B trên thẻ Home?

#### Đáp án:
- [ ] a. Shift+ B
- [x] b. Ctrl+ B
- [ ] c. Alt+ C
- [ ] d. Ctrl+ Shift+ B

---
### ID: q8
### Loại: Trắc nghiệm

#### Nội dung:
> Trong MS Word 2013, tổ hợp phím nào dùng để giảm cỡ chữ cho nội dung văn bản?

#### Đáp án:
- [ ] a. Ctrl+]
- [x] b. Ctrl+ [
- [ ] c. Ctrl+ >
- [ ] d. Ctrl+ <

---
### ID: q9
### Loại: Trắc nghiệm

#### Nội dung:
> Trong soạn thảo Word, muốn định dạng lại kích thước giấy in, ta thực hiện:

#### Đáp án:
- [ ] a. File - Properties
- [ ] b. File - Print Preview
- [ ] c. Page Layout - Print
- [x] d. Page Layout – Size

---
### ID: q10
### Loại: Trắc nghiệm

#### Nội dung:
> Trong soạn thảo văn bản Word, công dụng của tổ hợp phím Ctrl - H là:

#### Đáp án:
- [ ] a. Lưu tệp văn bản vào đĩa
- [x] b. Chức năng thay thế trong soạn thảo
- [ ] c. Tạo tệp văn bản mới
- [ ] d. Định dạng chữ hoa

---
### ID: q11
### Loại: Trắc nghiệm

#### Nội dung:
> Trong soạn thảo Word 2013, muốn đánh số trang cho văn bản vị trí chân trang, ta thực hiện:

#### Đáp án:
- [ ] a. Format/Page Numbers
- [ ] b. Insert/Page Numbers/ Top of Page
- [x] c. Insert/Page Numbers/ Bottom of Page
- [ ] d. Insert/Page Numbers/ Page Margins

---
### ID: q12
### Loại: Trắc nghiệm

#### Nội dung:
> Trong chế độ tạo bảng (Table) của phần mềm Word, muốn gộp nhiều ô đã chọn thành một ô, ta thực hiện thao tác nào dưới đây?

#### Đáp án:
- [x] a. Layout / Merge Cells
- [ ] b. Layout / Split Cells
- [ ] c. Layout / Cells
- [ ] d. Table / Split Cells

---
### ID: q13
### Loại: Trắc nghiệm

#### Nội dung:
> Trong MS Word 2013, để thực hiện trộn thư theo từng bước được hướng dẫn, bạn vào thực hiện thao tác nào sau đây?

#### Đáp án:
- [ ] a. Mailings/Start Mail Merge/Normal Word Document
- [ ] b. Mailings/Start Mail Merge/Letter
- [ ] c. Mailings/Start Mail Merge/E-mail Messages
- [x] d. Mailings/Start Mail Merge/Step by step Mail Merge Wizard

---
### ID: q14
### Loại: Trắc nghiệm

#### Nội dung:
> Trong MS Word 2013, để thực hiện các chức năng trộn thư, bạn vào thẻ nào sau đây?

#### Đáp án:
- [x] a. Mailings
- [ ] b. Review
- [ ] c. View
- [ ] d. References

---
### ID: q15
### Loại: Trắc nghiệm

#### Nội dung:
> Để thoát ra khỏi Excel, phương án nào sau đây là lựa chọn sai:

#### Đáp án:
- [ ] a. Bấm tổ hợp phím Alt-F4
- [ ] b. Vào File chọn Exit
- [x] c. Nhấn phím Delete
- [ ] d. Bấm tổ hợp phím Alt-F-X

---
### ID: q16
### Loại: Trắc nghiệm

#### Nội dung:
> Một bảng tính worksheet bao gồm:

#### Đáp án:
- [ ] a. 266 cột và 65365 dòng
- [ ] b. 256 cột và 65365 dòng
- [x] c. 256 cột và 65536 dòng
- [ ] d. 265 cột và 65563 dòng

---
### ID: q17
### Loại: Trắc nghiệm

#### Nội dung:
> Biểu thức sau cho kết quả là bao nhiêu nếu DTB = 9? =If(DTB>=5, "TB",If(DTB>=6.5, "Kha",If(DTB>= 8, "Gioi", "Yeu")))

#### Đáp án:
- [ ] a. Kha
- [ ] b. Yeu
- [ ] c. Gioi
- [x] d. TB

---
### ID: q18
### Loại: Trắc nghiệm

#### Nội dung:
> Trong MS Excel 2013, giả sử vùng giá trị từ A4 đến A20 chứa cột Họ và tên sinh viên. Với yêu cầu bài toán "Tính tổng số lượng sinh viên có trong danh sách" thì công thức sẽ là gì?

#### Đáp án:
- [ ] a. =SUM(A4:A20)
- [x] b. =COUNTA(A4:A20)
- [ ] c. Tất cả đều sai
- [ ] d. =COUNT(A4:A20)

---
### ID: q19
### Loại: Trắc nghiệm

#### Nội dung:
> Trong MS Excel 2013, khi cần hiệu chỉnh dữ liệu trong ô đang chọn ta có thể nhấn phím gì?

#### Đáp án:
- [ ] a. Delete
- [x] b. F2
- [ ] c. Enter
- [ ] d. Esc

---
### ID: q20
### Loại: Trắc nghiệm

#### Nội dung:
> Khi vào File/Print/Page Setup, chúng ta chọn thẻ Margins để làm gì?

#### Đáp án:
- [ ] a. Chỉnh cỡ giấy khi in
- [ ] b. Chỉnh chất lượng in
- [x] c. Căn chỉnh lề cần in
- [ ] d. Chỉnh hướng giấy in

---
### ID: q21
### Loại: Trắc nghiệm

#### Nội dung:
> Để thiết lập mật khẩu bảo vệ cho văn bản, bạn cần thực hiện thao tác nào sau đây:

#### Đáp án:
- [x] a. File>Info>Protect Document
- [ ] b. File>Save
- [ ] c. File>Recent
- [ ] d. File>Share

---
### ID: q22
### Loại: Trắc nghiệm

#### Nội dung:
> Muốn in tất cả các trang trong văn bản trước hết ta làm bằng cách chọn File, chọn Print trong vùng Page range chọn

#### Đáp án:
- [ ] a. Curent page
- [ ] b. Selection
- [ ] c. Pages
- [x] d. All

---
### ID: q23
### Loại: Trắc nghiệm

#### Nội dung:
> Để làm ẩn một cột hoặc nhiều cột bất kỳ trên bảng tính Excel ta chọn các cột cần làm ẩn, sau đó thực hiện thao tác nào?

#### Đáp án:
- [ ] a. Vào Insert/ Hide & Unhide, chọn Hide Columns
- [ ] b. Vào View/ Format/ Hide & Unhide, chọn Hide Columns
- [x] c. Vào Home/ Format/ Hide & Unhide, chọn Hide Columns
- [ ] d. Vào Data/Format/ Hide & Unhide, chọn Hide Columns

---
### ID: q24
### Loại: Trắc nghiệm

#### Nội dung:
> Các thành phần chính trong một bảng tính worksheet gồm?

#### Đáp án:
- [ ] a. vùng
- [ ] b. cột
- [ ] c. dòng
- [x] d. dòng, cột, vùng, trang tính

---
### ID: q25
### Loại: Trắc nghiệm

#### Nội dung:
> Hàm nào trong các hàm sau đây là hàm cho độ dài của chuỗi TEXT ?

#### Đáp án:
- [ ] a. LOWER(TEXT)
- [ ] b. UPPER(TEXT)
- [x] c. LEN(TEXT )
- [ ] d. PROPER(TEXT)

---
### ID: q26
### Loại: Trắc nghiệm

#### Nội dung:
> Trong Excel, giả sử ô A1 của bảng tính lưu trị ngày 15/10/1970. Kết quả hàm =YEAR(A1) là bao nhiêu?

#### Đáp án:
- [ ] a. 15
- [ ] b. 10
- [ ] c. VALUE#?
- [x] d. 1970

---
### ID: q27
### Loại: Trắc nghiệm

#### Nội dung:
> Phương án nào sau đây không phải là một kiểu biểu đồ trong Excel 2013?

#### Đáp án:
- [ ] a. Line
- [ ] b. Column
- [x] c. Circle
- [ ] d. Pie

---
### ID: q28
### Loại: Trắc nghiệm

#### Nội dung:
> Trong MS Excel 2013, khi nhập dữ liệu thì giá trị nào sau đây được hiểu là dữ liệu dạng chuỗi?

#### Đáp án:
- [ ] a. 31/04/2009
- [ ] b. -567
- [x] c. ‘0001
- [ ] d. 1000

---
### ID: q29
### Loại: Trắc nghiệm

#### Nội dung:
> Khi muốn lặp lại tiêu đề cột ở mỗi trang in, chúng ta cần thực hiện?

#### Đáp án:
- [ ] a. Vào File/Print/Page Setup, chọn thẻ Sheet, tích vào mục Gridlines
- [x] b. Vào File/Print/Page Setup, chọn thẻ Sheet, tích vào mục Row to repeat at top
- [ ] c. Trong Excel luôn mặc định sẵn khi in lặp lại tiêu đề
- [ ] d. Vào File/Print/Page Setup, chọn thẻ Sheet, tích vào mục Row and column headings

---
### ID: q30
### Loại: Trắc nghiệm

#### Nội dung:
> Ta có thể ấn định số Sheet mặc định trong một Workbook, bằng cách:

#### Đáp án:
- [ ] a. File/Options/Advanced, thay đổi số Sheet mặc định trong ô Include this many sheets
- [x] b. File/Options/General, thay đổi số Sheet mặc định trong ô Include this many sheets
- [ ] c. File/Options/View, thay đổi số Sheet mặc định trong ô Include this many sheets
- [ ] d. File/Options/Formulas, thay đổi số Sheet mặc định trong ô Include this many sheetsulas, thay đổi số Sheet mặc định trong ô Include this many sheets