# features/quiz_autofiller.py

import re
from core.ehou_client import EhouClient
from core.quiz_parser import QuizParser
from config import settings

def parse_markdown_answers(filepath: str) -> dict:
    """Phân tích file markdown và trả về một ngân hàng đáp án."""
    answer_bank = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"[-] Lỗi: Không tìm thấy file {filepath}")
        return {}

    question_blocks = content.split('---')

    for block in question_blocks:
        if not block.strip(): continue

        id_match = re.search(r'### ID: (q\d+)', block)
        type_match = re.search(r'### Loại: (Trắc nghiệm|Điền từ)', block)

        if not (id_match and type_match): continue
        
        q_id = id_match.group(1)
        q_type = type_match.group(1)
        
        solution = {'type': q_type}

        if q_type == 'Trắc nghiệm':
            correct_answer_match = re.search(r'-\s*\[x\]\s*(.*)', block)
            if correct_answer_match:
                solution['answer'] = correct_answer_match.group(1).strip()
        
        elif q_type == 'Điền từ':
            content_match = re.search(r'#### Nội dung:\s*>\s*(.*)', block, re.DOTALL)
            if content_match:
                # Tìm đáp án từ phần #### Đáp án:
                answer_match = re.search(r'#### Đáp án:\s*>\s*(.*?)(?:\n|$)', block, re.DOTALL)
                if answer_match:
                    # Tách các đáp án từ format [[]] [[]] [[]]
                    answers_text = answer_match.group(1).strip()
                    answers = re.findall(r'\[\[(.*?)\]\]', answers_text)
                    if answers:
                        solution['answers'] = answers
                    else:
                        # Nếu không có đáp án trong [[]], thử tìm từ nội dung
                        answers = re.findall(r'\[\[(.*?)\]\]', content_match.group(1))
                        solution['answers'] = answers
        
        if len(solution) > 1: # Đảm bảo có dữ liệu đáp án
            answer_bank[q_id] = solution
    
    print(f"[+] Đã phân tích xong file, tìm thấy đáp án cho {len(answer_bank)} câu hỏi.")
    return answer_bank


def autofill_quiz(client: EhouClient):
    """Tự động điền đáp án cho bài quiz từ file Markdown."""
    print("\n--- Chức năng 3: Tự động làm bài từ file đã lưu ---")

    quiz_url = input("[?] Nhập URL trang làm bài thi (attempt.php): ")
    if "attempt.php" not in quiz_url:
        print("[-] URL không hợp lệ.")
        return
        
    markdown_path = input("[?] Nhập đường dẫn đến file .md chứa đề thi: ")

    answer_bank = parse_markdown_answers(markdown_path)
    if not answer_bank:
        return
        
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
                    print(f"    -> Đáp án: {answers}")
                    print(f"    -> Ô trống: {input_names}")

        # Nộp trang và lấy HTML trang tiếp theo
        print(f"[*] Đang submit trang {page_count}...")
        print(f"[*] Payload keys: {list(payload.keys())[:5]}...")  # Debug: in ra một số key của payload
        response = client.post_data(settings.EHOU_PROCESS_ATTEMPT_URL, payload)
        
        if not response:
            print("[-] Gửi yêu cầu thất bại. Dừng chương trình.")
            print("[-] Có thể do:")
            print("  - Kết nối internet không ổn định")
            print("  - Session đã hết hạn")
            print("  - URL không hợp lệ")
            break
            
        # Kiểm tra URL response để xác định trạng thái
        if "/quiz/review.php" in response.url:
            print("\n[SUCCESS] ĐÃ HOÀN THÀNH BÀI THI VÀ ĐẾN TRANG REVIEW!")
            print(f"Trang review: {response.url}")
            break
            
        elif "/quiz/summary.php" in response.url:
            print("\n[+] Đã đến trang tóm tắt. Chuẩn bị nộp bài cuối cùng...")
            
            # Xử lý nộp bài cuối cùng từ trang tóm tắt
            summary_html = response.text
            summary_parser = QuizParser(summary_html)
            final_payload = summary_parser.extract_form_data()
            
            if not final_payload:
                print("[-] Không thể trích xuất form data từ trang tóm tắt.")
                print("[-] Có thể trang tóm tắt không có form submit.")
                print("[*] Bạn có thể vào link trang tóm tắt để nộp thủ công:")
                print(f"    {response.url}")
                break
                
            user_choice = input("[?] Bạn có muốn NỘP BÀI VÀ KẾT THÚC không? (y/n): ").lower()
            if user_choice == 'y':
                print("[*] Đang nộp bài cuối cùng...")
                final_response = client.post_data(settings.EHOU_PROCESS_ATTEMPT_URL, final_payload)
                
                if final_response and "/quiz/review.php" in final_response.url:
                    print("\n[SUCCESS] ĐÃ NỘP BÀI THÀNH CÔNG!")
                    print(f"Trang review: {final_response.url}")
                else:
                    print("[-] Nộp bài cuối cùng thất bại.")
                    if final_response:
                        print(f"URL response: {final_response.url}")
            else:
                print("[*] Đã hủy nộp bài. Bạn có thể vào link trang tóm tắt để nộp thủ công.")
            break # Kết thúc vòng lặp
            
        else:
            # Chuyển sang trang tiếp theo
            print(f"[+] Đã submit trang {page_count} thành công, chuyển sang trang tiếp theo...")
            current_html = response.text
            page_count += 1