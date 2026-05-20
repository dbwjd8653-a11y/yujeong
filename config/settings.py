# common/config.py
# 프로젝트 전체 공통 상수 — URL, 계정, 대기시간, 경로

import os

# ── URL ────────────────────────────────────────────────────────────
LOGIN_URL = (
    "https://accounts.elice.io/accounts/signin/me"
    "?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat"
    "&lang=ko-KR&org=qaproject"
)
BASE_URL     = "https://qaproject.elice.io/ai-helpy-chat"
BASE_UI_URL  = "https://qaproject.elice.io"
BASE_API_URL = "https://dev-v2-community-api.dev.elicer.io"

SIGNUP_URL = (
    "https://accounts.elice.io/accounts/signup/method"
    "?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat"
    "&lang=ko-KR&org=qaproject"
)

# ── 대기 시간 (초) ──────────────────────────────────────────────────
SHORT_WAIT   = 5
DEFAULT_WAIT = 10
LONG_WAIT    = 20

# ── 테스트 계정 ────────────────────────────────────────────────────
TEST_USER = {
    "id": os.getenv("TEST_USER_ID", "qa5team3-01@elicer.com"),
    "pw": os.getenv("TEST_USER_PW", "qwer1234!"),
}

MYPAGE_USER = {
    "id": os.getenv("MYPAGE_USER_ID", "qa5team3-02@elicer.com"),
    "pw": os.getenv("MYPAGE_USER_PW", "Mdk@02169630"),
}

# ── 다운로드 경로 ───────────────────────────────────────────────────
DOWNLOAD_DIR = r"C:\Users\Admin\Downloads"
