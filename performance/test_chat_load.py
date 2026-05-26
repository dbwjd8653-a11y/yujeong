# tests/performance/test_chat_load.py
# 채팅 메시지 연속 전송 부하 테스트 — FHC-095

import time
import logging
import pytest
import allure
from pages.chat.chat_page import ChatPage

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Performance"),
    allure.feature("채팅 부하 테스트"),
]

REPEAT = 10
INTERVAL = 1
TEST_MESSAGE = "안녕하세요"


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def chat_load(login_module):
    driver, wait = login_module
    page = ChatPage(driver, wait)
    page.open()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("채팅 메시지 연속 전송 부하 테스트")
@allure.title("[FHC-095] 채팅 메시지 연속 전송 부하 테스트")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_095_chat_load(chat_load):
    """
    [FHC-095] 채팅 메시지 연속 전송 부하 테스트

    전제: 헬피챗 접속, 로그인 완료 (관리자 계정)
    단계:
      1. 헬피챗 사이트 접속
      2. 로그인
      3. 채팅창 진입
      4. 메시지 연속 10회 전송
      5. 각 응답 수신 여부 및 시간 확인
    기대: 10회 전송 중 오류 없이 응답 수신, 각 응답 시간 기록됨
    관련 TC: FHC-022, FHC-023, FHC-024, FHC-025, FHC-026, FHC-027
    """
    logger.info("[FHC-095] 채팅 연속 전송 부하 테스트 시작")
    fail_count = 0

    for i in range(1, REPEAT + 1):
        chat_load.click_new_chat_from_lnb()
        time.sleep(0.5)  # 새 대화 DOM 안정화 대기
        start = time.time()
        chat_load.send_message(TEST_MESSAGE)
        success = chat_load.wait_for_ai_response()
        time.sleep(1)  # 응답 후 DOM 갱신 완료 대기
        elapsed = round(time.time() - start, 2)

        if success:
            logger.info(f"[{i}/{REPEAT}] 응답 수신 완료 ({elapsed}s)")
        else:
            fail_count += 1
            logger.error(f"[{i}/{REPEAT}] 응답 수신 실패 ({elapsed}s)")
        time.sleep(INTERVAL)

    assert fail_count == 0, f"10회 중 {fail_count}회 응답 수신 실패"
    logger.info("[FHC-095] 채팅 연속 전송 부하 테스트 완료")
