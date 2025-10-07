# features/quiz_solve_and_fill.py

import re
from bs4 import BeautifulSoup
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

def scrape_quiz_for_solving(client: EhouClient, quiz_url: str) -> tuple:
    """
    Cào đề thi và trả về (markdown_content, quiz_name, course_name, all_questions_data).
    all_questions_data: dict chứa thông tin câu hỏi để sử dụng khi auto-fill
    """
    current_html = client.get_page_content(quiz_url)
    if not current_html:
        print("[-] Không thể truy cập trang bài thi.")
        return None, None, None, None
        
    page_count = 1
    markdown_output = ""
    all_questions_data = {}  # Lưu trữ thông tin câu hỏi để dùng cho auto-fill
    
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
            if not q_id: 
                continue

            # Lưu thông tin câu hỏi để sử dụng sau này
            all_questions_data[q_id] = q_on_page

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
    
    return markdown_output, quiz_name, course_name, all_questions_data

def create_answer_template(quiz_name: str, all_questions_data: dict) -> str:
    """Tạo file template để user điền đáp án."""
    template = f"# TEMPLATE ĐÁP ÁN - {quiz_name}\n\n"
    template += "# HƯỚNG DẪN:\n"
    template += "# 1. Với câu trắc nghiệm: Thay [ ] thành [x] ở đáp án đúng\n"
    template += "# 2. Với câu điền từ: Thay [[]] thành [[đáp án]] theo thứ tự\n"
    template += "# 3. SAU KHI ĐIỀN XONG, LƯU FILE NÀY VÀ CHỌN TIẾP TỤC TRONG CHƯƠNG TRÌNH\n\n"
    
    for q_id, q_data in all_questions_data.items():
        template += f"\n---\n### ID: {q_id}\n"
        template += f"### Loại: {q_data['type']}\n"
        template += f"\n#### Nội dung:\n> {q_data['text']}\n"
        
        if q_data['type'] == 'Trắc nghiệm':
            template += "\n#### Đáp án:\n"
            for option in q_data.get('options', []):
                template += f"- [ ] {option}\n"
        
        elif q_data['type'] == 'Điền từ':
            input_count = len(q_data.get('input_names', []))
            if input_count > 0:
                placeholders = " ".join(["[[]]" for _ in range(input_count)])
                template += f"\n#### Đáp án:\n> {placeholders}\n"
            else:
                template += "\n#### Đáp án:\n> [Cần điền thủ công]\n"
    
    return template

def parse_answer_file(filepath: str) -> dict:
    """Phân tích file đáp án và trả về một ngân hàng đáp án."""
    answer_bank = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"[-] Lỗi: Không tìm thấy file {filepath}")
        return {}

    question_blocks = content.split('---')

    for block in question_blocks:
        if not block.strip(): 
            continue

        id_match = re.search(r'### ID:\s*(q\d+)', block)
        type_match = re.search(r'### Loại:\s*(Trắc nghiệm|Điền từ)', block)

        if not (id_match and type_match): 
            continue
        
        q_id = id_match.group(1)
        q_type = type_match.group(1)
        
        solution = {'type': q_type}

        if q_type == 'Trắc nghiệm':
            # Cải thiện regex để bắt cả [x] và [X], và xử lý nhiều định dạng
            correct_answer_match = re.search(r'-\s*\[[xX]\]\s*(.*?)(?:\n|$)', block, re.IGNORECASE)
            if correct_answer_match:
                answer_text = correct_answer_match.group(1).strip()
                solution['answer'] = answer_text
            else:
                # Thử tìm với định dạng khác (có thể có nhiều khoảng trắng)
                alt_match = re.search(r'[-•]\s*\[\s*[xX]\s*\]\s*(.*?)(?:\n|$)', block)
                if alt_match:
                    answer_text = alt_match.group(1).strip()
                    solution['answer'] = answer_text
        
        elif q_type == 'Điền từ':
            content_match = re.search(r'#### Nội dung:\s*>\s*(.*)', block, re.DOTALL)
            if content_match:
                # Tìm đáp án từ phần #### Đáp án:
                answer_match = re.search(r'#### Đáp án:\s*>\s*(.*?)(?:\n####|\n---|\Z)', block, re.DOTALL)
                if answer_match:
                    # Tách các đáp án từ format [[]] [[]] [[]]
                    answers_text = answer_match.group(1).strip()
                    answers = re.findall(r'\[\[(.*?)\]\]', answers_text)
                    if answers:
                        solution['answers'] = answers
        
        if len(solution) > 1:  # Đảm bảo có dữ liệu đáp án
            answer_bank[q_id] = solution
    
    return answer_bank

