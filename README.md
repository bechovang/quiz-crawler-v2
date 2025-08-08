# EHOU Automation Suite

Một bộ công cụ dòng lệnh được viết bằng Python để tự động hóa các tác vụ lặp đi lặp lại trên hệ thống E-learning của Trường Đại học Mở Hà Nội (EHOU), giúp sinh viên quản lý việc học hiệu quả và tiết kiệm thời gian.

## Tính năng chính

- **Xem Điểm Tổng Hợp:** Tự động đăng nhập, truy cập vào từng môn học và tổng hợp điểm tổng kết của tất cả các môn vào một bảng Markdown gọn gàng.
- **Lưu trữ Đề thi:** Từ một URL xem lại (review) bài thi đã làm, công cụ sẽ cào toàn bộ câu hỏi (bao gồm cả trắc nghiệm và điền từ) và đáp án đúng, sau đó lưu lại dưới dạng một file Markdown có cấu trúc chuẩn.
- **Tự động Làm bài:** Sử dụng một file Markdown đề thi đã được lưu trước đó để tự động điền đáp án cho một lần làm bài thi mới, giúp ôn tập và kiểm tra lại kiến thức một cách nhanh chóng.

## Cảnh báo

- Công cụ này được tạo ra với mục đích học tập và nghiên cứu về tự động hóa web (web automation) và web scraping.
- Người dùng chịu hoàn toàn trách nhiệm về việc sử dụng công cụ này. Việc lạm dụng có thể vi phạm quy định của nhà trường.
- Hãy sử dụng một cách có trách nhiệm, ví dụ như để tự động hóa các tác vụ nhàm chán, không phải để gian lận.
- Nhà phát triển không chịu trách nhiệm cho bất kỳ hậu quả nào phát sinh từ việc sử dụng phần mềm này.

## Cài đặt

Dự án này yêu cầu Python 3.8 trở lên.

1.  **Clone repository về máy của bạn:**
    ```bash
    git clone https://your-repository-url/ehou_automation_suite.git
    cd ehou_automation_suite
    ```

2.  **Tạo và kích hoạt môi trường ảo (khuyến khích):**
    ```bash
    # Trên Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Trên macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Cài đặt các thư viện cần thiết:**
    ```bash
    pip install -r requirements.txt
    ```

## Hướng dẫn sử dụng

Chạy chương trình chính từ terminal:

```bash
python main.py




------------


- Giữ nguyên tất cả định dạng Markdown gốc (dấu thăng, dấu sao, trích dẫn, v.v.).
- Ngôn ngữ sử dụng trong toàn bộ quá trình là Tiếng Việt.

---

### **VÍ DỤ CỤ THỂ**

**VÍ DỤ 1: CÂU HỎI TRẮC NGHIỆM**

**Input của người dùng:**
```markdown
### ID: q6
### Loại: Trắc nghiệm

#### Nội dung:
> Look at the text in the following question. What does Dan have to do? Choose the best answer.Dan, Don’t forget to put your football shirt in the washing machine as soon as you get home from the match. Add soap powder and turn dial to number 3. Mum

#### Đáp án:
- [ ] a. Remember to wash his football shirt after the match.
- [ ] b. Remember where he put the football shirt that he needs for the match.
- [ ] c. Dan’s mum asked him not to put his shirt in the washing machine.
- [ ] d. Remember to make sure his football shirt is clean in time for the match
```

**Output chính xác của bạn:**
```markdown
### ID: q6
### Loại: Trắc nghiệm

#### Nội dung:
> Look at the text in the following question. What does Dan have to do? Choose the best answer.Dan, Don’t forget to put your football shirt in the washing machine as soon as you get home from the match. Add soap powder and turn dial to number 3. Mum

#### Đáp án:
- [x] a. Remember to wash his football shirt after the match.
- [ ] b. Remember where he put the football shirt that he needs for the match.
- [ ] c. Dan’s mum asked him not to put his shirt in the washing machine.
- [ ] d. Remember to make sure his football shirt is clean in time for the match
```

---

**VÍ DỤ 2: CÂU HỎI ĐIỀN TỪ**

**Input của người dùng:**
```markdown
### ID: q1
### Loại: Điền từ

#### Nội dung:
> 1. ☐ The writer wrote the article to encourage us to work more and relax less.
> 2. ☐ People today are having a less stressful life than they did in the past.

#### Đáp án:
> [[]] [[]]
```

**Output chính xác của bạn:**
```markdown
### ID: q1
### Loại: Điền từ

#### Nội dung:
> 1. [F] The writer wrote the article to encourage us to work more and relax less.
> 2. [F] People today are having a less stressful life than they did in the past.

#### Đáp án:
> [[F]] [[F]]
```