# tests/mypage/test_mypage_profile.py
# 마이페이지 프로필 E2E 테스트 — FHC-076 ~ FHC-079

import logging

import allure
import pytest

from pages.mypage.mypage_profile_page import MyPageProfilePage

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("MyPage"),
    allure.feature("프로필"),
]

IMAGE_PATH = "images/test1.jpg"


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture
def mypage(login):
    """
    마이페이지 프로필 fixture

    전제: login fixture로 로그인 완료 상태
    단계:
      1. login에서 (driver, wait) 수신 → MyPage 반환
    """
    driver, wait = login
    return MyPageProfilePage(driver)


# ── 테스트 케이스 ──────────────────────────────────────────────────
@allure.story("마이페이지 - 프로필 기능")
class TestMyPageProfileHappyPath:

  @allure.story("프로필 드롭다운 메뉴 확인")
  @allure.title("[FHC-076] 프로필 드롭다운 메뉴 항목 확인")
  @allure.severity(allure.severity_level.NORMAL)
  def test_FHC_076_profile_dropdown_menu(self, mypage):
      """
      [FHC-076] 프로필 드롭다운 메뉴 항목 확인

      전제: 로그인 완료 상태
      단계:
        1. 우측 상단 프로필 버튼 클릭
      기대: 드롭다운에 '계정 관리', '결제 내역', '언어 설정', '고객 센터', '로그아웃' 메뉴 표시
      """
      logger.info("[FHC-076] 프로필 드롭다운 메뉴 항목 확인 시작")
      mypage.click_profile_button()
      assert mypage.get_account_management_menu().is_displayed(), "계정 관리 메뉴 미표시"
      assert mypage.get_payment_history_menu().is_displayed(), "결제 내역 메뉴 미표시"
      assert mypage.get_language_setting_menu().is_displayed(), "언어 설정 메뉴 미표시"
      assert mypage.get_customer_center_menu().is_displayed(), "고객 센터 메뉴 미표시"
      assert mypage.get_logout_menu().is_displayed(), "로그아웃 메뉴 미표시"
      logger.info("[FHC-076] 프로필 드롭다운 메뉴 항목 확인 완료")


  @allure.title("[FHC-077] 계정 관리 페이지 이동 확인")
  @allure.severity(allure.severity_level.NORMAL)
  def test_FHC_077_navigate_to_account_management(self, mypage):
      """
      [FHC-077] 계정 관리 페이지 이동 확인

      단계:
        1. 우측 상단 프로필 버튼 클릭
        2. '계정 관리' 메뉴 클릭
      기대: 계정 관리 페이지에 '이름', '이메일' 항목 표시
      """
      logger.info("[FHC-077] 계정 관리 페이지 이동 확인 시작")
      mypage.move_to_account_management()
      assert mypage.get_name_label().is_displayed(), "이름 항목 미표시"
      assert mypage.get_email_label().is_displayed(), "이메일 항목 미표시"
      logger.info("[FHC-077] 계정 관리 페이지 이동 확인 완료")


  @allure.title("[FHC-078] 프로필 이미지 변경 확인")
  @allure.severity(allure.severity_level.NORMAL)
  def test_FHC_078_change_profile_image(self, mypage):
      """
      [FHC-078] 프로필 이미지 변경 확인

      단계:
        1. 계정 관리 페이지로 이동
        2. 프로필 이미지 파일(images/test2.jpg) 업로드
      기대: '저장되었습니다.' 성공 메시지 표시
      """
      logger.info("[FHC-078] 프로필 이미지 변경 확인 시작")
      mypage.move_to_account_management()
      mypage.upload_profile_image(IMAGE_PATH)

      assert mypage.is_save_success_message_displayed(), (
        f"저장 성공 메시지 불일치: "
        f"{mypage.get_save_success_message_text()}"
        )
      
      logger.info("[FHC-078] 프로필 이미지 변경 확인 완료")


  @allure.title("[FHC-079] 프로필 이미지 제거 확인")
  @allure.severity(allure.severity_level.NORMAL)
  def test_FHC_079_remove_profile_image(self, mypage):
      """
      [FHC-079] 프로필 이미지 제거 확인

      단계:
        1. 계정 관리 페이지로 이동
        2. 프로필 이미지 수정 버튼 클릭
        3. '프로필 이미지 제거' 메뉴 클릭
      기대: '저장되었습니다.' 성공 메시지 표시
      """
      logger.info("[FHC-079] 프로필 이미지 제거 확인 시작")
      mypage.move_to_account_management()
      mypage.remove_profile_image()

      assert mypage.is_save_success_message_displayed(), (
          f"저장 성공 메시지 불일치: "
          f"{mypage.get_save_success_message_text()}"
      )

      logger.info("[FHC-079] 프로필 이미지 제거 확인 완료")