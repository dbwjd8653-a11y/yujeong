# tests/test_tools_05.py
# 퀴즈 생성 도구 E2E 테스트 — FHC-054 ~ FHC-056

import logging
import allure
from pages.tools.tools_quiz_page import QuizPage
import pytest

logger = logging.getLogger(__name__)

pytestmark = [
    allure.epic("Tools"),
    allure.feature("퀴즈 생성"),
]


# ── fixture ────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def quiz(login_module):
    """
    퀴즈 생성 도구 fixture (모듈 공유)

    전제: login_module fixture로 로그인 완료 상태
    단계:
      1. login_module에서 (driver, wait) 수신 → QuizPage 생성
      2. LNB 도구 탭 이동
      3. 퀴즈 생성 도구 초기 세팅
    """
    tool = QuizPage(login_module)
    tool.tools_LNB()
    tool.setup_tool()
    return tool


# ── 테스트 케이스 ──────────────────────────────────────────────────

@allure.story("퀴즈 생성 메뉴 확인")
@allure.title("[FHC-054] '퀴즈 생성' 메뉴 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_054_navigate_to_quiz(quiz):
    """
    [FHC-054] '퀴즈 생성' 메뉴 확인

    전제: 로그인 완료 상태
    단계:
      1. LNB > '도구' 탭 클릭
      2. '퀴즈 생성' 메뉴 클릭
    기대: '퀴즈 생성' 페이지 타이틀 확인
    """
    logger.info("[FHC-054] 퀴즈 생성 페이지 진입 확인 시작")
    quiz.is_tool_page_displayed()
    logger.info("[FHC-054] 퀴즈 생성 페이지 진입 확인 완료")


@allure.story("퀴즈 생성 내용 입력 버튼 활성화")
@allure.title("[FHC-055] 퀴즈 생성 내용 입력 → [자동 생성] 버튼 활성화 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_055_fill_fields_and_btn_enabled(quiz):
    """
    [FHC-055] 퀴즈 생성 내용 입력 → [자동 생성] 버튼 활성화 확인

    전제: test_FHC_054 이어서 퀴즈 생성 페이지 상태
    단계:
      1. 문제 유형 '객관식 (단일 선택)' 선택
      2. 난이도 '하' 선택
      3. 주제 '퀴즈' 입력
    기대:
      - 토큰 정상: [자동 생성] 버튼 활성화
      - 토큰 소진: 버튼 비활성화 (xfail)
    """
    logger.info("[FHC-055] 퀴즈 생성 내용 입력 → 버튼 활성화 확인 시작")
    quiz.select_option(QuizPage.OPTION_TYPE_DD, QuizPage.OPTION_TYPE_VALUE)
    quiz.select_option(QuizPage.DIFFICULTY_DD, QuizPage.DIFFICULTY_VALUE)
    quiz.enter_text(QuizPage.CONTENT_INPUT, QuizPage.CONTENT_VALUE)
    quiz.assert_generate_btn_enabled()
    logger.info("[FHC-055] 퀴즈 생성 내용 입력 → 버튼 활성화 확인 완료")


@allure.story("퀴즈 생성 완료 확인")
@allure.title("[FHC-056] 퀴즈 생성 버튼 클릭 → 생성 시작 및 완료 확인")
@allure.severity(allure.severity_level.NORMAL)
def test_FHC_056_generate_quiz(quiz):
    """
    [FHC-056] 퀴즈 생성 버튼 클릭 → 생성 시작 및 완료 확인

    전제: test_FHC_055 이어서 필수 항목 입력 완료 상태
    단계:
      1. [자동 생성] 버튼 클릭
      2. 로딩 스피너 확인
      3. 생성 완료 체크 아이콘 확인 (최대 2분)
    기대:
      - 토큰 소진: xfail
      - 토큰 정상: 2분 이내 퀴즈 생성 완료
    """
    logger.info("[FHC-056] 퀴즈 생성 버튼 클릭 → 생성 완료 확인 시작")
    quiz.click_generate()
    assert quiz.is_generating(), "생성이 시작되지 않았습니다"
    assert quiz.is_generated(timeout=120), "2분 이내 퀴즈 생성 실패"
    logger.info("[FHC-056] 퀴즈 생성 버튼 클릭 → 생성 완료 확인 완료")
