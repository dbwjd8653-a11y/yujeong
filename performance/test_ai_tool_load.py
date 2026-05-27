# tests/performance/test_ai_tool_load.py
# AI 도구(행동특성 및 종합의견) 연속 생성 요청 부하 테스트 — FHC-097

import time
import logging
import pytest
import allure

from config.settings import DOWNLOAD_DIR
from pages.tools.tools_behavior_page import BehaviorPage

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Performance"),
    allure.feature("AI 도구 부하 테스트"),
]

REPEAT       = 3
INTERVAL     = 3
SCHOOL_LEVEL = "중학교"
NAME_TEXT    = "포커스 1차 프로젝트"
REQUEST_TEXT = "엘리스 부트 캠프"


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def ai_tool_load(tools_driver_module):
    """
    BehaviorPage fixture (모듈 공유)

    전제: tools_driver_module fixture로 로그인 완료 상태
    단계:
      1. tools_driver_module에서 driver 수신 → BehaviorPage 반환
    """
    page = BehaviorPage(tools_driver_module)
    page.login()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("AI 도구 연속 생성 요청 부하 테스트")
@allure.title("[FHC-097] AI 도구(행동특성) 연속 생성 요청 부하 테스트")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_097_ai_tool_load(ai_tool_load):
    """
    [FHC-097] AI 도구(행동특성) 연속 생성 요청 부하 테스트

    전제: 헬피챗 접속, 로그인 완료 (관리자 계정)
    단계:
      1. 헬피챗 사이트 접속
      2. 로그인
      3. AI 도구(행동특성 및 종합의견) 진입
      4. 생성 요청 3회 연속 실행
      5. 각 생성 완료 여부 및 시간 확인
    기대: 3회 연속 생성 요청 모두 완료, 결과 파일 정상 다운로드
    관련 TC: FHC-037, FHC-042, FHC-043, FHC-044
    """
    logger.info("[FHC-097] AI 도구 연속 생성 부하 테스트 시작")
    page = ai_tool_load
    fail_count = 0

    with allure.step("[FHC-037] 도구 목록 표시 확인"):
        page.navigate_to_tools()

    with allure.step("[FHC-038] '행동특성 및 종합의견' 도구 선택"):
        page.click_tool_menu(BehaviorPage.TOOL_NAME)

    with allure.step("[FHC-039] 입력 내역 초기화"):
        page.reset_inputs()

    with allure.step("[FHC-040] 수업 정보 입력 탭 이동 및 학교급 선택"):
        page.click_class_info_tab()
        page.select_school_level(SCHOOL_LEVEL)

    with allure.step("[FHC-041] '다음으로' 버튼 클릭 → 학생 정보 화면 이동"):
        page.click_next()
        page.handle_modify_modal()

    with allure.step("[FHC-042] 학생 이름 입력"):
        page.ensure_student_row_exists()
        page.enter_student_name(NAME_TEXT)

    with allure.step("[FHC-043] 인성·태도 키워드 선택 및 저장"):
        page.open_keyword_modal()
        page.select_character_keyword()
        page.save_keyword_modal()
        if REQUEST_TEXT:
            page.enter_request_text(REQUEST_TEXT)

    for i in range(1, REPEAT + 1):
        if i > 1:
            time.sleep(INTERVAL)
        with allure.step(f"[FHC-044] AI 생성 트리거 ({i}/{REPEAT})"):
            page.trigger_generation()
            page.search_student(NAME_TEXT)
        logger.info(f"[{i}/{REPEAT}] 생성 결과 받기 시작")
        start = time.time()
        result = page.download_result(DOWNLOAD_DIR)
        elapsed = round(time.time() - start, 2)
        if result:
            logger.info(f"[{i}/{REPEAT}] 다운로드 완료 ({elapsed}s)")
        else:
            fail_count += 1
            logger.error(f"[{i}/{REPEAT}] 다운로드 실패 ({elapsed}s)")

    assert fail_count == 0, f"3회 중 {fail_count}회 생성 실패"
    logger.info("[FHC-097] AI 도구 연속 생성 부하 테스트 완료")
