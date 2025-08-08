# features/grade_viewer.py

import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup, Tag
from core.ehou_client import EhouClient
from config import settings

def view_grades(client: EhouClient):
    """Cào điểm từ trang dashboard bằng cách truy cập vào từng môn học."""
    print("\n--- Chức năng 1: Xem điểm tổng hợp ---")
    
    # 1. Truy cập Dashboard
    dashboard_url = settings.EHOU_MY_COURSES_URL
    print(f"[*] Đang truy cập trang Dashboard: {dashboard_url}")
    html_content = client.get_page_content(dashboard_url)
    if not html_content:
        print("[-] Không thể tải được nội dung trang Dashboard.")
        return

    # 2. Phân tích Dashboard để tìm các khóa học
    print("[*] Đang tìm danh sách các khóa học...")
    soup = BeautifulSoup(html_content, 'lxml')
    course_elements = soup.select('div[data-block="myoverview"] .list-group-item a[href*="/course/view.php"]')
    
    if not course_elements:
        print("[-] Không tìm thấy danh sách khóa học trên Dashboard.")
        return
        
    course_links = [{'name': tag.get_text(strip=True), 'url': tag['href']} for tag in course_elements]
    print(f"[+] Tìm thấy {len(course_links)} khóa học.")
    
    # 3. Vòng lặp qua từng khóa học để lấy điểm
    all_grades_data = []
    for i, course in enumerate(course_links):
        print(f"\n--- [{i+1}/{len(course_links)}] Đang xử lý môn: {course['name']} ---")
        try:
            course_page_html = client.get_page_content(course['url'])
            if not course_page_html: continue
            
            course_soup = BeautifulSoup(course_page_html, 'lxml')
            grade_link_tag = course_soup.select_one('a[href*="/grade/report/user/index.php"]')
            if not isinstance(grade_link_tag, Tag):
                print(f"  [-] Không tìm thấy link 'Điểm' cho môn này.")
                continue
            
            grade_page_url = urljoin(settings.EHOU_BASE_URL, grade_link_tag['href'])
            print(f"  [*] Đang truy cập trang điểm...")

            grade_page_html = client.get_page_content(grade_page_url)
            if not grade_page_html: continue
            
            grade_soup = BeautifulSoup(grade_page_html, 'lxml')
            total_row = grade_soup.select_one('tr.coursetotal, tr.lastrow')
            final_grade = "Chưa có"
            
            if isinstance(total_row, Tag):
                grade_cell = total_row.select_one('td.grade')
                if isinstance(grade_cell, Tag):
                    final_grade = grade_cell.get_text(strip=True)

            print(f"  [+] Điểm tổng kết: {final_grade}")
            all_grades_data.append({'course_name': course['name'], 'final_grade': final_grade})

        except Exception as e:
            print(f"  [-] Đã xảy ra lỗi không mong muốn: {e}")

    # 4. In kết quả
    print("\n" + "="*50)
    print("== BẢNG TỔNG KẾT ĐIỂM CÁC MÔN HỌC ==")
    print("="*50 + "\n")
    
    markdown_output = "| Môn học | Điểm tổng kết |\n"
    markdown_output += "| :--- | :---: |\n"
    
    for item in all_grades_data:
        markdown_output += f"| {item['course_name']} | {item['final_grade']} |\n"
        
    print(markdown_output)
    
    if input("[?] Bạn có muốn lưu kết quả vào file 'diem_so.md' không? (y/n): ").lower() == 'y':
        with open('diem_so.md', 'w', encoding='utf-8') as f:
            f.write(markdown_output)
        print("[+] Đã lưu thành công!")