# tests/test_tools_04.py
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
]

TOPIC        = "AI"
INSTRUCTIONS = "간략하고 빠르게 생성"


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def ppt(login_module):
    """
    PPT 생성 페이지 fixture (모듈 공유)

    전제: login_module fixture로 로그인 완료 상태
    단계:
      1. login_module에서 (driver, wait) 수신 → PPTPage 반환
    """
    driver, wait = login_module
    return PPTPage(driver, wait)


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("PPT 생성 메뉴 확인")
@allure.title("[FHC-050] 'PPT 생성' 메뉴 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_050_navigate_to_ppt(ppt):
    """
    [FHC-050] 'PPT 생성' 메뉴 확인

    전제: 로그인 완료 상태
    단계:
      1. LNB > '도구' 탭 클릭
      2. 'PPT 생성' 메뉴 클릭
    기대: 'PPT 생성' 탭 확인
    """
    logger.info("[FHC-050] PPT 생성 메뉴 확인 시작")
    ppt.navigate_to_tools()
    ppt.click_tool_menu(PPTPage.TOOL_NAME)
    assert ppt.is_on_tool_page(), "PPT 생성 페이지 미이동"
    logger.info("[FHC-050] PPT 생성 메뉴 확인 완료")


@allure.story("PPT 생성 내용 입력 필수 항목")
@allure.title("[FHC-051] PPT 생성 내용 입력 (필수 항목만)")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_051_fill_required_fields(ppt):
    """
    [FHC-051] PPT 생성 내용 입력 (필수 항목만)

    전제: test_FHC_050 이어서 PPT 생성 페이지 상태
    단계:
      1. 초기화 확인 (버튼 비활성화)
      2. 주제(AI) 입력
    기대: [자동 생성] 버튼 활성화
    """
    logger.info("[FHC-051] PPT 필수 항목 입력 시작")
    if ppt.has_any_field_value():
        ppt.clear_all_fields()
    ppt.scroll_to_generate_btn()
    assert not ppt.is_generate_btn_enabled(), "초기화 후 버튼 비활성화 실패"
    ppt.enter_topic(TOPIC)
    ppt.scroll_to_generate_btn()
    assert ppt.is_generate_btn_enabled(), "[자동 생성] 버튼 미활성화"
    logger.info("[FHC-051] PPT 필수 항목 입력 완료")


@allure.story("PPT 생성 내용 입력 선택 항목 포함")
@allure.title("[FHC-051] PPT 생성 내용 입력 (선택 항목 포함)")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_051_fill_with_optional_fields(ppt):
    """
    [FHC-051] PPT 생성 내용 입력 (선택 항목 포함)

    전제: test_FHC_051 이어서 주제 입력 완료 상태
    단계:
      1. 지시사항 입력
      2. 슬라이드 수 입력
      3. 섹션 수 입력
    기대: [자동 생성] 버튼 활성화 유지
    """
    logger.info("[FHC-051] PPT 선택 항목 포함 입력 시작")
    assert ppt.is_generate_btn_enabled(), "[자동 생성] 버튼 미활성화"
    ppt.enter_instructions(INSTRUCTIONS)
    ppt.enter_slides_count()
    ppt.enter_section_count()
    assert ppt.is_generate_btn_enabled(), "선택 항목 입력 후 버튼 미활성화"
    logger.info("[FHC-051] PPT 선택 항목 포함 입력 완료")


@allure.story("심층조사 모드 토글 확인")
@allure.title("[FHC-052] '심층조사 모드' 토글 활성화/비활성화 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_052_deep_research_toggle(ppt):
    """
    [FHC-052] '심층조사 모드' 토글 활성화/비활성화 확인

    전제: test_FHC_051 이어서 PPT 생성 페이지 상태
    단계:
      1. '심층조사 모드' 토글 클릭
    기대:
      - 기존 OFF → ON 전환
      - 기존 ON → OFF 전환
    """
    logger.info("[FHC-052] 심층조사 모드 토글 확인 시작")
    before = ppt.is_deep_research_on()
    ppt.click_deep_research_toggle()
    after = ppt.is_deep_research_on()
    assert before != after, f"토글 전환 실패 (전: {before}, 후: {after})"
    logger.info("[FHC-052] 심층조사 모드 토글 확인 완료")


@pytest.mark.slow
@allure.story("PPT 생성 결과 다운로드")
@allure.title("[FHC-053] PPT 생성 결과 다운로드")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_053_download_ppt(ppt):
    """
    [FHC-053] PPT 생성 결과 다운로드

    전제: test_FHC_052 이어서 입력 완료 상태
    단계:
      1. [자동 생성] 버튼 클릭
      2. 생성 완료 대기 (최대 2분)
      3. [생성 결과 다운받기] 버튼 클릭
    기대: 파일 경로 선택 창 출력 및 PPT 파일(.pptx) 저장
    """
    logger.info("[FHC-053] PPT 다운로드 시작")
    ppt.click_generate()
    assert ppt.wait_for_generation(timeout=120), "PPT 2분 이내 생성 실패"
    ppt.click_download()
    assert ppt.is_pptx_downloaded(DOWNLOAD_DIR, timeout=30), "PPT 파일 다운로드 실패"
    logger.info("[FHC-053] PPT 다운로드 완료")
