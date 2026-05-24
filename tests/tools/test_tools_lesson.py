# tests/tools/test_tools_lesson.py
# 수업지도안 도구 E2E 테스트 — FHC-045 ~ FHC-049

import os
import pytest
import logging
import allure
from pages.tools.tools_lesson_page import LessonPlanPage

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Tools"),
    allure.feature("수업지도안"),
    allure.story("수업지도안 생성 해피 케이스"),
]

COMMENT        = "없음"
REFERENCE_FILE = os.path.join(os.path.dirname(__file__), "../fixtures/file_choose_test.pdf")


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def page(login_module):
    driver, wait = login_module
    return LessonPlanPage(driver, wait)


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.title("[FHC-045~049] 수업지도안 생성 해피 케이스 (다시 생성 포함)")
@allure.severity(allure.severity_level.NORMAL)
def test_lesson_plan_happy_case(page):
    """
    [FHC-045~049] 수업지도안 생성 해피 케이스

    전제: 로그인 완료 상태
    단계:
      1. [FHC-045] LNB > '도구' 탭 > '수업지도안' 메뉴 클릭
      2. [FHC-046] 교급, 학년, 교과, 수업 차시, 생성 방식 랜덤 선택
      3. [FHC-047] 참고 자료 업로드 및 기타 요청 사항 입력
      4. [FHC-048] '다시 생성' 버튼 클릭
      5. [FHC-049] 재생성 완료 대기 (최대 60초)
    기대: 최초 생성 및 재생성 모두 1분 이내 완료
    """
    with allure.step("[FHC-045] 수업지도안 메뉴 이동"):
        logger.info("[FHC-045] 수업지도안 메뉴 이동 시작")
        page.navigate_to_tools()
        page.click_tool_menu(LessonPlanPage.TOOL_NAME)
        assert page.is_on_tool_page(), "수업지도안 페이지 미이동"

    with allure.step("[FHC-046] 필수 항목 랜덤 선택"):
        logger.info("[FHC-046] 필수 항목 입력 시작")
        page.regen_with_random_values()

    with allure.step("[FHC-047] 선택 항목 입력"):
        logger.info("[FHC-047] 선택 항목 입력 시작")
        page.scroll_to_upload_area()
        assert page.is_upload_area_visible(), "업로드 영역 미표시"
        page.upload_reference(os.path.abspath(REFERENCE_FILE))
        page.enter_comment(COMMENT)

    with allure.step("[FHC-048] '다시 생성' 버튼 클릭"):
        logger.info("[FHC-048] 다시 생성 시작")
        page.click_generate()

    with allure.step("[FHC-049] 재생성 완료 확인"):
        logger.info("[FHC-049] 재생성 완료 확인 시작")
        assert page.wait_for_generation(timeout=60), "수업지도안 재생성 1분 이내 실패"


    logger.info("[FHC-045~049] 수업지도안 생성 해피 케이스 완료")