def autofill_quiz_with_answers(client: EhouClient, quiz_url: str, answer_bank: dict):
    """Tự động điền đáp án cho bài quiz."""
    current_html = client.get_page_content(quiz_url)
    page_count = 1
    
    while current_html:
        print(f"\n--- Đang xử lý Trang {page_count} ---")
        parser = QuizParser(current_html)
        payload = parser.extract_form_data()
        
        if not payload:
            print("[*] Không tìm thấy form trên trang. Có thể đã đến trang tóm tắt.")
            break

        questions_on_page = parser.extract_questions()
        if not questions_on_page:
            print("[*] Không tìm thấy câu hỏi nào. Chuyển tiếp...")
        
        for q_on_page in questions_on_page:
            q_id = q_on_page.get('id')
            solution = answer_bank.get(q_id)
            
            if not solution:
                print(f"  [!] Không tìm thấy đáp án cho câu ID: {q_id}. Bỏ qua.")
                continue

            print(f"  [*] Đang xử lý câu ID: {q_id} ({solution.get('type')})")
            
            if solution['type'] == 'Trắc nghiệm':
                correct_answer_text = solution.get('answer', '').lower()
                for i, option_text in enumerate(q_on_page.get('options', [])):
                    if option_text.lower() == correct_answer_text:
                        payload[q_on_page['input_name']] = i
                        print(f"    -> Đã chọn đáp án: '{option_text[:50]}...'")
                        break
            
            elif solution['type'] == 'Điền từ':
                answers = solution.get('answers', [])
                input_names = q_on_page.get('input_names', [])
                if len(answers) == len(input_names):
                    for name, answer in zip(input_names, answers):
                        payload[name] = answer
                    print(f"    -> Đã điền {len(answers)} ô trống: {answers}")
                else:
                    print(f"    -> Lỗi: Số đáp án ({len(answers)}) không khớp số ô trống ({len(input_names)}).")

        # Nộp trang và lấy HTML trang tiếp theo
        print(f"[*] Đang submit trang {page_count}...")
        
        response = client.post_data(settings.EHOU_PROCESS_ATTEMPT_URL, payload)
        
        if not response:
            print("[-] Gửi yêu cầu thất bại. Dừng chương trình.")
            break
            
        # Kiểm tra URL response để xác định trạng thái
        if "/quiz/review.php" in response.url:
            print("\n[SUCCESS] ĐÃ HOÀN THÀNH BÀI THI VÀ ĐẾN TRANG REVIEW!")
            print(f"Trang review: {response.url}")
            break
            
        elif "/quiz/summary.php" in response.url:
            print("\n[+] Đã đến trang tóm tắt. Tự động nộp bài cuối cùng...")
            
            # Xử lý nộp bài cuối cùng từ trang tóm tắt
            summary_html = response.text
            summary_parser = QuizParser(summary_html)
            
            final_payload = summary_parser.extract_summary_form_data()
            
            if not final_payload:
                final_payload = summary_parser.extract_form_data()
                
            if not final_payload:
                print("[-] Không thể trích xuất form data từ trang tóm tắt.")
                print(f"[*] Bạn có thể vào link trang tóm tắt để nộp thủ công: {response.url}")
                break
                
            # Tìm nút submit phù hợp
            submit_button_name = summary_parser.find_submit_button()
            if submit_button_name and submit_button_name not in final_payload:
                final_payload[submit_button_name] = 'Nộp bài và kết thúc'
            elif 'submit' not in final_payload:
                final_payload['submit'] = 'Nộp bài và kết thúc'
                
            print("[*] Đang nộp bài cuối cùng...")
            
            final_response = client.post_data(settings.EHOU_PROCESS_ATTEMPT_URL, final_payload)
            
            if final_response and "/quiz/review.php" in final_response.url:
                print("\n[SUCCESS] ĐÃ NỘP BÀI THÀNH CÔNG!")
                print(f"Trang review: {final_response.url}")
            else:
                print("[-] Nộp bài cuối cùng thất bại.")
                if final_response:
                    print(f"URL response: {final_response.url}")
                print(f"[*] Bạn có thể vào link trang tóm tắt để nộp thủ công: {response.url}")
            break
            
        else:
            # Chuyển sang trang tiếp theo
            print(f"[+] Đã submit trang {page_count} thành công, chuyển sang trang tiếp theo...")
            current_html = response.text
            page_count += 1

