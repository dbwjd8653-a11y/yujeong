# tests/test_signup_01.py
# 회원가입 E2E 테스트 — FHC-001 ~ FHC-00

import logging
import pytest
from pages.signup.signup_page import SignupPage

logger = logging.getLogger(__name__)


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture
def signup(driver):
    """
    회원가입 페이지 진입 fixture

    전제: 브라우저 실행 상태
    단계:
      1. 회원가입 페이지 URL로 이동
      2. '이메일로 가입하기' 버튼 클릭
    """
    page = SignupPage(driver)
    page.open()
    page.click_create_account_with_email()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

def test_FHC_001_signup_page_elements(signup):
    """
    [FHC-001] 회원가입 페이지 이동 확인

    전제: 로그인 되지 않은 상태
    단계:
      1. '회원가입' 링크 클릭
    기대: 회원가입 입력창 표시 (이메일, 비밀번호, 이름, 약관 동의, '회원가입' 버튼)
    """
    logger.info("[FHC-001] 회원가입 페이지 요소 확인 시작")
    assert "signup" in signup.driver.current_url
    assert signup.get_email_input().is_displayed()
    assert signup.get_password_input().is_displayed()
    assert signup.get_name_input().is_displayed()
    assert signup.get_agree_checkbox().is_displayed()
    logger.info("[FHC-001] 회원가입 페이지 요소 확인 완료")

# ── 테스트 케이스 ──────────────────────────────────────────────────
def test_FHC_002_signup_agree_all(signup):
    """
    [FHC-002] 전체 동의 회원가입 동작 테스트

    전제: 로그인 되지 않은 상태 / 회원가입 입력창 접근
    단계:
      1. 이메일 입력
      2. 비밀번호 입력
      3. 이름 입력
      4. 전체 동의 체크박스 클릭
      5. '회원가입' 버튼 클릭
    기대: AI Helpy Chat > Helpy Pro Agent 창 활성화 (랜딩 페이지 이동)
    """
    logger.info("[FHC-002] 전체 동의 회원가입 시작")
    signup.enter_email("testteam3js16@test.com")
    signup.enter_password("test1234!!")
    signup.enter_name("김엘리스")
    signup.click_agree_checkbox()
    signup.click_create_account_button()
    assert signup.is_signup_success(), "회원가입 후 랜딩 페이지로 이동하지 않았습니다"
    logger.info("[FHC-002] 전체 동의 회원가입 완료")

def test_FHC_003_signup_required_only(signup):
    """
    [FHC-003] 필수 약관만 동의 후 회원가입 동작 테스트

    전제: 로그인 되지 않은 상태 / 회원가입 입력창 접근
    단계:
      1. 이메일 입력
      2. 비밀번호 입력
      3. 이름 입력
      4. 만 14세 이상 체크박스 클릭
      5. [필수] 약관 체크박스 클릭
      6. '회원가입' 버튼 클릭
    기대: AI Helpy Chat > Helpy Pro Agent 창 활성화 (랜딩 페이지 이동)
    """
    logger.info("[FHC-003] 필수 약관 회원가입 시작")
    signup.enter_email("testteam3js17@test.com")
    signup.enter_password("test1234!!")
    signup.enter_name("김엘리스")
    signup.click_age_checkbox()
    signup.click_required_checkbox()
    signup.click_create_account_button()
    assert signup.is_signup_success(), "회원가입 후 랜딩 페이지로 이동하지 않았습니다"
    logger.info("[FHC-003] 필수 약관 회원가입 완료")

def test_FHC_004_signup_invalid_email(signup):
    """
    [FHC-004] 이메일 유효성 검사 (negative test)

    전제: 로그인 되지 않은 상태 / 회원가입 입력창 접근
    단계:
      1. 이메일 필드에 '123' 입력
    기대: '이메일 주소가 올바르지 않습니다.' 오류 메시지 표시
    """
    logger.info("[FHC-004] 이메일 유효성 검사 시작")
    signup.enter_email("123")
    assert signup.get_email_error_message().is_displayed()
    logger.info("[FHC-004] 이메일 유효성 검사 완료")

def test_FHC_005_signup_invalid_name(signup):
    """
    [FHC-005] 이름 유효성 검사 (negative test)

    전제: 로그인 되지 않은 상태 / 회원가입 입력창 접근
    단계:
      1. 유효한 이메일 입력
      2. 유효한 비밀번호 입력
      3. 이름 입력 필드에 300자 이상 텍스트 입력
      4. 전체 동의 체크박스 클릭
      5. '회원가입' 버튼 클릭
    기대: '예기치 못한 문제가 발생하였습니다. 잠시 후, 다시 시도해주세요.' 오류 메시지 표시
    """
    logger.info("[FHC-005] 이름 유효성 검사 시작")
    signup.enter_email("testteam3js18@test.com")
    signup.enter_password("test1234!!")
    signup.enter_name(LONG_TEXT_300)
    signup.click_agree_checkbox()
    signup.click_create_account_button()
    assert signup.get_name_error_message().is_displayed()
    logger.info("[FHC-005] 이름 유효성 검사 완료")