# tests/test_tools_06.py
# 심층 조사 도구 E2E 테스트 — FHC-057 ~ FHC-063

import pytest
import logging
import allure
from pages.tools.tools_deep_page import DeepPage

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Tools"),
    allure.feature("심층 조사"),
]


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def deep(login_module):
    """
    심층 조사 도구 fixture (모듈 공유)

    전제: login_module fixture로 로그인 완료 상태
    단계:
      1. login_module에서 (driver, wait) 수신 → DeepPage 생성
      2. LNB 도구 메뉴 진입 및 심층 조사 도구 초기 세팅
    """
    tool = DeepPage(login_module)
    tool.tools_LNB()
    tool.setup_tool()
    return tool


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("심층 조사 메뉴 확인")
@allure.title("[FHC-057] '심층 조사' 메뉴 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_057_navigate_to_deep_research(deep):
    """
    [FHC-057] '심층 조사' 메뉴 확인

    전제: 로그인 완료 상태
    단계:
      1. LNB > '도구' 탭 클릭
      2. '심층 조사' 메뉴 클릭
    기대: '심층 조사' 페이지 타이틀 확인
    """
    logger.info("[FHC-057] 심층 조사 페이지 진입 확인 시작")
    deep.is_tool_page_displayed()
    logger.info("[FHC-057] 심층 조사 페이지 진입 확인 완료")


@allure.story("주제만 입력 버튼 활성화")
@allure.title("[FHC-058] 주제만 입력 → [자동 생성] 버튼 활성화 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_058_topic_only_btn_enabled(deep):
    """
    [FHC-058] 주제만 입력 → [자동 생성] 버튼 활성화 확인

    전제: test_FHC_057 이어서 심층 조사 페이지 상태
    단계:
      1. 주제 입력 필드에 '날씨' 입력
      2. 지시사항 필드 비움
    기대:
      - 토큰 정상: [자동 생성] 버튼 활성화
      - 토큰 소진: 버튼 비활성화 (xfail)
    """
    logger.info("[FHC-058] 주제만 입력 → 버튼 활성화 확인 시작")
    deep.enter_text(DeepPage.TOPIC_INPUT, DeepPage.TOPIC_TEXT)
    deep.enter_text(DeepPage.MESSAGE_INPUT, "")
    deep.assert_generate_btn_enabled()
    logger.info("[FHC-058] 주제만 입력 → 버튼 활성화 확인 완료")


@allure.story("주제 지시사항 입력 버튼 활성화")
@allure.title("[FHC-059] 주제 + 지시사항 입력 → [자동 생성] 버튼 활성화 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_059_topic_and_message_btn_enabled(deep):
    """
    [FHC-059] 주제 + 지시사항 입력 → [자동 생성] 버튼 활성화 확인

    전제: test_FHC_058 이어서 주제 입력 완료 상태
    단계:
      1. 지시사항 필드에 '대한민국 서울의 2026년 5월의 날씨' 입력
    기대:
      - 토큰 정상: [자동 생성] 버튼 활성화
      - 토큰 소진: 버튼 비활성화 (xfail)
    """
    logger.info("[FHC-059] 주제 + 지시사항 입력 → 버튼 활성화 확인 시작")
    deep.enter_text(DeepPage.MESSAGE_INPUT, DeepPage.MESSAGE_TEXT)
    deep.assert_generate_btn_enabled()
    logger.info("[FHC-059] 주제 + 지시사항 입력 → 버튼 활성화 확인 완료")



@allure.story("생성 버튼 클릭 생성 시작 확인")
@allure.title("[FHC-060] 생성 버튼 클릭 → 생성 시작 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_060_generate_start(deep):
    """
    [FHC-060] 생성 버튼 클릭 → 생성 시작 확인

    전제: test_FHC_059 이어서 주제 + 지시사항 입력 완료 상태
    단계:
      1. [자동 생성] 버튼 클릭
      2. 로딩 스피너 확인
    기대:
      - 토큰 소진: xfail
      - 토큰 정상: 로딩 스피너 표시 (생성 시작)
    """
    logger.info("[FHC-060] 생성 버튼 클릭 → 생성 시작 확인 시작")
    if deep.is_token_exhausted():
        pytest.xfail("토큰 한도 소진으로 생성 불가")
    deep.click_generate()
    assert deep.is_generating(), "생성이 시작되지 않았습니다"
    logger.info("[FHC-060] 생성 버튼 클릭 → 생성 시작 확인 완료")


@pytest.mark.slow
@allure.story("생성 버튼 클릭 생성 완료 확인")
@allure.title("[FHC-060] 생성 버튼 클릭 → 생성 완료 확인 (slow)")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_060_generate_complete(deep):
    """
    [FHC-060] 생성 완료 확인 (최대 10분 소요 — slow 테스트)

    전제: test_FHC_060_generate_start 이어서 생성 중인 상태
    단계:
      1. 생성 완료 체크 아이콘 확인 (최대 10분)
    기대: 10분 이내 생성 완료
    """
    logger.info("[FHC-060] 생성 완료 확인 시작")
    if deep.is_token_exhausted():
        pytest.xfail("토큰 한도 소진으로 생성 불가")
    assert deep.is_generated(timeout=600), "10분 이내 생성 실패"
    logger.info("[FHC-060] 생성 완료 확인 완료")


@allure.story("주제 공백 입력 오류 메시지")
@allure.title("[FHC-061] 주제 공백 입력 시 오류 메시지 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_061_blank_topic_error(deep):
    """
    [FHC-061] 주제 공백 입력 시 오류 메시지 확인

    전제: test_FHC_060 이어서 심층 조사 페이지 상태
    단계:
      1. 생성 중이면 정지
      2. 주제 필드에 공백(' ') 입력
      3. 지시사항 필드 비움
      4. [자동 생성] 버튼 클릭
    기대: '답변 생성에 문제가 발생했습니다.' 오류 메시지 표시
    """
    logger.info("[FHC-061] 주제 공백 입력 시 오류 메시지 확인 시작")
    deep.stop_if_generating()
    deep.enter_text(DeepPage.TOPIC_INPUT, DeepPage.TOPIC_BLANK)
    deep.enter_text(DeepPage.MESSAGE_INPUT, "")
    deep.click_generate()
    assert deep.is_error_alert_displayed(), "오류 메시지가 표시되지 않았습니다"
    logger.info("[FHC-061] 주제 공백 입력 시 오류 메시지 확인 완료")


@allure.story("주제 500자 입력 버튼 활성화 경계값")
@allure.title("[FHC-062] 주제 500자 입력 → [자동 생성] 버튼 활성화 확인 (경계값)")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_062_topic_500_chars_btn_enabled(deep):
    """
    [FHC-062] 주제 500자 입력 → [자동 생성] 버튼 활성화 확인 (경계값)

    전제: test_FHC_061 이어서 심층 조사 페이지 상태
    단계:
      1. 생성 중이면 정지
      2. 주제 필드에 500자 입력 ('가' * 500)
    기대:
      - 토큰 정상: [자동 생성] 버튼 활성화 (500자 허용 범위 내)
      - 토큰 소진: 버튼 비활성화 (xfail)
    """
    logger.info("[FHC-062] 주제 500자 입력 → 버튼 활성화 확인 시작")
    deep.stop_if_generating()
    deep.enter_text(DeepPage.TOPIC_INPUT, DeepPage.TOPIC_500_CHARS)
    deep.assert_generate_btn_enabled()
    logger.info("[FHC-062] 주제 500자 입력 → 버튼 활성화 확인 완료")


@allure.story("주제 501자 입력 버튼 비활성화 경계값")
@allure.title("[FHC-063] 주제 501자 입력 → [자동 생성] 버튼 비활성화 확인 (경계값)")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_063_topic_501_chars_btn_disabled(deep):
    """
    [FHC-063] 주제 501자 입력 → [자동 생성] 버튼 비활성화 확인 (경계값)

    전제: test_FHC_062 이어서 심층 조사 페이지 상태
    단계:
      1. 생성 중이면 정지
      2. 주제 필드에 501자 입력 ('가' * 501)
    기대: [자동 생성] 버튼 비활성화 (501자 허용 범위 초과)
    """
    logger.info("[FHC-063] 주제 501자 입력 → 버튼 비활성화 확인 시작")
    deep.stop_if_generating()
    deep.enter_text(DeepPage.TOPIC_INPUT, DeepPage.TOPIC_501_CHARS)
    deep.assert_generate_btn_disabled()
    logger.info("[FHC-063] 주제 501자 입력 → 버튼 비활성화 확인 완료")
