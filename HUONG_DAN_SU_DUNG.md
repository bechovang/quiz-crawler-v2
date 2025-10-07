# HƯỚNG DẪN SỬ DỤNG EHOU AUTOMATION SUITE

## 🎯 Tổng quan
EHOU Automation Suite là bộ công cụ tự động hóa cho hệ thống E-learning của Trường Đại học Mở Hà Nội (EHOU), giúp sinh viên quản lý việc học hiệu quả và tiết kiệm thời gian.

## 📋 Các chức năng chính

### 1. Xem điểm tổng hợp các môn học
- **Mục đích**: Tự động đăng nhập và tổng hợp điểm tổng kết của tất cả các môn học
- **Kết quả**: Bảng Markdown gọn gàng với điểm số của từng môn

### 2. Cào đề thi (chưa có đáp án) từ link Attempt ⭐ MỚI
- **Mục đích**: Tạo "đề tủ" từ trang làm bài thi mà không cần hy sinh lần làm bài
- **Input**: URL trang `attempt.php` (trang làm bài thi)
- **Output**: File Markdown với cấu trúc câu hỏi, placeholder ☐ cho ô trống
- **Ưu điểm**: Không cần nộp bài để lấy đáp án

### 3. Cào và lưu trữ đề thi từ link Review (có đáp án)
- **Mục đích**: Lưu trữ đề thi hoàn chỉnh từ trang review (đã có đáp án)
- **Input**: URL trang `review.php` (trang xem lại bài thi đã làm)
- **Output**: File Markdown với câu hỏi và đáp án đúng

### 4. Tự động làm bài từ file đề thi đã lưu
- **Mục đích**: Tự động điền đáp án cho bài thi mới từ file đã chuẩn bị
- **Input**: URL trang `attempt.php` + file Markdown có đáp án
- **Output**: Bài thi được điền tự động

### 5. Cào đề -> Giải offline -> Tự động điền (Chỉ nhập URL 1 lần) ⭐ TIỆN LỢI NHẤT
- **Mục đích**: Quy trình tối ưu - chỉ nhập URL một lần, sau đó giải offline và tự động điền
- **Input**: Chỉ cần URL trang `attempt.php` một lần duy nhất
- **Output**: 
  - `MODE5_CAU_HOI.md` - File câu hỏi để đọc và giải
  - `MODE5_DAP_AN.md` - File template đáp án để điền
  - Tự động điền đáp án vào bài thi sau khi hoàn thành
- **Ưu điểm**: 
  - Không cần nhập URL nhiều lần
  - Giải bài offline, không lo hết thời gian
  - Tự động điền ngay khi đã có đáp án
  - File cố định, ghi đè mỗi lần chạy (không tạo nhiều file rác)

## 🚀 Luồng công việc khuyến nghị

### **🌟 PHƯƠNG PHÁP MỚI - SỬ DỤNG MODE 5 (Đơn giản nhất)**

#### **Quy trình 1 bước duy nhất:**
```bash
# Chọn chức năng 5
# Nhập URL attempt.php MỘT LẦN DUY NHẤT
# => Chương trình tự động:
#    1. Cào đề thi và lưu 2 file:
#       - MODE5_CAU_HOI.md - để đọc/giải
#       - MODE5_DAP_AN.md - để điền đáp án
#    2. Đợi bạn điền đáp án vào MODE5_DAP_AN.md
#    3. Tự động điền đáp án vào bài thi khi bạn nhấn Enter
#    * File sẽ được ghi đè mỗi lần chạy Mode 5
```

#### **Chi tiết các bước:**
1. **Chọn chức năng 5** trong menu
2. **Nhập URL attempt.php** của bài thi
3. **Đọc file câu hỏi** (`MODE5_CAU_HOI.md`) để hiểu đề
4. **Điền đáp án** vào file template (`MODE5_DAP_AN.md`):
   - Trắc nghiệm: Thay `- [ ]` thành `- [x]` cho đáp án đúng
   - Điền từ: Thay `[[]]` thành `[[đáp án]]`
5. **Lưu file** đáp án
6. **Quay lại terminal** và nhấn Enter
7. **Chương trình tự động điền** đáp án vào bài thi

**Lưu ý:** File `MODE5_CAU_HOI.md` và `MODE5_DAP_AN.md` sẽ được ghi đè mỗi lần chạy Mode 5 (chỉ dùng tạm cho quy trình làm bài).

---

### **📚 PHƯƠNG PHÁP CŨ - Thủ công từng bước**

