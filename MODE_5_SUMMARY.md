# MODE 5 - TỔNG KẾT / SUMMARY

## 🎯 Chức năng mới / New Feature

### Tiếng Việt:
**Mode 5: Cào đề -> Giải offline -> Tự động điền (Chỉ nhập URL 1 lần)**

#### Đặc điểm nổi bật:
- ✅ Chỉ cần nhập URL **MỘT LẦN DUY NHẤT**
- ✅ Tự động tạo 2 file cố định (ghi đè mỗi lần chạy):
  - `MODE5_CAU_HOI.md` - File câu hỏi để đọc/giải
  - `MODE5_DAP_AN.md` - File template đáp án để điền
- ✅ Giải bài offline, không lo hết thời gian
- ✅ Tự động điền đáp án vào bài thi sau khi hoàn thành

#### Quy trình sử dụng:
1. Chạy chương trình và chọn **chức năng 5**
2. Nhập URL bài thi (attempt.php) - **CHỈ MỘT LẦN**
3. Chương trình sẽ:
   - Cào toàn bộ đề thi
   - Tạo file `MODE5_CAU_HOI.md` để bạn đọc
   - Tạo file `MODE5_DAP_AN.md` để bạn điền đáp án
4. Bạn mở file `MODE5_DAP_AN.md` và điền:
   - **Trắc nghiệm**: Thay `- [ ]` thành `- [x]` cho đáp án đúng
   - **Điền từ**: Thay `[[]]` thành `[[đáp án]]`
5. Lưu file đáp án
6. Quay lại terminal, nhấn Enter
7. Chương trình tự động điền tất cả đáp án vào bài thi! 🎉

**Lưu ý**: File `MODE5_CAU_HOI.md` và `MODE5_DAP_AN.md` sẽ được ghi đè mỗi lần chạy Mode 5.

---

### English:
**Mode 5: Scrape -> Solve Offline -> Auto-Fill (Enter URL Only Once)**

#### Key Features:
- ✅ Only need to enter URL **ONCE**
- ✅ Automatically creates 2 fixed files (overwritten each run):
  - `MODE5_CAU_HOI.md` - Questions file for reading/solving
  - `MODE5_DAP_AN.md` - Answer template file for filling in
- ✅ Solve quiz offline, no time pressure
- ✅ Automatically fills in answers after completion

#### Usage Flow:
1. Run the program and select **function 5**
2. Enter quiz URL (attempt.php) - **ONLY ONCE**
3. The program will:
   - Scrape the entire quiz
   - Create `MODE5_CAU_HOI.md` file for you to read
   - Create `MODE5_DAP_AN.md` file for you to fill in answers
4. Open `MODE5_DAP_AN.md` and fill in:
   - **Multiple choice**: Change `- [ ]` to `- [x]` for correct answer
   - **Fill in blanks**: Change `[[]]` to `[[answer]]`
5. Save the answer file
6. Return to terminal, press Enter
7. Program automatically fills all answers into the quiz! 🎉

**Note**: Files `MODE5_CAU_HOI.md` and `MODE5_DAP_AN.md` are overwritten each time you run Mode 5.

---

## 📁 Files Created / Các file đã tạo

### New Files / File mới:
1. **`features/quiz_solve_and_fill.py`** - Core implementation of Mode 5
   - Scrapes quiz questions
   - Creates answer template
   - Auto-fills answers

### Modified Files / File đã chỉnh sửa:
1. **`main.py`** - Added Mode 5 to menu and routing
2. **`HUONG_DAN_SU_DUNG.md`** - Updated documentation with Mode 5 guide

---

## 🔧 Technical Details / Chi tiết kỹ thuật

### Functions in `quiz_solve_and_fill.py`:
- `scrape_quiz_for_solving()` - Scrapes quiz and returns question data
- `create_answer_template()` - Creates template file for user to fill answers
- `parse_answer_file()` - Parses filled answer file
- `autofill_quiz_with_answers()` - Automatically fills quiz with answers
- `quiz_solve_and_fill()` - Main orchestrator function

