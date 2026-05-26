# tests/signup/test_signup.py
# 회원가입 E2E 테스트 — FHC-001 ~ FHC-005

import logging
import pytest
import allure
from pages.signup.signup_page import SignupPage
from utils.random_generator import generate_test_email

logger = logging.getLogger(__name__)

LONG_TEXT_300 = "김수한무거북이와두루미삼천갑자동방삭치치카포사리사리센타워리워리세브리깡" * 10
DEFAULT_PASSWORD = "test1234!!"
DEFAULT_NAME = "김엘리스"

pytestmark = [
    allure.epic("Signup"),
    allure.feature("회원가입"),
]


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

# ── Happy Path ───────────────────────────────────────────────────
@allure.story("회원가입 성공")
class TestSignupHappyPath:
    
  @allure.title("[FHC-001] 회원가입 페이지 이동 확인")
  @allure.severity(allure.severity_level.NORMAL)
  def test_FHC_001_signup_page_elements(self, signup):
      """
      [FHC-001] 회원가입 페이지 이동 확인

      전제: 로그인 되지 않은 상태
      단계: 1. '회원가입' 링크 클릭
      기대: 회원가입 입력창 표시 (이메일, 비밀번호, 이름, 약관 동의, '회원가입' 버튼)
      """
      logger.info("[FHC-001] 회원가입 페이지 요소 확인 시작")
      
      assert "signup" in signup.driver.current_url

      assert signup.get_email_input().is_displayed()
      assert signup.get_password_input().is_displayed()
      assert signup.get_name_input().is_displayed()
      assert signup.get_agree_checkbox().is_displayed()
      
      logger.info("[FHC-001] 회원가입 페이지 요소 확인 완료")


  @pytest.mark.parametrize(
      ("agreement_type", "tc_id"),
      [
          ("all", "FHC-002"),
          ("required", "FHC-003"),
      ]
  )
  @allure.title("{tc_id} 회원가입 성공")
  @allure.severity(allure.severity_level.CRITICAL)
  def test_signup_success(self, signup, agreement_type, tc_id):
      """
      [FHC-002] 전체 동의 회원가입 성공
      전제: 회원 가입 페이지 접근
      단계:
          1. 로그인 필수 요소 입력
          2. 회원 약관 '전체 동의' 클릭
      기대: 회원 가입 성공

      [FHC-003] 필수 약관 동의 회원가입 성공
      전제: 회원 가입 페이지 접근
      단계: 
          1. 로그인 필수 요소 입력
          2. 회원 약관 중 필수 요소 클릭
            - 14세 이상, [Required], [필수] 항목
      기대: 회원 가입 성공
      """

      logger.info(f"[{tc_id}] 회원가입 시작")

      signup.fill_signup_form(
          email=generate_test_email(),
          password=DEFAULT_PASSWORD,
          name=DEFAULT_NAME
      )

      signup.agree_terms(agreement_type)

      signup.click_create_account_button()

      assert signup.is_signup_success(), (
          "회원가입 성공 후 랜딩 페이지 이동 실패"
      )

      logger.info(f"[{tc_id}] 회원가입 완료")


# ── Negative Path ────────────────────────────────────────────────
@allure.story("회원가입 실패")
class TestSignupNegative:

    @allure.title("[FHC-004] 이메일 유효성 검사")
    @allure.severity(allure.severity_level.NORMAL)
    def test_FHC_004_signup_invalid_email(self, signup):
        """
        [FHC-004] 이메일 유효성 검사
        단계: 
            회원가입 페이지 > 유효하지 않은 이메일 입력
        기대:
            이메일 오류 메시지가 출력된다.
        """

        logger.info("[FHC-004] 이메일 유효성 검사 시작")

        signup.enter_email("123")

        assert signup.get_email_error_message().is_displayed(), (
            "이메일 유효성 오류 메시지 미출력"
        )

        logger.info("[FHC-004] 이메일 유효성 검사 완료")

    @allure.title("[FHC-005] 이름 유효성 검사")
    @allure.severity(allure.severity_level.NORMAL)
    def test_FHC_005_signup_invalid_name(self, signup):
        """
        [FHC-005] 이름 유효성 검사
        단계:
            회원가입 페이지 > 유효하지 않은 이름 입력(300자 이상)
        기대:
            이름 오류 메시지가 출력된다.
        """

        logger.info("[FHC-005] 이름 유효성 검사 시작")

        signup.fill_signup_form(
            email=generate_test_email(),
            password=DEFAULT_PASSWORD,
            name=LONG_TEXT_300
        )

        signup.agree_terms("all")

        signup.click_create_account_button()

        assert signup.get_name_error_message().is_displayed(), (
            "이름 유효성 오류 메시지 미출력"
        )

        logger.info("[FHC-005] 이름 유효성 검사 완료")