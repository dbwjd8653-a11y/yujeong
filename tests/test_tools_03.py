# test_tools_03.py
# '수업지도안' 도구 E2E 테스트
# FHC-044 / FHC-045 / FHC-046 / FHC-047

import pytest
from pages.tools.lesson_plan_page import LessonPlanPage

# ─── 테스트 설정값 ────────────────────────────────────────────────────────────
SCHOOL_LEVEL  = "중학교"
GRADE         = "3학년"
SUBJECT       = "수학"
TOPIC         = "교육"
PERIOD        = "1"
METHOD        = "basic"
COMMENT       = "없음"
# ─────────────────────────────────────────────────────────────────────────────


# 로그인 후 LessonPlanPage 객체를 모듈 전체에서 공유
@pytest.fixture(scope="module")
def page(driver_module):
    p = LessonPlanPage(driver_module)
    p.login()
    return p


# ========== FHC-044: 수업지도안 메뉴 확인 ==========

def test_FHC_044_navigate_to_lesson_plan(page):
    page.navigate_to_tools()
    page.click_tool_menu(LessonPlanPage.TOOL_NAME)
    assert page.is_on_tool_page(), "수업지도안 도구 페이지로 이동하지 못했습니다"


# ========== FHC-045: 수업 내용 입력 (필수 항목만) ==========

def test_FHC_045_fill_required_fields(page):
    if page.has_previous_result():
        page.regen_with_different_values()
    else:
        page.select_school_level(SCHOOL_LEVEL)
        page.select_grade(GRADE)
        page.select_subject(SUBJECT)
        page.select_period(PERIOD)
        page.select_generation_method(METHOD)
        assert page.is_generate_btn_enabled(), \
            "필수 항목 입력 완료 후 [수업지도안 생성] 버튼이 활성화되지 않았습니다"


# ========== FHC-046: 수업 내용 입력 (선택 항목 포함) ==========

def test_FHC_046_fill_with_optional_fields(page):
    page.scroll_to_upload_area()
    assert page.is_upload_area_visible(), "참고자료 업로드 영역이 화면에 표시되지 않았습니다"
    assert page.click_upload_area_and_verify(), "파일 선택 창이 활성화되지 않았습니다"
    page.enter_comment(COMMENT)
    assert page.is_generate_btn_enabled(), \
        "선택 항목 포함 입력 완료 후 [수업지도안 생성] 버튼이 활성화되지 않았습니다"
    page.click_generate()


# ========== FHC-047: 수업지도안 생성 완료 ==========

def test_FHC_047_generate_lesson_plan(page):
    assert page.wait_for_generation(timeout=60), \
        "수업지도안 AI 생성이 1분 이내에 완료되지 않았습니다"
    import time
    time.sleep(1)
    page.driver.quit()
    print("브라우저 닫기 완료")
