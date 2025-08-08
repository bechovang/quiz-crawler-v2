# features/scrape_questions.py

import re
from bs4 import BeautifulSoup, Tag
from core.ehou_client import EhouClient
from core.quiz_parser import QuizParser
from config import settings

def remove_vietnamese_diacritics(text: str) -> str:
    """Chuyển đổi tiếng Việt có dấu thành không dấu."""
    vietnamese_map = {
        'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
        'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
        'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
        'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
        'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
        'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
        'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
        'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
        'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
        'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
        'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
        'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y',
        'đ': 'd',
        'À': 'A', 'Á': 'A', 'Ả': 'A', 'Ã': 'A', 'Ạ': 'A',
        'Ă': 'A', 'Ằ': 'A', 'Ắ': 'A', 'Ẳ': 'A', 'Ẵ': 'A', 'Ặ': 'A',
        'Â': 'A', 'Ầ': 'A', 'Ấ': 'A', 'Ẩ': 'A', 'Ẫ': 'A', 'Ậ': 'A',
        'È': 'E', 'É': 'E', 'Ẻ': 'E', 'Ẽ': 'E', 'Ẹ': 'E',
        'Ê': 'E', 'Ề': 'E', 'Ế': 'E', 'Ể': 'E', 'Ễ': 'E', 'Ệ': 'E',
        'Ì': 'I', 'Í': 'I', 'Ỉ': 'I', 'Ĩ': 'I', 'Ị': 'I',
        'Ò': 'O', 'Ó': 'O', 'Ỏ': 'O', 'Õ': 'O', 'Ọ': 'O',
        'Ô': 'O', 'Ồ': 'O', 'Ố': 'O', 'Ổ': 'O', 'Ỗ': 'O', 'Ộ': 'O',
        'Ơ': 'O', 'Ờ': 'O', 'Ớ': 'O', 'Ở': 'O', 'Ỡ': 'O', 'Ợ': 'O',
        'Ù': 'U', 'Ú': 'U', 'Ủ': 'U', 'Ũ': 'U', 'Ụ': 'U',
        'Ư': 'U', 'Ừ': 'U', 'Ứ': 'U', 'Ử': 'U', 'Ữ': 'U', 'Ự': 'U',
        'Ỳ': 'Y', 'Ý': 'Y', 'Ỷ': 'Y', 'Ỹ': 'Y', 'Ỵ': 'Y',
        'Đ': 'D'
    }
    
    for vietnamese_char, ascii_char in vietnamese_map.items():
        text = text.replace(vietnamese_char, ascii_char)
    
    return text

def clean_text(text: str) -> str:
    """Loại bỏ các khoảng trắng thừa và ký tự xuống dòng."""
    if not text:
        return ""
    return ' '.join(text.strip().split())

def scrape_questions_to_markdown(client: EhouClient):
    """
    Truy cập vào một bài thi đang làm, cào tất cả câu hỏi qua các trang
    và lưu thành file Markdown chưa có đáp án.
    """
    print("\n--- Chức năng 2: Cào đề thi (chưa có đáp án) ---")
    
    quiz_url = input("[?] Nhập URL trang làm bài thi (attempt.php): ")
    if "attempt.php" not in quiz_url:
        print("[-] URL không hợp lệ.")
        return

    # --- Bắt đầu vòng lặp qua các trang để cào ---
    current_html = client.get_page_content(quiz_url)
    if not current_html:
        print("[-] Không thể truy cập trang bài thi.")
        return
        
    page_count = 1
    markdown_output = ""
    
    # Lấy thông tin chung từ trang đầu tiên
    soup = BeautifulSoup(current_html, 'lxml')
    course_name = clean_text(soup.select_one('.breadcrumb a[href*="/course/view.php"]').get_text()) if soup.select_one('.breadcrumb a[href*="/course/view.php"]') else "Không xác định"
    quiz_name = clean_text(soup.find('title').get_text()) if soup.find('title') else "Đề thi"
    
    markdown_output += f"# [META] Môn học: {course_name}\n"
    markdown_output += f"# [META] Tên bài thi: {quiz_name}\n"
    markdown_output += f"# [META] URL Attempt: {quiz_url}\n"

    while current_html:
        print(f"[*] Đang cào dữ liệu từ Trang {page_count}...")
        parser = QuizParser(current_html)
        
        questions_on_page = parser.extract_questions()
        if not questions_on_page:
            print("[*] Không tìm thấy câu hỏi nào trên trang này. Kết thúc cào đề.")
            break

        # Xử lý từng câu hỏi trên trang
        for q_on_page in questions_on_page:
            q_id = q_on_page.get('id', '')
            if not q_id: continue

            markdown_output += f"\n---\n### ID: {q_id}\n"
            markdown_output += f"### Loại: {q_on_page['type']}\n"
            markdown_output += f"\n#### Nội dung:\n> {q_on_page['text']}\n"

            if q_on_page['type'] == 'Trắc nghiệm':
                markdown_output += "\n#### Đáp án:\n"
                for option in q_on_page.get('options', []):
                    markdown_output += f"- [ ] {option}\n"
            
            elif q_on_page['type'] == 'Điền từ':
                # Tạo placeholder cho các ô trống
                input_count = len(q_on_page.get('input_names', []))
                if input_count > 0:
                    placeholders = " ".join(["[[]]" for _ in range(input_count)])
                    markdown_output += f"\n#### Đáp án:\n> {placeholders}\n"
                else:
                    markdown_output += "\n#### Đáp án:\n> [Cần điền thủ công]\n"
                
                # Thêm hướng dẫn nếu nội dung trống
                if not q_on_page.get('text', '').strip():
                    markdown_output += "\n#### Ghi chú:\n> [Cần xem trực tiếp trên trang web để điền đáp án]\n"
                else:
                    # Thêm hướng dẫn về cách điền đáp án
                    markdown_output += "\n#### Hướng dẫn:\n> Thay thế ☐ bằng đáp án đúng (T/F hoặc từ phù hợp), giữ nguyên vị trí\n"

        # Chuẩn bị để chuyển trang tiếp theo
        payload = parser.extract_form_data()
        
        # Kiểm tra xem có nút "Next" không
        soup = BeautifulSoup(current_html, 'lxml')
        next_button = soup.find('input', {'name': 'next'})
        
        if not next_button:
            print("[*] Đã cào đến trang cuối cùng.")
            break

        response = client.post_data(settings.EHOU_PROCESS_ATTEMPT_URL, payload)
        
        if not response:
            print("[-] Gửi yêu cầu thất bại. Dừng cào đề.")
            break
            
        if "/summary.php" in response.url:
            print("[*] Đã đến trang tóm tắt. Kết thúc cào đề.")
            break
            
        current_html = response.text
        page_count += 1
        
    # --- Lưu file ---
    clean_quiz_name = remove_vietnamese_diacritics(quiz_name)
    safe_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', clean_quiz_name)
    output_filename = f"{safe_filename}_CHUA_CO_DAP_AN.md"
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(markdown_output)
        print("\n[SUCCESS] Đã cào xong đề thi!")
        print(f"[+] File đã được lưu tại: ./{output_filename}")
        print("[!] Mở file này và tự điền đáp án đúng trước khi sử dụng chức năng tự động làm bài.")
    except Exception as e:
        print(f"\n[-] Lỗi khi lưu file: {e}") 