def quiz_solve_and_fill(client: EhouClient):
    """
    Chức năng mode 5: Cào đề, lưu file để giải, tạo template đáp án, 
    sau đó tự động điền đáp án khi user đã hoàn thành.
    """
    print("\n" + "="*70)
    print("--- Chức năng 5: Cào đề -> Giải -> Tự động điền đáp án ---")
    print("="*70)
    
    quiz_url = input("[?] Nhập URL trang làm bài thi (attempt.php): ")
    if "attempt.php" not in quiz_url:
        print("[-] URL không hợp lệ.")
        return
    
    # Bước 1: Cào đề thi
    print("\n[BƯỚC 1] Đang cào đề thi...")
    markdown_content, quiz_name, course_name, all_questions_data = scrape_quiz_for_solving(client, quiz_url)
    
    if not markdown_content or not all_questions_data:
        print("[-] Cào đề thi thất bại.")
        return
    
    # Tạo tên file cố định cho Mode 5 (ghi đè mỗi lần chạy)
    questions_filename = "MODE5_CAU_HOI.md"
    answer_filename = "MODE5_DAP_AN.md"
    
    # Lưu file câu hỏi để user đọc/giải
    try:
        with open(questions_filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"[+] Đã lưu đề thi tại: ./{questions_filename}")
    except Exception as e:
        print(f"[-] Lỗi khi lưu file câu hỏi: {e}")
        return
    
    # Bước 2: Tạo file template đáp án
    print("\n[BƯỚC 2] Đang tạo file template đáp án...")
    answer_template = create_answer_template(quiz_name, all_questions_data)
    try:
        with open(answer_filename, 'w', encoding='utf-8') as f:
            f.write(answer_template)
        print(f"[+] Đã tạo file đáp án tại: ./{answer_filename}")
    except Exception as e:
        print(f"[-] Lỗi khi tạo file đáp án: {e}")
        return
    
    # Bước 3: Hướng dẫn user
    print("\n" + "="*70)
    print("[HƯỚNG DẪN]")
    print(f"1. Mở file: {questions_filename}")
    print(f"   -> Đọc và giải đề thi")
    print(f"\n2. Mở file: {answer_filename}")
    print(f"   -> Điền đáp án theo hướng dẫn trong file")
    print(f"   -> Trắc nghiệm: Thay [ ] thành [x] ở đáp án đúng")
    print(f"   -> Điền từ: Thay [[]] thành [[đáp án]]")
    print(f"\n3. LƯU FILE ĐÁP ÁN sau khi điền xong")
    print(f"\n4. Quay lại đây và nhấn Enter để tiếp tục tự động điền")
    print("="*70)
    
    input("\n[Nhấn Enter khi bạn đã điền xong đáp án và lưu file...]")
    
    # Bước 4: Đọc file đáp án và tự động điền
    print("\n[BƯỚC 3] Đang đọc file đáp án...")
    answer_bank = parse_answer_file(answer_filename)
    
    if not answer_bank:
        print("[-] Không tìm thấy đáp án nào trong file. Vui lòng kiểm tra lại file đáp án.")
        return
    
    print(f"[+] Đã đọc được {len(answer_bank)} câu hỏi có đáp án.")
    
    # Bước 5: Tự động điền đáp án vào quiz
    print("\n[BƯỚC 4] Đang tự động điền đáp án vào quiz...")
    autofill_quiz_with_answers(client, quiz_url, answer_bank)
    
    print("\n" + "="*70)
    print("[HOÀN TẤT] Đã hoàn thành quy trình!")
    print("="*70)

