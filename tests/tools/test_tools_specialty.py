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

@pytest.mark.flaky(reruns=2, reruns_delay=3)
@allure.title("[FHC-028~033] 세부 특기사항 폼·네비게이션 검증 (생성 전, 토큰 무관)")
@allure.severity(allure.severity_level.NORMAL)
def test_specialty_form_flow(specialty):
    """
    [FHC-028~033] 세부 특기사항 — 진입·입력·검증 (AI 생성 제외)

    전제: 로그인 완료 상태
    단계:
      1. [FHC-028] LNB > '도구' 탭 클릭 → 도구 목록 표시
      2. [FHC-029] '세부 특기사항' 도구 클릭
      3. [FHC-030] 수업 정보 필수 항목 입력 (학교급, 학년, 과목, 단원) → '다음으로' 버튼 활성화
      4. [FHC-031] '다음으로' 버튼 클릭 → '학생 정보 입력 및 생성' 페이지 이동
      5. [FHC-032] 이전 입력 데이터(수업 정보) 반영 확인
      6. [FHC-033] 학생 이름 입력 및 학습 태도 키워드 선택 · 저장 → '생성 결과 받기' 버튼 노출
    기대: 생성 직전까지 폼·네비게이션 정상 (토큰 불필요)
    """
    with allure.step("[FHC-028] 도구 목록 표시 확인"):
        logger.info("[FHC-028] 도구 목록 표시 확인 시작")
        specialty.navigate_to_tools()
        assert specialty.is_tools_list_displayed(), \
            "도구 목록 페이지에 도구 카드가 표시되지 않았습니다"

    with allure.step("[FHC-029] '세부 특기사항' 도구 선택"):
        logger.info("[FHC-029] 세부 특기사항 도구 선택 시작")
        specialty.click_tool_menu(SpecialtyPage.TOOL_NAME)
        assert specialty.is_on_tool_page(), \
            "세부 특기사항 도구 페이지로 이동하지 못했습니다"

    with allure.step("[FHC-030] 수업 정보 입력 준비 (초기화)"):
        logger.info("[FHC-030] 수업 정보 입력 준비 시작")
        specialty.reset_inputs()
        assert specialty.is_class_info_tab_visible(), \
            "초기화 완료 후 수업 정보 입력 탭이 표시되지 않았습니다"

    with allure.step("[FHC-030] 수업 정보 입력 탭 이동"):
        logger.info("[FHC-030] 수업 정보 입력 탭 이동 시작")
        specialty.click_class_info_tab()
        assert specialty.is_school_level_combobox_visible(), \
            "수업 정보 입력 화면(학교급 콤보박스)이 표시되지 않았습니다"

    with allure.step("[FHC-030] 수업 정보 필수 항목 입력 (학교급, 학년, 과목, 단원)"):
        logger.info("[FHC-030] 수업 정보 필수 항목 입력 시작")
        specialty.select_school_level(SCHOOL_LEVEL)
        specialty.select_grade(GRADE)
        specialty.enter_subject(SUBJECT)
        specialty.enter_unit(UNIT)
        assert specialty.is_next_button_enabled(), \
            "수업 정보 입력 완료 후 '다음으로' 버튼이 활성화되지 않았습니다"

    with allure.step("[FHC-031~032] '다음으로' 버튼 클릭 → '학생 정보 입력 및 생성' 페이지 이동 / 이전 입력 데이터 반영 확인"):
        logger.info("[FHC-031] 다음으로 버튼 클릭 시작")
        specialty.click_next()
        specialty.handle_modify_modal()
        assert specialty.is_student_tab_visible(), \
            "학생 정보 입력 및 생성 페이지로 이동하지 못했습니다"

    with allure.step("[FHC-033] 학생 이름 입력"):
        logger.info("[FHC-033] 학생 이름 입력 시작")
        specialty.ensure_student_row_exists()
        specialty.enter_student_name(NAME_TEXT)
        assert specialty.is_student_name_entered(NAME_TEXT), \
            f"학생 이름 '{NAME_TEXT}'이 입력 필드에 반영되지 않았습니다"

    with allure.step("[FHC-033] 학습 태도 키워드 선택 및 저장"):
        logger.info("[FHC-033] 학습 태도 키워드 선택 및 저장 시작")
        specialty.open_keyword_modal()
        specialty.select_study_attitude_keyword()
        specialty.save_keyword_modal()
        if REQUEST_TEXT:
            specialty.enter_request_text(REQUEST_TEXT)
        assert specialty.is_result_button_visible(), \
            "키워드 저장 후 '생성 결과 받기' 버튼이 표시되지 않았습니다"

    logger.info("[FHC-028~033] 세부 특기사항 폼·네비게이션 검증 완료")


@pytest.mark.skip(reason="토큰 한도 소진으로 AI 생성 미완료 — 폼·네비게이션은 test_specialty_form_flow에서 검증")
@allure.title("[FHC-035~036] 세부 특기사항 생성 결과 다운로드")
@allure.severity(allure.severity_level.NORMAL)
def test_specialty_generate_and_download(specialty):
    """
    [FHC-035~036] 세부 특기사항 — AI 생성 및 xlsx 다운로드

    전제: test_specialty_form_flow 이후 실행 (module fixture로 폼 상태 공유)
    단계:
      1. [FHC-035] [학생 추가] 버튼 클릭 → 새 학생 목록 생성(생성 트리거)
      2. [FHC-036] [생성 결과 받기] 버튼 클릭 → xlsx 파일 다운로드
    기대: 생성 완료 후 결과 파일 정상 다운로드
    """
    with allure.step("[FHC-035] '학생 추가' 버튼 클릭 → 새 학생 목록 생성"):
        logger.info("[FHC-035] 학생 추가 버튼 클릭 시작")
        specialty.trigger_generation()

    with allure.step("[FHC-036] '생성 결과 받기' 버튼 클릭 → xlsx 파일 다운로드"):
        logger.info("[FHC-036] 생성 결과 받기 버튼 클릭 시작")
        result = specialty.download_result(DOWNLOAD_DIR)
        assert result, "xlsx 결과 파일 다운로드에 실패했습니다"

    logger.info("[FHC-035~036] 세부 특기사항 생성 결과 다운로드 완료")
