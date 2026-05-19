import logging
import pytest

from pages.mypage_profile_page import MyPage

logger = logging.getLogger(__name__)

# =========================
# fixture
# =========================

# 로그인 후 MyPage 객체 생성
@pytest.fixture
def mypage(login):

    logger.info("🧪 MyPage fixture 시작")

    driver, wait = login

    page = MyPage(driver)

    logger.info("✅ MyPage 객체 생성 완료")

    return page


# =========================
# test_mypage_01
# =========================

def test_check_mypage_dropdown_menu(mypage):
    """
    [test_mypage_01]
    마이페이지 드롭다운 메뉴 UI 확인
    """

    logger.info("🧪 [test_mypage_01] 드롭다운 메뉴 UI 확인 시작")

    # 프로필 메뉴 열기
    mypage.click_profile_button()

    logger.info("⏳ 드롭다운 메뉴 노출 확인 중")

    # 메뉴 UI 확인
    assert mypage.get_account_management_menu().is_displayed()
    logger.info("✅ 계정 관리 메뉴 노출 확인")

    assert mypage.get_payment_history_menu().is_displayed()
    logger.info("✅ 결제 내역 메뉴 노출 확인")

    assert mypage.get_language_setting_menu().is_displayed()
    logger.info("✅ 언어 설정 메뉴 노출 확인")

    assert mypage.get_customer_center_menu().is_displayed()
    logger.info("✅ 고객 센터 메뉴 노출 확인")

    assert mypage.get_logout_menu().is_displayed()
    logger.info("✅ 로그아웃 메뉴 노출 확인")


# =========================
# test_mypage_02
# =========================

def test_move_account_management_page(mypage):
    """
    [test_mypage_02]
    계정 관리 페이지 UI 확인
    """

    logger.info("🧪 [test_mypage_02] 계정 관리 페이지 이동 테스트 시작")

    # 계정 관리 페이지 이동
    mypage.move_to_account_management()

    logger.info("⏳ 계정 관리 페이지 요소 확인 중")

    # 기본 정보 영역 확인
    assert mypage.get_name_label().is_displayed()
    logger.info("✅ 이름 항목 노출 확인")

    assert mypage.get_email_label().is_displayed()
    logger.info("✅ 이메일 항목 노출 확인")


# =========================
# test_mypage_03
# =========================

def test_change_profile_image(mypage):
    """
    [test_mypage_03]
    프로필 이미지 변경 확인
    """

    logger.info("🧪 [test_mypage_03] 프로필 이미지 변경 테스트 시작")

    # 계정 관리 페이지 이동
    mypage.move_to_account_management()

    # 이미지 업로드
    mypage.upload_profile_image(
        "images/test2.jpg"
    )

    logger.info("⏳ 저장 완료 메시지 확인 중")

    # 저장 완료 메시지 확인
    success_message = (
        mypage.get_save_success_message()
    )

    assert success_message.is_displayed()

    assert (
        "저장되었습니다" in success_message.text
        or
        "Saved successfully" in success_message.text
    )

    logger.info("✅ 프로필 이미지 변경 성공")


# =========================
# test_mypage_04
# =========================

def test_remove_profile_image(mypage):
    """
    [test_mypage_04]
    프로필 이미지 제거
    """

    logger.info("🧪 [test_mypage_04] 프로필 이미지 제거 테스트 시작")

    # 계정 관리 페이지 이동
    mypage.move_to_account_management()

    # 펜 버튼 클릭
    mypage.click_profile_image_edit_button()

    # 프로필 이미지 제거 클릭
    mypage.click_remove_profile_image_menu()

    logger.info("⏳ 저장 완료 메시지 확인 중")

    # 저장 완료 메시지 확인
    success_message = (
        mypage.get_save_success_message()
    )

    assert success_message.is_displayed()

    assert (
        "저장되었습니다." in success_message.text
        or
        "Saved successfully." in success_message.text
    )

    logger.info("✅ 프로필 이미지 제거 성공")