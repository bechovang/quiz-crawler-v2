# config/settings.py

# --- EHOU URLs ---
EHOU_BASE_URL = 'https://learning.ehou.edu.vn'
EHOU_LOGIN_URL = f'{EHOU_BASE_URL}/login/index.php'
EHOU_PROCESS_ATTEMPT_URL = f'{EHOU_BASE_URL}/mod/quiz/processattempt.php'
EHOU_MY_COURSES_URL = f'{EHOU_BASE_URL}/my/'

# --- Automation Settings ---
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'

# Độ trễ (giây) để tránh bị phát hiện hoặc bị block
DELAY_AFTER_LOGIN = 2.0         # Chờ sau khi đăng nhập thành công
DELAY_AFTER_PAGE_LOAD = 1.5     # Chờ sau khi tải một trang mới
DELAY_AFTER_PAGE_SUBMIT = 2.5   # Chờ sau khi nộp một trang câu hỏi