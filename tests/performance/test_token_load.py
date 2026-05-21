# tests/performance/test_token_load.py
# 토큰 사용량 페이지 반복 조회 부하 테스트 — FHC-099

import time
import logging
import pytest
from pages.token.token_page import TokenPage

logger = logging.getLogger(__name__)

REPEAT = 5


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def token_load(login_module):
    driver, wait = login_module
    page = TokenPage(driver, wait)
    page.click_lnb_token()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

def test_FHC_099_token_page_load(token_load):
    """
    [FHC-099] 토큰 사용량 페이지 반복 조회 부하 테스트

    전제: 헬피챗 접속, 로그인 완료 (관리자 계정)
    단계:
      1. 헬피챗 사이트 접속
      2. 로그인
      3. 토큰 사용량 페이지 진입
      4. 페이지 새로고침 5회 반복
      5. 각 조회 시 데이터 정상 표시 확인
    기대: 5회 반복 조회 중 데이터 누락 또는 오류 없음, 사용량 수치 정상 표시
    관련 TC: FHC-018, FHC-019, FHC-020, FHC-021
    """
    logger.info("[FHC-099] 토큰 사용량 반복 조회 부하 테스트 시작")
    fail_count = 0

    for i in range(1, REPEAT + 1):
        start = time.time()
        token_load.driver.refresh()
        result = token_load.is_token_table_displayed()
        elapsed = round(time.time() - start, 2)

        if result:
            logger.info(f"[{i}/{REPEAT}] 토큰 테이블 정상 표시 ({elapsed}s)")
        else:
            fail_count += 1
            logger.error(f"[{i}/{REPEAT}] 토큰 테이블 미표시 ({elapsed}s)")

    assert fail_count == 0, f"5회 중 {fail_count}회 데이터 미표시"
    logger.info("[FHC-099] 토큰 사용량 반복 조회 부하 테스트 완료")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
