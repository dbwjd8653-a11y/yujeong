# config/settings.py
# 프로젝트 전체 공통 상수 — URL, 계정, 대기시간, 경로

import os
from dotenv import load_dotenv

load_dotenv()

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
SIGNUP_FORM_URL = (
    "https://accounts.elice.io/accounts/signup/form"
    "?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat"
    "&lang=ko-KR&org=qaproject"
)

# ── 대기 시간 (초) ──────────────────────────────────────────────────
# CI는 headless라 렌더가 느려 기존 한도(10/20초)를 종종 초과한다.
# (요소 출현 즉시 리턴하므로 정상 케이스 속도엔 영향 없고 상한만 키우는 보정)
_WAIT_SCALE  = 1.5 if os.environ.get("CI") else 1
SHORT_WAIT   = 2
DEFAULT_WAIT = int(10 * _WAIT_SCALE)   # CI: 15
LONG_WAIT    = int(20 * _WAIT_SCALE)   # CI: 30

# ── 테스트 계정 ────────────────────────────────────────────────────
TEST_USER = {
    "id": os.getenv("TEST_USER_ID"),
    "pw": os.getenv("TEST_USER_PW"),
}

# ── 마이페이지 전용 계정 (파괴적 테스트용 — 계정 탈퇴/재가입, 비밀번호 변경) ──
# 메인 TEST_USER를 망가뜨리지 않도록 반드시 분리된 더미 계정을 사용한다.
MYPAGE_USER = {
    "id":   os.getenv("MYPAGE_USER_ID"),
    "pw":   os.getenv("MYPAGE_USER_PW"),
    "name": os.getenv("MYPAGE_USER_NAME"),
}
# 비밀번호 변경 테스트에서 사용 후 원복하는 임시 비밀번호
MYPAGE_NEW_PASSWORD = os.getenv("MYPAGE_NEW_PASSWORD")

# ── 비관리자 계정 (조직 설정 권한 테스트용) ──
NON_ADMIN_USER = {
    "id": os.getenv("NON_ADMIN_USER_ID"),
    "pw": os.getenv("NON_ADMIN_USER_PW"),
}

# ── 다운로드 경로 ───────────────────────────────────────────────────
DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads")