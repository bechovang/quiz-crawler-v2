# core/ehou_client.py

import requests
import getpass
from bs4 import BeautifulSoup, Tag
from urllib.parse import urljoin, quote
from config import settings
import time

class EhouClient:
    """
    Quản lý session và quy trình đăng nhập CAS (Single Sign-On) của EHOU.
    """
    def __init__(self):
        self.username = ""
        self.password = ""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': settings.DEFAULT_USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
        })
        self.logged_in = False
        self.cas_base_url = 'https://cas.ehou.edu.vn/cas'

    def login(self) -> bool:
        """Thực hiện quy trình đăng nhập CAS."""
        if self.logged_in:
            return True

        print("[*] Vui lòng nhập thông tin đăng nhập EHOU:")
        self.username = input("    Tên đăng nhập: ")
        self.password = getpass.getpass("    Mật khẩu (sẽ không hiển thị): ")

        if not self.username or not self.password:
            print("[-] Tên đăng nhập và mật khẩu không được để trống.")
            return False

        print(f"[*] Bắt đầu quy trình đăng nhập cho tài khoản: {self.username}...")

        try:
            # B1: Lấy login token từ trang CAS
            service_url = settings.EHOU_LOGIN_URL
            cas_login_url = f'{self.cas_base_url}/login?service={quote(service_url)}'
            cas_page_res = self.session.get(cas_login_url, allow_redirects=True)
            cas_page_res.raise_for_status()

            soup = BeautifulSoup(cas_page_res.content, 'lxml')
            lt_input = soup.find('input', {'name': 'lt'})
            execution_input = soup.find('input', {'name': 'execution'})

            if not (isinstance(lt_input, Tag) and isinstance(execution_input, Tag)):
                print("[-] Lỗi: Không tìm thấy token 'lt' hoặc 'execution' trong form đăng nhập.")
                return False

            # B2: Gửi thông tin đăng nhập để lấy "vé"
            cas_post_payload = {
                'username': self.username, 'password': self.password,
                'lt': lt_input['value'], 'execution': execution_input['value'],
                '_eventId': 'submit', 'submit': 'ĐĂNG NHẬP'
            }
            cas_response = self.session.post(cas_login_url, data=cas_post_payload, allow_redirects=False)

            if cas_response.status_code != 302:
                print("[-] Đăng nhập CAS thất bại. Vui lòng kiểm tra lại tài khoản/mật khẩu.")
                return False
            
            redirect_location_with_ticket = cas_response.headers.get('Location')
            if not redirect_location_with_ticket or 'ticket=' not in redirect_location_with_ticket:
                print("[-] Lỗi: Máy chủ CAS không cung cấp 'ticket'.")
                return False

            # B3: Dùng "vé" để truy cập Moodle và tạo session
            moodle_response = self.session.get(redirect_location_with_ticket, allow_redirects=True)
            moodle_response.raise_for_status()

            if 'MoodleSession' in self.session.cookies and 'logout.php' in moodle_response.text:
                print("[+] Đăng nhập thành công!")
                self.logged_in = True
                time.sleep(settings.DELAY_AFTER_LOGIN)
                return True
            else:
                print("[-] Đăng nhập thất bại ở bước cuối cùng (xác thực ticket).")
                return False

        except requests.exceptions.RequestException as e:
            print(f"[-] Lỗi kết nối trong quá trình đăng nhập: {e}")
            return False

    def get_page_content(self, url: str) -> str | None:
        if not self.logged_in:
            print("[-] Chưa đăng nhập.")
            return None
        try:
            response = self.session.get(url)
            response.raise_for_status()
            time.sleep(settings.DELAY_AFTER_PAGE_LOAD)
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"[-] Lỗi khi tải trang {url}: {e}")
            return None

    def post_data(self, url: str, payload: dict) -> requests.Response | None:
        if not self.logged_in:
            print("[-] Chưa đăng nhập.")
            return None
        try:
            # Gửi dưới dạng multipart/form-data để mô phỏng trình duyệt chính xác
            files_payload = {key: (None, str(value)) for key, value in payload.items()}
            response = self.session.post(url, files=files_payload)
            response.raise_for_status()
            time.sleep(settings.DELAY_AFTER_PAGE_SUBMIT)
            return response
        except requests.exceptions.RequestException as e:
            print(f"[-] Lỗi khi gửi POST đến {url}: {e}")
            return None