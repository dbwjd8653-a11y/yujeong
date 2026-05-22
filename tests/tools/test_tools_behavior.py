# tests/test_tools_02.py
# '행동특성 및 종합의견' 도구 E2E 테스트 — FHC-037 ~ FHC-044

import pytest
import allure

from pages.tools.tools_behavior_page import BehaviorPage

from config.settings import DOWNLOAD_DIR

pytestmark = [
    allure.epic("Tools"),
    allure.feature("행동특성 및 종합의견"),
]

SCHOOL_LEVEL  = "중학교"
NAME_TEXT     = "포커스 1차 프로젝트"
REQUEST_TEXT  = "엘리스 부트 캠프"


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def behavior(tools_driver_module):
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

@allure.story("도구 목록 표시 확인")
@allure.title("[FHC-037] 도구 목록 표시 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_037_tools_list_displayed(behavior):
    """
    [FHC-037] 도구 목록 표시 확인

    전제: 로그인 한 상태
    단계:
      1. LNB 또는 직접 URL로 도구(Tools) 페이지 이동
    기대: 도구 카드 목록이 표시된다
    """
    behavior.navigate_to_tools()
    assert behavior.is_tools_list_displayed(), \
        "도구 목록 페이지에 도구 카드가 표시되지 않았습니다"


@allure.story("행동특성 및 종합의견 도구 선택")
@allure.title("[FHC-038] '행동특성 및 종합의견' 도구 선택")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_038_navigate_to_behavior(behavior):
    """
    [FHC-038] '행동특성 및 종합의견' 도구 선택

    전제: 도구 목록 페이지
    단계:
      1. '행동특성 및 종합의견' 도구 클릭
    기대: 행동특성 및 종합의견 도구 상세 페이지로 이동한다
    """
    behavior.click_tool_menu(BehaviorPage.TOOL_NAME)
    assert behavior.is_on_tool_page(), \
        "행동특성 및 종합의견 도구 페이지로 이동하지 못했습니다"


@allure.story("입력 내역 초기화")
@allure.title("[FHC-039] 입력 내역 초기화")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_039_reset_inputs(behavior):
    """
    [FHC-039] 입력 내역 초기화

    전제: 행동특성 및 종합의견 도구 페이지
    단계:
      1. '입력 내역 초기화' 버튼 클릭
      2. 확인 모달에서 '초기화 하기' 클릭
    기대: 이전 입력값이 초기화되고 수업 정보 탭이 표시된다
    """
    behavior.reset_inputs()
    assert behavior.is_class_info_tab_visible(), \
        "초기화 완료 후 수업 정보 입력 탭이 표시되지 않았습니다"


@allure.story("수업 정보 입력 탭 이동 및 학교급 선택")
@allure.title("[FHC-040] 수업 정보 입력 탭 이동 및 학교급 선택")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_040_class_info_and_school_level(behavior):
    """
    [FHC-040] 수업 정보 입력 탭 이동 및 학교급 선택

    전제: 초기화 완료 상태
    단계:
      1. '수업 정보 입력' 탭 클릭
      2. 학교급 선택
    기대: 학교급이 선택되어 '다음으로' 버튼이 활성화된다
    """
    behavior.click_class_info_tab()
    assert behavior.is_school_level_combobox_visible(), \
        "수업 정보 입력 화면(학교급 콤보박스)이 표시되지 않았습니다"
    behavior.select_school_level(SCHOOL_LEVEL)
    assert behavior.is_next_button_enabled(), \
        f"학교급 '{SCHOOL_LEVEL}' 선택 후 '다음으로' 버튼이 활성화되지 않았습니다"


@allure.story("다음으로 버튼 클릭 학생 정보 화면 이동")
@allure.title("[FHC-041] '다음으로' 버튼 클릭 → 학생 정보 화면 이동")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_041_click_next_to_student(behavior):
    """
    [FHC-041] '다음으로' 버튼 클릭 → 학생 정보 화면 이동

    전제: 수업 정보(학교급) 입력 완료
    단계:
      1. '다음으로' 버튼 클릭 (수정 모달 발생 시 '수정하기' 처리)
    기대: 학생 정보 입력 화면으로 이동한다
    """
    behavior.click_next()
    behavior.handle_modify_modal()
    assert behavior.is_student_tab_visible(), \
        "학생 정보 입력 화면으로 이동하지 못했습니다"


@allure.story("학생 이름 입력")
@allure.title("[FHC-042] 학생 이름 입력")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_042_enter_student_name(behavior):
    """
    [FHC-042] 학생 이름 입력

    전제: 학생 정보 입력 화면
    단계:
      1. 학생 이름 입력 행에 이름 입력
    기대: 입력한 이름이 반영된다
    """
    behavior.ensure_student_row_exists()
    behavior.enter_student_name(NAME_TEXT)
    assert behavior.is_student_name_entered(NAME_TEXT), \
        f"학생 이름 '{NAME_TEXT}'이 입력 필드에 반영되지 않았습니다"


@allure.story("인성·태도 키워드 선택 및 저장")
@allure.title("[FHC-043] 인성·태도 키워드 선택 및 저장")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_043_select_and_save_keyword(behavior):
    """
    [FHC-043] 인성·태도 키워드 선택 및 저장

    전제: 학생 이름 입력 완료
    단계:
      1. 키워드 버튼 클릭
      2. 인성·태도 아코디언 → '예의 바르고 배려심 있음' 선택
      3. 저장
    기대: 키워드가 저장되고 '생성 결과 받기' 버튼이 표시된다
    """
    behavior.open_keyword_modal()
    behavior.select_character_keyword()
    behavior.save_keyword_modal()
    if REQUEST_TEXT:
        behavior.enter_request_text(REQUEST_TEXT)
    assert behavior.is_result_button_visible(), \
        "키워드 저장 후 '생성 결과 받기' 버튼이 표시되지 않았습니다"


@pytest.mark.slow
@allure.story("AI 생성 및 결과 파일 다운로드")
@allure.title("[FHC-044] AI 생성 및 결과 파일 다운로드")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_044_generate_and_download(behavior):
    """
    [FHC-044] AI 생성 및 결과 파일 다운로드

    전제: 키워드 저장 완료
    단계:
      1. '+ 학생 추가' 버튼으로 AI 생성 트리거
      2. 학생 검색
      3. '생성 결과 받기' 클릭
    기대: xlsx 결과 파일이 정상적으로 다운로드된다
    """
    behavior.trigger_generation()
    behavior.search_student(NAME_TEXT)
    result = behavior.download_result(DOWNLOAD_DIR)
    assert result, "xlsx 결과 파일 다운로드에 실패했습니다"
