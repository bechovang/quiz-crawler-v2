# features/quiz_scraper.py

import re
from bs4 import BeautifulSoup, Tag
from core.ehou_client import EhouClient

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

def scrape_quiz(client: EhouClient):
    """Cào dữ liệu từ URL trang review và lưu thành file Markdown."""
    print("\n--- Chức năng 3: Cào và lưu trữ đề thi từ link Review ---")
    
    review_url = input("[?] Nhập URL trang review bài thi (review.php): ")
    if "review.php" not in review_url:
        print("[-] URL không hợp lệ.")
        return

    html_content = client.get_page_content(review_url)
    if not html_content:
        return

    soup = BeautifulSoup(html_content, 'lxml')

    # Trích xuất thông tin chung
    course_name = clean_text(soup.select_one('.breadcrumb a[href*="/course/view.php"]').get_text()) if soup.select_one('.breadcrumb a[href*="/course/view.php"]') else "Không xác định"
    quiz_name = clean_text(soup.find('title').get_text()) if soup.find('title') else "Đề thi"
    
    markdown_output = f"# [META] Môn học: {course_name}\n"
    markdown_output += f"# [META] Tên bài thi: {quiz_name}\n"
    markdown_output += f"# [META] URL Review: {review_url}\n"

    question_divs = soup.select('div.que')
    if not question_divs:
        print("[-] Không tìm thấy câu hỏi nào trên trang.")
        return
        
    print(f"[*] Tìm thấy {len(question_divs)} câu hỏi. Bắt đầu xử lý...")

    for q_div in question_divs:
        if not isinstance(q_div, Tag): continue
        
        q_id = q_div.get('id', '')
        markdown_output += f"\n---\n### ID: {q_id}\n"

        if 'multichoice' in q_div.get('class', []):
            markdown_output += "### Loại: Trắc nghiệm\n"
            
            qtext_el = q_div.select_one('.qtext')
            markdown_output += f"\n#### Nội dung:\n> {clean_text(qtext_el.get_text())}\n" if qtext_el else ""

            markdown_output += "\n#### Đáp án:\n"
            answer_els = q_div.select('.answer div[class^="r"]')
            for ans_el in answer_els:
                label_text = clean_text(ans_el.find('label').get_text()) if ans_el.find('label') else ""
                is_correct = 'correct' in ans_el.get('class', [])
                prefix = "- [x]" if is_correct else "- [ ]"
                markdown_output += f"{prefix} {label_text}\n"

        elif 'gapfill' in q_div.get('class', []):
            markdown_output += "### Loại: Điền từ\n"
            
            formulation_el = q_div.select_one('.formulation')
            if formulation_el:
                # Tạo bản sao để chỉnh sửa
                formulation_clone = BeautifulSoup(str(formulation_el), 'lxml').div
                
                for input_tag in formulation_clone.select('input.droptarget, input[type="text"]'):
                    correct_value = input_tag.get('value', '').strip()
                    input_tag.replace_with(f"[[{correct_value}]]")
                
                full_text = clean_text(formulation_clone.get_text())
                markdown_output += f"\n#### Nội dung:\n> {full_text}\n"
        
        else:
            markdown_output += "### Loại: Không xác định\n"

    # Chuyển đổi tiếng Việt có dấu thành không dấu trước khi tạo tên file
    clean_quiz_name = remove_vietnamese_diacritics(quiz_name)
    safe_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', clean_quiz_name)
    output_filename = f"{safe_filename}.md"
    
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(markdown_output)
        print(f"\n[+] Đã cào đề thi thành công! File đã được lưu tại: ./{output_filename}")
    except Exception as e:
        print(f"\n[-] Lỗi khi lưu file: {e}")