# tests/test_mypage_02.py
# 마이페이지 프로필 E2E 테스트 — FHC-078 ~ FHC-079

import logging
import pytest
from pages.mypage.mypage_profile_page import MyPage

logger = logging.getLogger(__name__)

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
    return MyPage(driver)


# ── 테스트 케이스 ──────────────────────────────────────────────────

def test_FHC_078_change_profile_image(mypage):
    """
    [FHC-078] 프로필 이미지 변경 확인

    전제: 로그인 완료 상태
    단계:
      1. 계정 관리 페이지로 이동
      2. 프로필 이미지 파일(images/test2.jpg) 업로드
    기대: '저장되었습니다.' 성공 메시지 표시
    """
    logger.info("[FHC-078] 프로필 이미지 변경 확인 시작")
    mypage.move_to_account_management()
    mypage.upload_profile_image(IMAGE_PATH)
    msg = mypage.get_save_success_message()
    assert msg.is_displayed(), "저장 성공 메시지 미표시"
    assert "저장되었습니다" in msg.text or "Saved successfully" in msg.text, \
        f"저장 성공 메시지 불일치: {msg.text}"
    logger.info("[FHC-078] 프로필 이미지 변경 확인 완료")


def test_FHC_079_remove_profile_image(mypage):
    """
    [FHC-079] 프로필 이미지 제거 확인

    전제: 로그인 완료 상태
    단계:
      1. 계정 관리 페이지로 이동
      2. 프로필 이미지 수정 버튼 클릭
      3. '프로필 이미지 제거' 메뉴 클릭
    기대: '저장되었습니다.' 성공 메시지 표시
    """
    logger.info("[FHC-079] 프로필 이미지 제거 확인 시작")
    mypage.move_to_account_management()
    mypage.click_profile_image_edit_button()
    mypage.click_remove_profile_image_menu()
    msg = mypage.get_save_success_message()
    assert msg.is_displayed(), "저장 성공 메시지 미표시"
    assert "저장되었습니다" in msg.text or "Saved successfully" in msg.text, \
        f"저장 성공 메시지 불일치: {msg.text}"
    logger.info("[FHC-079] 프로필 이미지 제거 확인 완료")
