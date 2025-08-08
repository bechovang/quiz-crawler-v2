# main.py

import sys
from core.ehou_client import EhouClient
from features.grade_viewer import view_grades
from features.quiz_scraper import scrape_quiz
from features.scrape_questions import scrape_questions_to_markdown
from features.quiz_autofiller import autofill_quiz

def show_menu():
    """Hiển thị menu chính và điều hướng chức năng."""
    print("\n" + "="*50)
    print("==      EHOU AUTOMATION SUITE      ==")
    print("="*50)
    print("1. Xem điểm tổng hợp các môn học")
    print("2. Cào đề thi (chưa có đáp án) từ link Attempt")
    print("3. Cào và lưu trữ đề thi từ link Review (có đáp án)")
    print("4. Tự động làm bài từ file đề thi đã lưu")
    print("0. Thoát chương trình")
    print("="*50)

def main():
    """Hàm chính điều khiển luồng hoạt động của chương trình."""
    client = EhouClient()
    if not client.login():
        sys.exit("[-] Đăng nhập thất bại. Chương trình kết thúc.")

    while True:
        show_menu()
        choice = input("[?] Vui lòng chọn chức năng: ")

        if choice == '1':
            view_grades(client)
        elif choice == '2':
            scrape_questions_to_markdown(client)
        elif choice == '3':
            scrape_quiz(client)
        elif choice == '4':
            autofill_quiz(client)
        elif choice == '0':
            print("[*] Cảm ơn bạn đã sử dụng. Tạm biệt!")
            break
        else:
            print("[-] Lựa chọn không hợp lệ. Vui lòng chọn lại.")
        
        input("\n(Nhấn Enter để quay lại menu chính...)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Chương trình bị dừng bởi người dùng.")
    except Exception as e:
        print(f"\n[-] Đã có lỗi không mong muốn xảy ra: {e}")
    finally:
        sys.exit(0)