#### **Bước 1: Tạo đề tủ (Không hy sinh lần làm bài)**
```bash
# Chọn chức năng 2
# Nhập URL attempt.php
# Kết quả: File *_CHUA_CO_DAP_AN.md
```

#### **Bước 2: Điền đáp án thủ công**
1. Mở file `*_CHUA_CO_DAP_AN.md` bằng trình soạn thảo
2. Điền đáp án đúng vào các ô trống:
   - **Trắc nghiệm**: Thay `- [ ]` thành `- [x]` cho đáp án đúng
   - **Điền từ**: Thay `☐` bằng đáp án đúng (T/F, từ phù hợp)
3. Lưu file với tên mới (ví dụ: `de_thi_DA_DIEN.md`)

#### **Bước 3: Tự động làm bài**
```bash
# Chọn chức năng 4
# Nhập URL attempt.php mới
# Nhập đường dẫn file đã điền đáp án
# Kết quả: Bài thi được điền tự động
```

## 📝 Ví dụ cụ thể

### **🌟 Ví dụ cho Mode 5 (Format mới với [[]])):**

#### **File template đáp án được tạo tự động:**
```markdown
### ID: q123
### Loại: Trắc nghiệm

#### Nội dung:
> What is the capital of Vietnam?

#### Đáp án:
- [ ] a. Ho Chi Minh City
- [ ] b. Hanoi
- [ ] c. Da Nang
- [ ] d. Hue
```

#### **Sau khi bạn điền (thay [ ] thành [x]):**
```markdown
### ID: q123
### Loại: Trắc nghiệm

#### Nội dung:
> What is the capital of Vietnam?

#### Đáp án:
- [ ] a. Ho Chi Minh City
- [x] b. Hanoi  ← Đáp án đúng
- [ ] c. Da Nang
- [ ] d. Hue
```

#### **Câu điền từ - Template ban đầu:**
```markdown
### ID: q456
### Loại: Điền từ

#### Nội dung:
> Complete: I ☐ to school yesterday.

#### Đáp án:
> [[]] [[]]  ← Điền đáp án vào đây
```

#### **Sau khi bạn điền:**
```markdown
### ID: q456
### Loại: Điền từ

#### Nội dung:
> Complete: I ☐ to school yesterday.

#### Đáp án:
> [[went]] [[T]]  ← Đã điền xong
```

---

### **📚 Ví dụ cho Mode cũ (Format cũ với ☐):**

#### **Câu hỏi trắc nghiệm:**
```markdown
#### Đáp án:
- [ ] a. Unbelievable
- [x] b. Belief  ← Đáp án đúng
- [ ] c. Believe
- [ ] d. Believable
```

#### **Câu hỏi điền từ (True/False):**
```markdown
#### Nội dung:
> ☐ 1. The writer wrote the article to encourage us to work more and relax less.
> ☐ 2. People today are having a less stressful life than they did in the past.

#### Đáp án:
> [F] [F]  ← Điền F cho False, T cho True
```

#### **Câu hỏi điền từ (Matching):**
```markdown
#### Nội dung:
> 1. waste time ☐
> 2. take a long time ☐

#### Đáp án:
> [use time badly] [last too long]  ← Điền từ phù hợp
```

## ⚠️ Lưu ý quan trọng

### **Bảo mật:**
- Chỉ sử dụng cho mục đích học tập và nghiên cứu
- Không chia sẻ thông tin đăng nhập
- Sử dụng có trách nhiệm, không lạm dụng

### **Kỹ thuật:**
- Đảm bảo kết nối internet ổn định
- Không đóng trình duyệt trong quá trình tự động
- Backup file đề thi quan trọng

### **Troubleshooting:**
- **Lỗi đăng nhập**: Kiểm tra lại thông tin tài khoản
- **Lỗi cào đề**: Kiểm tra URL có đúng định dạng không
- **Lỗi tự động điền**: Kiểm tra file Markdown có đúng format không

## 🔧 Cài đặt và chạy

```bash
# 1. Kích hoạt virtual environment
.\venv\Scripts\activate

# 2. Chạy chương trình
python main.py

# 3. Nhập thông tin đăng nhập EHOU
# 4. Chọn chức năng mong muốn
```

## 📞 Hỗ trợ

Nếu gặp vấn đề, hãy kiểm tra:
1. Thông tin đăng nhập có chính xác không
2. URL có đúng định dạng không
3. File Markdown có đúng cấu trúc không
4. Kết nối internet có ổn định không

---

**Lưu ý**: Công cụ này được tạo ra với mục đích học tập và nghiên cứu. Người dùng chịu hoàn toàn trách nhiệm về việc sử dụng. 