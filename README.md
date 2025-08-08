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