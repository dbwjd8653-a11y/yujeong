# tests/test_tools_01.py
# '세부 특기사항' 도구 E2E 테스트 — FHC-028 ~ FHC-036

import logging
import pytest
import allure

from pages.tools.tools_specialty_page import SpecialtyPage
from config.settings import DOWNLOAD_DIR

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Tools"),
    allure.feature("세부 특기사항"),
    allure.story("세부 특기사항 생성 해피 케이스"),
]

SCHOOL_LEVEL  = "중학교"
GRADE         = "3학년"
SUBJECT       = "수학"
UNIT          = "1"
NAME_TEXT     = "포커스 1차 프로젝트"
REQUEST_TEXT  = ""


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def specialty(tools_driver_module):
    """
    SpecialtyPage fixture (모듈 공유)

    전제: tools_driver_module fixture로 로그인 완료 상태
    단계:
      1. tools_driver_module에서 driver 수신 → SpecialtyPage 반환
    """
    page = SpecialtyPage(tools_driver_module)
    page.login()
    return page


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.title("[FHC-028~036] 세부 특기사항 생성 해피 케이스")
@allure.severity(allure.severity_level.NORMAL)
def test_specialty_happy_case(specialty):
    """
    [FHC-028~036] 세부 특기사항 생성 해피 케이스

    전제: 로그인 완료 상태
    단계:
      1. [FHC-028] LNB 또는 직접 URL로 도구(Tools) 페이지 이동
      2. [FHC-029] '세부 특기사항' 도구 클릭
      3. [FHC-030] 입력 내역 초기화
      4. [FHC-031] '수업 정보 입력' 탭 클릭
      5. [FHC-032] 학교급 / 학년 / 과목 / 단원 입력
      6. [FHC-033] '다음으로' 버튼 클릭 → 학생 정보 화면 이동
      7. [FHC-034] 학생 이름 입력
      8. [FHC-035] 학습 태도 키워드 선택 및 저장
      9. [FHC-036] AI 생성 및 결과 파일 다운로드
    기대: 전체 시나리오 정상 완료
    """
    with allure.step("[FHC-028] 도구 목록 표시 확인"):
        logger.info("[FHC-028] 도구 목록 표시 확인 시작")
        with allure.step("g: 도구 페이지로 이동 → 도구 카드 목록 표시 확인"):
            specialty.navigate_to_tools()
            assert specialty.is_tools_list_displayed(), \
                "도구 목록 페이지에 도구 카드가 표시되지 않았습니다"

    with allure.step("[FHC-029] '세부 특기사항' 도구 선택"):
        logger.info("[FHC-029] 세부 특기사항 도구 선택 시작")
        with allure.step("g: 세부 특기사항 클릭 → 도구 상세 페이지 이동 확인"):
            specialty.click_tool_menu(SpecialtyPage.TOOL_NAME)
            assert specialty.is_on_tool_page(), \
                "세부 특기사항 도구 페이지로 이동하지 못했습니다"

    with allure.step("[FHC-030] 입력 내역 초기화"):
        logger.info("[FHC-030] 입력 내역 초기화 시작")
        with allure.step("g: 초기화 클릭 → 수업 정보 입력 탭 표시 확인"):
            specialty.reset_inputs()
            assert specialty.is_class_info_tab_visible(), \
                "초기화 완료 후 수업 정보 입력 탭이 표시되지 않았습니다"

    with allure.step("[FHC-031] 수업 정보 입력 탭 이동"):
        logger.info("[FHC-031] 수업 정보 입력 탭 이동 시작")
        with allure.step("g: 수업 정보 입력 탭 클릭 → 학교급 콤보박스 표시 확인"):
            specialty.click_class_info_tab()
            assert specialty.is_school_level_combobox_visible(), \
                "수업 정보 입력 화면(학교급 콤보박스)이 표시되지 않았습니다"

    with allure.step("[FHC-032] 수업 정보 입력 (학교급 / 학년 / 과목 / 단원)"):
        logger.info("[FHC-032] 수업 정보 입력 시작")
        with allure.step("g: 학교급 / 학년 / 과목 / 단원 입력 → 다음으로 버튼 활성화 확인"):
            specialty.select_school_level(SCHOOL_LEVEL)
            specialty.select_grade(GRADE)
            specialty.enter_subject(SUBJECT)
            specialty.enter_unit(UNIT)
            assert specialty.is_next_button_enabled(), \
                "수업 정보 입력 완료 후 '다음으로' 버튼이 활성화되지 않았습니다"

    with allure.step("[FHC-033] '다음으로' 버튼 클릭 → 학생 정보 화면 이동"):
        logger.info("[FHC-033] 다음으로 버튼 클릭 시작")
        with allure.step("g: 다음으로 클릭 → 학생 정보 입력 화면 이동 확인"):
            specialty.click_next()
            specialty.handle_modify_modal()
            assert specialty.is_student_tab_visible(), \
                "학생 정보 입력 화면으로 이동하지 못했습니다"

    with allure.step("[FHC-034] 학생 이름 입력"):
        logger.info("[FHC-034] 학생 이름 입력 시작")
        with allure.step("g: 학생 이름 입력 → 이름 반영 확인"):
            specialty.ensure_student_row_exists()
            specialty.enter_student_name(NAME_TEXT)
            assert specialty.is_student_name_entered(NAME_TEXT), \
                f"학생 이름 '{NAME_TEXT}'이 입력 필드에 반영되지 않았습니다"

    with allure.step("[FHC-035] 학습 태도 키워드 선택 및 저장"):
        logger.info("[FHC-035] 학습 태도 키워드 선택 및 저장 시작")
        with allure.step("g: 키워드 선택 및 저장 → 생성 결과 받기 버튼 표시 확인"):
            specialty.open_keyword_modal()
            specialty.select_study_attitude_keyword()
            specialty.save_keyword_modal()
            if REQUEST_TEXT:
                specialty.enter_request_text(REQUEST_TEXT)
            assert specialty.is_result_button_visible(), \
                "키워드 저장 후 '생성 결과 받기' 버튼이 표시되지 않았습니다"

    with allure.step("[FHC-036] AI 생성 및 결과 파일 다운로드"):
        logger.info("[FHC-036] AI 생성 및 다운로드 시작")
        with allure.step("g: AI 생성 트리거 → xlsx 파일 다운로드 확인"):
            specialty.trigger_generation()
            specialty.search_student(NAME_TEXT)
            result = specialty.download_result(DOWNLOAD_DIR)
            assert result, "xlsx 결과 파일 다운로드에 실패했습니다"

    logger.info("[FHC-028~036] 세부 특기사항 생성 해피 케이스 완료")
