# tests/test_tools_01.py
# '세부 특기사항' 도구 E2E 테스트 — FHC-028 ~ FHC-036

import pytest

from pages.tools.tools_specialty_page import SpecialtyPage

from config.settings import DOWNLOAD_DIR

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

def test_FHC_028_tools_list_displayed(specialty):
    """
    [FHC-028] 도구 목록 표시 확인

    전제: 로그인 한 상태
    단계:
      1. LNB 또는 직접 URL로 도구(Tools) 페이지 이동
    기대: 도구 카드 목록이 표시된다
    """
    specialty.navigate_to_tools()
    assert specialty.is_tools_list_displayed(), \
        "도구 목록 페이지에 도구 카드가 표시되지 않았습니다"


def test_FHC_029_navigate_to_specialty(specialty):
    """
    [FHC-029] '세부 특기사항' 도구 선택

    전제: 도구 목록 페이지
    단계:
      1. '세부 특기사항' 도구 클릭
    기대: 세부 특기사항 도구 상세 페이지로 이동한다
    """
    specialty.click_tool_menu(SpecialtyPage.TOOL_NAME)
    assert specialty.is_on_tool_page(), \
        "세부 특기사항 도구 페이지로 이동하지 못했습니다"


def test_FHC_030_reset_inputs(specialty):
    """
    [FHC-030] 입력 내역 초기화

    전제: 세부 특기사항 도구 페이지
    단계:
      1. '입력 내역 초기화' 버튼 클릭
      2. 확인 모달에서 '초기화 하기' 클릭
    기대: 이전 입력값이 초기화되고 수업 정보 탭이 표시된다
    """
    specialty.reset_inputs()
    assert specialty.is_class_info_tab_visible(), \
        "초기화 완료 후 수업 정보 입력 탭이 표시되지 않았습니다"


def test_FHC_031_class_info_tab(specialty):
    """
    [FHC-031] 수업 정보 입력 탭 이동

    전제: 세부 특기사항 도구 페이지, 초기화 완료
    단계:
      1. '수업 정보 입력' 탭 클릭
    기대: 학교급 선택 콤보박스를 포함한 수업 정보 입력 화면이 표시된다
    """
    specialty.click_class_info_tab()
    assert specialty.is_school_level_combobox_visible(), \
        "수업 정보 입력 화면(학교급 콤보박스)이 표시되지 않았습니다"


def test_FHC_032_fill_class_info(specialty):
    """
    [FHC-032] 수업 정보 입력 (학교급 / 학년 / 과목 / 단원)

    전제: 수업 정보 입력 탭 활성화 상태
    단계:
      1. 학교급 / 학년 / 과목 / 단원 순서로 입력
    기대: 모든 항목이 입력되어 '다음으로' 버튼이 활성화된다
    """
    specialty.select_school_level(SCHOOL_LEVEL)
    specialty.select_grade(GRADE)
    specialty.enter_subject(SUBJECT)
    specialty.enter_unit(UNIT)
    assert specialty.is_next_button_enabled(), \
        "수업 정보 입력 완료 후 '다음으로' 버튼이 활성화되지 않았습니다"


def test_FHC_033_click_next_to_student(specialty):
    """
    [FHC-033] '다음으로' 버튼 클릭 → 학생 정보 화면 이동

    전제: 수업 정보 입력 완료
    단계:
      1. '다음으로' 버튼 클릭 (수정 모달 발생 시 '수정하기' 처리)
    기대: 학생 정보 입력 화면으로 이동한다
    """
    specialty.click_next()
    specialty.handle_modify_modal()
    assert specialty.is_student_tab_visible(), \
        "학생 정보 입력 화면으로 이동하지 못했습니다"


def test_FHC_034_enter_student_name(specialty):
    """
    [FHC-034] 학생 이름 입력

    전제: 학생 정보 입력 화면
    단계:
      1. 학생 이름 입력 행에 이름 입력
    기대: 입력한 이름이 반영된다
    """
    specialty.ensure_student_row_exists()
    specialty.enter_student_name(NAME_TEXT)
    assert specialty.is_student_name_entered(NAME_TEXT), \
        f"학생 이름 '{NAME_TEXT}'이 입력 필드에 반영되지 않았습니다"


def test_FHC_035_select_and_save_keyword(specialty):
    """
    [FHC-035] 학습 태도 키워드 선택 및 저장

    전제: 학생 이름 입력 완료
    단계:
      1. 키워드 버튼 클릭
      2. 학습 태도 아코디언 → '수업 집중도 높음' 선택
      3. 저장
    기대: 키워드가 저장되고 '생성 결과 받기' 버튼이 표시된다
    """
    specialty.open_keyword_modal()
    specialty.select_study_attitude_keyword()
    specialty.save_keyword_modal()
    if REQUEST_TEXT:
        specialty.enter_request_text(REQUEST_TEXT)
    assert specialty.is_result_button_visible(), \
        "키워드 저장 후 '생성 결과 받기' 버튼이 표시되지 않았습니다"


def test_FHC_036_generate_and_download(specialty):
    """
    [FHC-036] AI 생성 및 결과 파일 다운로드

    전제: 키워드 저장 완료
    단계:
      1. '+ 학생 추가' 버튼으로 AI 생성 트리거
      2. 학생 검색
      3. '생성 결과 받기' 클릭
    기대: xlsx 결과 파일이 정상적으로 다운로드된다
    """
    specialty.trigger_generation()
    specialty.search_student(NAME_TEXT)
    result = specialty.download_result(DOWNLOAD_DIR)
    assert result, "xlsx 결과 파일 다운로드에 실패했습니다"
