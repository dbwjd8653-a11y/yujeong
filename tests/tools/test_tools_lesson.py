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

    with allure.step("[FHC-046] 필수 항목 랜덤 선택"):
        logger.info("[FHC-046] 필수 항목 입력 시작")
        page.regen_with_random_values()

    with allure.step("[FHC-047] 선택 항목 입력"):
        logger.info("[FHC-047] 선택 항목 입력 시작")
        page.scroll_to_upload_area()
        page.upload_reference(os.path.abspath(REFERENCE_FILE))
        page.enter_comment(COMMENT)

    with allure.step("[FHC-048] '다시 생성' 버튼 클릭"):
        logger.info("[FHC-048] 다시 생성 시작")
        page.click_generate()

    with allure.step("[FHC-049] 재생성 완료 확인"):
        logger.info("[FHC-049] 재생성 완료 확인 시작")
        page.wait_for_regeneration(timeout=60)


    logger.info("[FHC-045~049] 수업지도안 생성 해피 케이스 완료")


# ── 실패 케이스 ──────────────────────────────────────────────────

@allure.title("[FHC-045-F] 수업지도안 페이지 미이동")
@allure.story("수업지도안 생성 새드케이스")
@allure.severity(allure.severity_level.NORMAL)
def test_fhc045_page_not_loaded(page):
    with allure.step("[FHC-045-F] 메뉴 미클릭 상태에서 수업지도안 페이지 진입 여부 확인"):
        page.navigate_to_tools()
        logger.error("[FHC-045-F] 수업지도안 메뉴 미클릭 — 페이지 미이동 확인")
        assert not page.is_on_tool_page(), "메뉴 미클릭 상태에서 수업지도안 페이지로 이동됨"


@allure.title("[FHC-046-F] 필수 항목 미선택 시 생성 버튼 비활성화")
@allure.story("수업지도안 생성 새드케이스")
@allure.severity(allure.severity_level.NORMAL)
def test_fhc046_generate_btn_disabled_without_input(page):
    with allure.step("[FHC-046-F] 필수 항목 미선택 상태에서 생성 버튼 비활성화 확인"):
        page.navigate_to_tools()
        page.click_tool_menu(LessonPlanPage.TOOL_NAME)
        logger.error("[FHC-046-F] 필수 항목 미선택 — 생성 버튼 비활성화 확인")
        assert not page.is_generate_btn_enabled(), "필수 항목 미선택 상태에서 생성 버튼이 활성화되어 있음"


@allure.title("[FHC-047-F] 업로드 영역 미표시")
@allure.story("수업지도안 생성 새드케이스")
@allure.severity(allure.severity_level.NORMAL)
def test_fhc047_upload_area_not_visible(page):
    with allure.step("[FHC-047-F] 스크롤 없이 업로드 영역 미표시 확인"):
        page.navigate_to_tools()
        page.click_tool_menu(LessonPlanPage.TOOL_NAME)
        logger.error("[FHC-047-F] 스크롤 없이 업로드 영역 접근 — 미표시 확인")
        assert not page.is_upload_area_visible(), "스크롤 없이 업로드 영역이 표시됨"


@allure.title("[FHC-048-F] 재생성 확인 모달 취소 클릭 시 생성 미진행")
@allure.story("수업지도안 생성 새드케이스")
@allure.severity(allure.severity_level.NORMAL)
def test_fhc048_cancel_regeneration_modal(page):
    with allure.step("[FHC-048-F] 다시 생성 클릭 후 모달에서 취소 클릭"):
        page.navigate_to_tools()
        page.click_tool_menu(LessonPlanPage.TOOL_NAME)
        page.regen_with_random_values()
        logger.error("[FHC-048-F] 재생성 확인 모달에서 취소 클릭 — 생성 미진행 확인")
        assert page.click_generate_and_cancel(), "재생성 확인 모달 취소 처리 실패"


@allure.title("[FHC-049-F] 재생성 1분 초과 시 실패")
@allure.story("수업지도안 생성 새드케이스")
@allure.severity(allure.severity_level.NORMAL)
def test_fhc049_regeneration_timeout(page):
    with allure.step("[FHC-049-F] 재생성 타임아웃 발생 확인"):
        logger.error("[FHC-049-F] 재생성 타임아웃 — 1분 초과 시 실패 확인")
        assert not page.wait_for_regeneration(timeout=1), "타임아웃(1초) 내 재생성이 완료됨"
