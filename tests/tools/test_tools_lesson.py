# tests/test_tools_03.py
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
]

SCHOOL_LEVEL   = "중학교"
GRADE          = "3학년"
SUBJECT        = "수학"
TOPIC          = "교육"
PERIOD         = "1"
METHOD         = "basic"
COMMENT        = "없음"
REFERENCE_FILE = os.path.join(os.path.dirname(__file__), "../fixtures/file_choose_test.pdf")


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def page(login_module):
    """
    수업지도안 페이지 fixture (모듈 공유)

    전제: login_module fixture로 로그인 완료 상태
    단계:
      1. login_module에서 (driver, wait) 수신 → LessonPlanPage 반환
    """
    driver, wait = login_module
    return LessonPlanPage(driver, wait)


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("수업지도안 메뉴 확인")
@allure.title("[FHC-045] '수업지도안' 메뉴 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_045_navigate_to_lesson_plan(page):
    """
    [FHC-045] '수업지도안' 메뉴 확인

    전제: 로그인 완료 상태
    단계:
      1. LNB > '도구' 탭 클릭
      2. '수업지도안' 메뉴 클릭
    기대: '수업지도안' 탭 확인
    """
    logger.info("[FHC-045] 수업지도안 메뉴 확인 시작")
    page.navigate_to_tools()
    page.click_tool_menu(LessonPlanPage.TOOL_NAME)
    assert page.is_on_tool_page(), "수업지도안 페이지 미이동"
    logger.info("[FHC-045] 수업지도안 메뉴 확인 완료")


@allure.story("수업 내용 입력 필수 항목")
@allure.title("[FHC-046] 수업 내용 입력 (필수 항목만)")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_046_fill_required_fields(page):
    """
    [FHC-046] 수업 내용 입력 (필수 항목만)

    전제: test_FHC_045 이어서 수업지도안 페이지 상태
    단계:
      1. 수업 정보 입력 항목 (교급, 학년, 교과, 수업 차시, 생성 방식) 선택
    기대: [수업지도안 생성] 버튼 활성화
    """
    logger.info("[FHC-046] 필수 항목 입력 시작")
    if page.has_previous_result():
        page.regen_with_different_values()
    else:
        page.select_school_level(SCHOOL_LEVEL)
        page.select_grade(GRADE)
        page.select_subject(SUBJECT)
        page.select_period(PERIOD)
        page.select_generation_method(METHOD)
        assert page.is_generate_btn_enabled(), "[수업지도안 생성] 버튼 미활성화"
    logger.info("[FHC-046] 필수 항목 입력 완료")


@allure.story("수업 내용 입력 선택 항목 포함")
@allure.title("[FHC-047] 수업 내용 입력 (선택 항목 포함)")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_047_fill_with_optional_fields(page):
    """
    [FHC-047] 수업 내용 입력 (선택 항목 포함)

    전제: test_FHC_046 이어서 수업지도안 페이지 상태
    단계:
      1. 참고 자료 업로드 영역 스크롤 확인
      2. 파일 선택 창 활성화 확인
      3. 기타 요청 사항 입력
    기대: [수업지도안 생성] 버튼 활성화
    """
    logger.info("[FHC-047] 선택 항목 포함 입력 시작")
    page.scroll_to_upload_area()
    assert page.is_upload_area_visible(), "업로드 영역 미표시"
    page.upload_reference(os.path.abspath(REFERENCE_FILE))
    page.enter_comment(COMMENT)
    assert page.is_generate_btn_enabled(), "[수업지도안 생성] 버튼 미활성화"
    page.click_generate()
    logger.info("[FHC-047] 선택 항목 포함 입력 완료")


@allure.story("수업지도안 생성 완료")
@allure.title("[FHC-049] 수업지도안 생성 완료")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_049_generate_lesson_plan(page):
    """
    [FHC-049] 수업지도안 생성 완료

    전제: test_FHC_047 이어서 생성 버튼 클릭 상태
    단계:
      1. 생성 완료 대기 (최대 60초)
    기대: AI 답변이 1분 이내 생성
    """
    logger.info("[FHC-049] 수업지도안 생성 완료 확인 시작")
    assert page.wait_for_generation(timeout=60), "수업지도안 1분 이내 생성 실패"
    logger.info("[FHC-049] 수업지도안 생성 완료 확인 완료")
