# pages/agents/agents_page.py
# '에이전트 탐색' 목록 페이지 Page Object
# FHC-058, FHC-059 에서 사용

import random

from config.selenium_imports import By, EC, WebDriverWait
from config.settings import BASE_URL

from pages.base_page import BasePage


class AgentsPage(BasePage):

    AGENTS_URL = BASE_URL + "/agents"

    # ========== Locators ==========

    # LNB의 '에이전트 마켓플레이스' 메뉴 링크
    # (2026-06-15 서버 개편으로 '에이전트 탐색' → '에이전트 마켓플레이스'로 통합·개명.
    #  탭 이름 변경에 영향받지 않도록 href 기반으로 매칭 — tools의 LNB_TOOLS_LINK와 동일 방식)
    LNB_AGENTS_LINK = (
        By.XPATH,
        "//a[contains(@href,'ai-helpy-chat/agents')"
        " and not(contains(@href,'ai-helpy-chat/agents/'))]",
    )

    # 에이전트 목록 컨테이너 (virtuoso 스크롤러)
    AGENT_GRID = (
        By.CSS_SELECTOR,
        "div[data-testid='virtuoso-scroller']",
    )

    # 개별 에이전트 카드 (클릭 가능한 <a> 태그)
    AGENT_CARDS = (
        By.XPATH,
        "//div[contains(@class,'virtuoso-grid-item')]//a",
    )

    # 에이전트 검색창 (virtuoso 가상 그리드를 스크롤하지 않고 특정 에이전트로 필터)
    AGENT_SEARCH_INPUT = (
        By.CSS_SELECTOR,
        "input[placeholder='AI 에이전트 검색']",
    )

    # ========== 페이지 이동 ==========

    def open(self):
        """에이전트 탐색 페이지 직접 이동 (로그인 이후 사용)"""
        self.driver.get(self.AGENTS_URL)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def navigate_to_base(self):
        """메인 채팅 페이지로 이동 후 페이지 로드 대기 (LNB 탭 클릭 테스트 전제 조건)"""
        from config.settings import BASE_URL
        from config.login_helpers import close_token_banner
        self.driver.get(BASE_URL)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        close_token_banner(self.driver, self.wait)

    # ========== LNB 탭 클릭 ==========

    def click_agents_tab_from_lnb(self):
        """LNB의 '에이전트 탐색' 메뉴를 클릭해 페이지 이동"""
        link = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.LNB_AGENTS_LINK))
        self.js_click(link)
        WebDriverWait(self.driver, 20).until(EC.url_contains("/agents"))
        self.logger.info("LNB '에이전트 마켓플레이스' 탭 클릭 완료")

    # ========== 목록 확인 ==========

    def is_agent_list_displayed(self) -> bool:
        """에이전트 목록(virtuoso 그리드)이 화면에 표시되는지 확인"""
        try:
            self.wait.until(EC.presence_of_element_located(self.AGENT_GRID))
            cards = WebDriverWait(self.driver, 15).until(
                EC.presence_of_all_elements_located(self.AGENT_CARDS)
            )
            self.logger.info(f"에이전트 목록 표시 확인 (카드 {len(cards)}개)")
            return len(cards) > 0
        except Exception:
            return False

    # ========== 에이전트 클릭 ==========

    def click_random_agent(self) -> str:
        """목록에서 랜덤 에이전트 카드 클릭, 클릭한 에이전트 이름 반환"""
        cards = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located(self.AGENT_CARDS)
        )
        card = random.choice(cards)

        # 에이전트 이름 추출 (있으면)
        try:
            name = card.find_element(
                By.XPATH, ".//p[contains(@class,'MuiTypography-body1')]"
            ).text.strip()
        except Exception:
            name = "(이름 파악 불가)"

        self.js_click(card)
        self.wait.until(EC.url_contains("/agents/"))
        self.logger.info(f"에이전트 '{name}' 클릭 완료")
        return name

    def click_first_agent(self) -> str:
        """목록의 첫 번째 에이전트 카드 클릭 (재현성 필요한 경우 사용)"""
        cards = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located(self.AGENT_CARDS)
        )
        card = cards[0]
        try:
            name = card.find_element(
                By.XPATH, ".//p[contains(@class,'MuiTypography-body1')]"
            ).text.strip()
        except Exception:
            name = "(이름 파악 불가)"

        self.js_click(card)
        self.wait.until(EC.url_contains("/agents/"))
        self.logger.info(f"첫 번째 에이전트 '{name}' 클릭 완료")
        return name

    def click_agent_by_name(self, name: str) -> str:
        """검색창에 이름을 입력해 필터링한 뒤 해당 에이전트 카드를 클릭.
        virtuoso 가상 그리드는 스크롤해야 항목이 렌더되므로, 검색으로 대상만 남겨 안정적으로 클릭한다.
        """
        search = self.wait.until(EC.element_to_be_clickable(self.AGENT_SEARCH_INPUT))
        search.clear()
        search.send_keys(name)
        self.logger.info(f"에이전트 검색어 입력: '{name}'")

        card = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//div[contains(@class,'virtuoso-grid-item')]"
                f"//a[.//p[normalize-space(text())='{name}']]",
            ))
        )
        self.js_click(card)
        self.wait.until(EC.url_contains("/agents/"))
        self.logger.info(f"에이전트 '{name}' 클릭 완료")
        return name