### Workflow:
1. User enters URL once
2. Scrape entire quiz (all pages)
3. Save questions to `*_CAU_HOI_*.md`
4. Create answer template `*_DAP_AN_*.md`
5. Wait for user to fill answers
6. Parse filled answers
7. Auto-fill quiz using the same URL

---

## ✅ Benefits / Lợi ích

### Tiếng Việt:
- 🚀 **Tiện lợi hơn**: Chỉ nhập URL 1 lần thay vì 2-3 lần như trước
- ⏱️ **Tiết kiệm thời gian**: Không phải copy-paste URL nhiều lần
- 🎯 **Chính xác hơn**: Sử dụng cùng một session, không lo lỗi URL
- 📝 **Dễ sử dụng**: Quy trình tự động từ đầu đến cuối

### English:
- 🚀 **More convenient**: Only enter URL once instead of 2-3 times
- ⏱️ **Time-saving**: No need to copy-paste URL multiple times
- 🎯 **More accurate**: Uses same session, no URL errors
- 📝 **Easier to use**: Automated workflow from start to finish

---

## 🎓 Example / Ví dụ

```bash
$ python main.py

==================================================
==      EHOU AUTOMATION SUITE      ==
==================================================
1. Xem điểm tổng hợp các môn học
2. Cào đề thi (chưa có đáp án) từ link Attempt
3. Cào và lưu trữ đề thi từ link Review (có đáp án)
4. Tự động làm bài từ file đề thi đã lưu
5. Cào đề -> Giải offline -> Tự động điền (Chỉ nhập URL 1 lần)
0. Thoát chương trình
==================================================

[?] Vui lòng chọn chức năng: 5

======================================================================
--- Chức năng 5: Cào đề -> Giải -> Tự động điền đáp án ---
======================================================================

[?] Nhập URL trang làm bài thi (attempt.php): https://...

[BƯỚC 1] Đang cào đề thi...
[*] Đang cào dữ liệu từ Trang 1...
[*] Đang cào dữ liệu từ Trang 2...
[+] Đã lưu đề thi tại: ./MODE5_CAU_HOI.md

[BƯỚC 2] Đang tạo file template đáp án...
[+] Đã tạo file đáp án tại: ./MODE5_DAP_AN.md

======================================================================
[HƯỚNG DẪN]
1. Mở file: MODE5_CAU_HOI.md
   -> Đọc và giải đề thi

2. Mở file: MODE5_DAP_AN.md
   -> Điền đáp án theo hướng dẫn trong file
   -> Trắc nghiệm: Thay [ ] thành [x] ở đáp án đúng
   -> Điền từ: Thay [[]] thành [[đáp án]]

3. LƯU FILE ĐÁP ÁN sau khi điền xong

4. Quay lại đây và nhấn Enter để tiếp tục tự động điền
======================================================================

[Nhấn Enter khi bạn đã điền xong đáp án và lưu file...]

[BƯỚC 3] Đang đọc file đáp án...
[+] Đã đọc được 25 câu hỏi có đáp án.

[BƯỚC 4] Đang tự động điền đáp án vào quiz...
--- Đang xử lý Trang 1 ---
  [*] Đang xử lý câu ID: q123 (Trắc nghiệm)
    -> Đã chọn đáp án: 'Belief'
...
[SUCCESS] ĐÃ HOÀN THÀNH BÀI THI VÀ ĐẾN TRANG REVIEW!

======================================================================
[HOÀN TẤT] Đã hoàn thành quy trình!
======================================================================
```

---

## 📖 Documentation / Tài liệu

Xem chi tiết trong file `HUONG_DAN_SU_DUNG.md` - phần "🌟 PHƯƠNG PHÁP MỚI - SỬ DỤNG MODE 5"

See details in `HUONG_DAN_SU_DUNG.md` - section "🌟 PHƯƠNG PHÁP MỚI - SỬ DỤNG MODE 5"

