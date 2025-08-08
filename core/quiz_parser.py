# core/quiz_parser.py

from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Any

class QuizParser:
    """Phân tích HTML của trang quiz để trích xuất thông tin cần thiết."""

    def __init__(self, html_content: str):
        self.soup = BeautifulSoup(html_content, 'lxml')

    def extract_form_data(self) -> Dict[str, Any]:
        """Trích xuất tất cả dữ liệu ẩn và các trường cần thiết từ form câu hỏi."""
        form_data = {}
        response_form = self.soup.find('form', id='responseform')
        if not isinstance(response_form, Tag):
            return {}
            
        # Lấy tất cả các thẻ input (bao gồm cả hidden, radio, checkbox, text)
        inputs = response_form.find_all('input')
        for input_tag in inputs:
            if isinstance(input_tag, Tag):
                name = input_tag.get('name')
                value = input_tag.get('value', '')
                input_type = input_tag.get('type')

                if not name:
                    continue
                
                # Chỉ lấy các giá trị của hidden, text, và radio/checkbox đã được chọn
                if input_type in ['hidden', 'text', 'submit']:
                    form_data[name] = value
                elif input_type in ['radio', 'checkbox'] and input_tag.has_attr('checked'):
                     form_data[name] = value
                        
        return form_data

    def extract_questions(self) -> List[Dict[str, Any]]:
        """Trích xuất thông tin chi tiết của tất cả câu hỏi trên trang."""
        questions = []
        question_divs = self.soup.select('div.que')

        for q_div in question_divs:
            if not isinstance(q_div, Tag):
                continue
            
            q_data = {}
            q_id = q_div.get('id', '')
            q_data['id'] = q_id

            qtext_el = q_div.select_one('.qtext')
            q_data['text'] = ' '.join(qtext_el.get_text().strip().split()) if qtext_el else ""

            if 'multichoice' in q_div.get('class', []):
                q_data['type'] = 'Trắc nghiệm'
                options = []
                option_labels = q_div.select('.answer div[class^="r"] label')
                for opt_label in option_labels:
                    if isinstance(opt_label, Tag):
                        options.append(' '.join(opt_label.get_text().strip().split()))
                q_data['options'] = options
                
                # Tìm name của radio button
                radio_input = q_div.find('input', {'type': 'radio'})
                q_data['input_name'] = radio_input.get('name', '') if radio_input else ''

            elif 'gapfill' in q_div.get('class', []):
                q_data['type'] = 'Điền từ'
                input_names = []
                input_tags = q_div.select('.formulation input.droptarget, .formulation input[type="text"]')
                for input_tag in input_tags:
                    if isinstance(input_tag, Tag):
                        input_names.append(input_tag.get('name', ''))
                q_data['input_names'] = input_names
                
                # Lấy nội dung đầy đủ của câu hỏi điền từ
                formulation_el = q_div.select_one('.formulation')
                if formulation_el:
                    # Tạo bản sao HTML để xử lý
                    formulation_html = str(formulation_el)
                    temp_soup = BeautifulSoup(formulation_html, 'lxml')
                    
                    # Thay thế các input bằng placeholder với định dạng checkbox
                    for input_tag in temp_soup.select('input.droptarget, input[type="text"]'):
                        # Thay thế bằng checkbox trống
                        input_tag.replace_with(" ☐ ")
                    
                    # Lấy text đã được xử lý
                    gapfill_text = temp_soup.get_text(separator=' ', strip=True)
                    if gapfill_text:
                        q_data['text'] = gapfill_text
                    else:
                        # Fallback: Lấy text từ toàn bộ div.que
                        que_text = q_div.get_text()
                        if que_text:
                            # Loại bỏ các phần không cần thiết
                            lines = que_text.split('\n')
                            clean_lines = []
                            for line in lines:
                                line = line.strip()
                                if line and not line.startswith('Question') and not line.startswith('ID:'):
                                    clean_lines.append(line)
                            if clean_lines:
                                q_data['text'] = ' '.join(clean_lines)

            else:
                q_data['type'] = 'Không xác định'

            questions.append(q_data)
            
        return questions

    def extract_summary_form_data(self) -> Dict[str, Any]:
        """Trích xuất form data từ trang tóm tắt (summary.php)."""
        form_data = {}
        
        # Tìm form trên trang tóm tắt
        summary_form = self.soup.find('form')
        if not isinstance(summary_form, Tag):
            return {}
            
        # Lấy tất cả các thẻ input
        inputs = summary_form.find_all('input')
        for input_tag in inputs:
            if isinstance(input_tag, Tag):
                name = input_tag.get('name')
                value = input_tag.get('value', '')
                input_type = input_tag.get('type')

                if not name:
                    continue
                
                # Lấy tất cả các trường ẩn và submit
                if input_type in ['hidden', 'submit']:
                    form_data[name] = value
                        
        return form_data

    def find_submit_button(self) -> str:
        """Tìm nút submit trên trang tóm tắt."""
        # Tìm tất cả các button và input submit
        submit_buttons = self.soup.find_all(['button', 'input'], type='submit')
        
        for button in submit_buttons:
            if isinstance(button, Tag):
                # Kiểm tra text hoặc value của button
                button_text = button.get_text(strip=True) or button.get('value', '')
                if any(keyword in button_text.lower() for keyword in ['nộp bài', 'submit', 'finish', 'kết thúc']):
                    return button.get('name', 'submit')
        
        return 'submit'  # Fallback