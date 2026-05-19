"""
퀴즈 생성 도구 UI 시나리오 테스트
scope="module" 로 브라우저 하나로 test_01 ~ test_03 순서대로 실행합니다.
"""

import pytest
import logging
from pages.tools_05_page import Tool5Page

logger = logging.getLogger(__name__)

# ── fixtures ──────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def tools_ready(login_module):
    """
    [퀴즈 생성 도구 fixture - 모듈 전체 공유]

    [Pre-condition]
    - login_module fixture로 로그인이 완료된 상태

    [Test Steps]
    1. 햄버거 메뉴를 클릭하여 도구 목록으로 이동한다.
    2. '퀴즈 생성' 도구를 선택하고 초기 상태를 세팅한다.

    [Note]
    scope="module" 이므로 이후 test_02, test_03은 같은 브라우저에서 이어서 실행됩니다.
    """
    quiz = Tool5Page(login_module)
    quiz.tools_LNB()
    quiz.setup_tool()
    return quiz


# ── 테스트 케이스 ──────────────────────────────────────────────────

def test_tool_01_menu_access(tools_ready):
    """
    [FHC-054] 퀴즈 생성 페이지 진입 확인

    [목적] LNB를 통해 '퀴즈 생성' 도구로 정상 진입하는지 검증한다.

    [Pre-condition]
    - 로그인 완료 상태
    - 도구 목록 페이지에 접속한 상태

    [Test Steps]
    1. 도구 목록에서 '퀴즈 생성' 카드를 클릭한다.

    [Expected Result]
    퀴즈 생성 페이지 타이틀이 화면에 표시된다.
    """
    logger.info("[FHC-054] 퀴즈 생성 페이지 진입 확인 시작")
    tools_ready.is_tool_page_displayed()
    logger.info("[FHC-054] 퀴즈 생성 페이지 진입 확인 완료")


def test_tool_02_input_and_btn_enabled(tools_ready):
    """
    [FHC-055] 퀴즈 생성 내용 입력 → 생성 버튼 활성화 확인

    [목적] 필수 입력 항목을 모두 입력했을 때 생성 버튼이 활성화되는지 검증한다.

    [Pre-condition]
    - test_01 이어서 퀴즈 생성 페이지에 있는 상태

    [Test Steps]
    """
    logger.info("[FHC-055] 퀴즈 생성 내용 입력 → 생성 버튼 활성화 확인 시작")
    # 1. 문제 유형을 '객관식 (단일 선택)'으로 선택한다.
    tools_ready.select_option(Tool5Page.OPTION_TYPE_DD, Tool5Page.OPTION_TYPE_VALUE)
    # 2. 난이도를 '하'로 선택한다.
    tools_ready.select_option(Tool5Page.DIFFICULTY_DD, Tool5Page.DIFFICULTY_VALUE)
    # 3. 주제 입력 필드에 '퀴즈'를 입력한다.
    tools_ready.enter_text(Tool5Page.CONTENT_INPUT, Tool5Page.CONTENT_VALUE)
    # [Expected Result]
    # - 토큰 정상: 자동 생성 버튼이 활성화된다.
    # - 토큰 소진: 버튼이 비활성화 상태임을 확인하고 xfail 처리한다.
    tools_ready.assert_generate_btn_enabled()
    logger.info("[FHC-055] 퀴즈 생성 내용 입력 → 생성 버튼 활성화 확인 완료")


def test_tool_03_generate(tools_ready):
    """
    [FHC-056] 퀴즈 생성 버튼 클릭 → 생성 시작 및 완료 확인

    [목적] 생성 버튼 클릭 후 AI가 퀴즈를 정상적으로 생성하는지 검증한다.

    [Pre-condition]
    - test_02 이어서 필수 항목이 모두 입력된 상태

    [Test Steps]
    """
    logger.info("[FHC-056] 퀴즈 생성 버튼 클릭 → 생성 시작 및 완료 확인 시작")
    # [Expected Result]
    # - 토큰 소진: xfail 처리한다.
    # - 토큰 정상: 2분 이내에 퀴즈가 생성 완료된다.
    if tools_ready.is_token_exhausted():
        pytest.xfail("토큰 한도 소진으로 생성 불가")
    # 1. 자동 생성(또는 다시 생성) 버튼을 클릭한다.
    tools_ready.click_generate()
    # 2. 로딩 스피너가 나타나는지 확인한다.
    assert tools_ready.is_generating(), "생성이 시작되지 않았습니다"
    # 3. 스피너가 사라지고 완료 체크 아이콘이 나타날 때까지 대기한다.
    assert tools_ready.is_generated(timeout=120), "2분 이내 퀴즈 생성 실패"
    logger.info("[FHC-056] 퀴즈 생성 버튼 클릭 → 생성 시작 및 완료 확인 완료")
