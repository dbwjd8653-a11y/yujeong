# tests/performance/test_mypage_load.py
# 마이페이지 탭 반복 이동 부하 테스트 — FHC-098

import time
import logging
import pytest
import allure
from pages.mypage.mypage_page import MyPage

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Performance"),
    allure.feature("마이페이지 부하 테스트"),
]

REPEAT = 3


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def mypage_load(login_module):
    driver, wait = login_module
    page = MyPage(driver)
    page.navigate_to_account()
    return driver, wait


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("마이페이지 탭 반복 이동 부하 테스트")
@allure.title("[FHC-098] 마이페이지 탭 반복 이동 부하 테스트")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_098_mypage_tab_load(mypage_load):
    """
    [FHC-098] 마이페이지 탭 반복 이동 부하 테스트

    전제: 헬피챗 접속, 로그인 완료 (일반 계정)
    단계:
      1. 헬피챗 사이트 접속
      2. 로그인
      3. 마이페이지 진입
      4. 계정 → 내 기관 → 언어 → 지원 탭 순차 클릭 (3번 반복)
      5. 각 탭 전환 시 페이지 정상 표시 확인
    기대: 탭 전환 시 오류 없이 콘텐츠 정상 표시, 로딩 실패 없음
    관련 TC: FHC-076, FHC-077, FHC-083, FHC-090, FHC-093
    """
    logger.info("[FHC-098] 마이페이지 탭 반복 이동 부하 테스트 시작")
    driver, wait = mypage_load
    page = MyPage(driver)
    fail_count = 0

    for i in range(1, REPEAT + 1):
        logger.info(f"[{i}/{REPEAT}] 탭 순환 시작")

        try:
            start = time.time()
            page.navigate_to_account()
            page.navigate_to_org()
            page.navigate_to_language()
            page.navigate_to_support()
            elapsed = round(time.time() - start, 2)
            logger.info(f"[{i}/{REPEAT}] 탭 순환 완료 ({elapsed}s)")
        except Exception as e:
            fail_count += 1
            logger.error(f"[{i}/{REPEAT}] 탭 전환 오류: {e}")

    assert fail_count == 0, f"3회 중 {fail_count}회 탭 전환 실패"
    logger.info("[FHC-098] 마이페이지 탭 반복 이동 부하 테스트 완료")
