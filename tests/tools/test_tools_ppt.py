# tests/tools/test_tools_ppt.py
# PPT 생성 도구 E2E 테스트 — FHC-050 ~ FHC-053

import pytest
import logging
import allure
from pages.tools.tools_ppt_page import PPTPage
from config.settings import DOWNLOAD_DIR

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Tools"),
    allure.feature("PPT 생성"),
    allure.story("PPT 생성 해피 케이스"),
]

TOPIC        = "AI"
INSTRUCTIONS = "간략하고 빠르게 생성"


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def ppt(login_module):
    driver, wait = login_module
    return PPTPage(driver, wait)


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.title("[FHC-050~053] PPT 생성 해피 케이스 (다운로드 포함)")
@allure.severity(allure.severity_level.NORMAL)
def test_ppt_happy_case(ppt):
    """
    [FHC-050~053] PPT 생성 해피 케이스

    전제: 로그인 완료 상태
    단계:
      1. [FHC-050] LNB > '도구' 탭 > 'PPT 생성' 메뉴 클릭
      2. [FHC-051] 필수 항목(주제) 및 선택 항목(지시사항, 슬라이드 수, 섹션 수) 입력
      3. [FHC-052] 심층조사 모드 토글 전환 확인
      4. [FHC-053] 자동 생성 버튼 클릭 → 생성 완료 후 다운로드
    기대: 생성 및 다운로드 모두 정상 완료
    """
    with allure.step("[FHC-050] PPT 생성 메뉴 이동"):
        logger.info("[FHC-050] PPT 생성 메뉴 이동 시작")
        ppt.navigate_to_tools()
        ppt.click_tool_menu(PPTPage.TOOL_NAME)

    with allure.step("[FHC-051] 필수 항목 및 선택 항목 입력"):
        logger.info("[FHC-051] 항목 입력 시작")
        if ppt.has_any_field_value():
            ppt.clear_all_fields()
        ppt.enter_topic(TOPIC)
        ppt.enter_instructions(INSTRUCTIONS)
        ppt.enter_slides_count()
        ppt.enter_section_count()

    with allure.step("[FHC-052] 심층조사 모드 토글 전환 확인"):
        logger.info("[FHC-052] 심층조사 모드 토글 확인 시작")
        ppt.click_deep_research_toggle()

    with allure.step("[FHC-053] '다시 생성' 버튼 클릭"):
        logger.info("[FHC-053] 다시 생성 시작")
        ppt.scroll_to_generate_btn()
        ppt.click_generate()
        ppt.wait_for_regeneration(timeout=120)

    with allure.step("[FHC-053] PPT 다운로드"):
        logger.info("[FHC-053] PPT 다운로드 시작")
        ppt.download_result(DOWNLOAD_DIR)

    logger.info("[FHC-050~053] PPT 생성 해피 케이스 완료")
