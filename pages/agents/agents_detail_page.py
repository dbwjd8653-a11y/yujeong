# pages/agents/agents_detail_page.py
# 에이전트 상세 페이지 및 대화 페이지 Page Object
# FHC-059, FHC-060 에서 사용

from config.selenium_imports import By, EC, WebDriverWait

from pages.base_page import BasePage


class AgentDetailPage(BasePage):

    # ========== Locators ==========

    # 에이전트 상세 페이지 — 주요 기능 버튼 (퀵 리플라이)
    # 추천 프롬프트 버튼만 정확히 잡는다: 텍스트(MuiTypography-body2 span)를 담은
    # type=button 중 로고(img)·아이콘/전송(svg) 버튼은 제외.
    # (브랜드 로고 'AI Helpy Chat' 버튼을 잘못 클릭하던 문제 방지)
    QUICK_REPLY_BUTTONS = (
        By.XPATH,
        "//button[@type='button'"
        " and not(ancestor::header)"
        " and not(.//img) and not(.//svg)"
        " and .//span[contains(@class,'MuiTypography-body2')]]",
    )

    # 채팅 입력창
    CHAT_INPUT = (
        By.CSS_SELECTOR,
        "textarea[name='input']",
    )

    # 전송 버튼 (화살표 아이콘 버튼 — submit)
    SEND_BUTTON = (
        By.XPATH,
        "//button[@type='submit' or contains(@aria-label,'전송') or contains(@aria-label,'send')]",
    )

    # AI 응답 완료 마커 — 답변 markdown 렌더가 끝나면 data-status='complete'
    # (data-with-artifact 컨테이너는 답변 시작 전에도 붙어 false-positive가 나므로 완료 상태로 검증)
    RESPONSE_COMPLETE = (
        By.CSS_SELECTOR,
        ".elice-aichat__markdown[data-status='complete']",
    )

    # LNB 내 대화 목록 항목 (chatrooms 경로를 가진 링크)
    LNB_CHATROOM_LINK = (
        By.XPATH,
        "//aside//a[contains(@href,'chatrooms')]",
    )

    # ========== 주요 기능 확인 (FHC-059) ==========

    def is_on_agent_detail(self, timeout: int = 15) -> bool:
        """에이전트 상세 페이지로 진입했는지 확인.
        상세 URL은 '.../agents/<id>' 형태(목록은 '.../agents' 로 끝남)이며,
        '심층 조사' 같은 특수 에이전트는 일반 채팅 UI(입력창)가 없으므로
        UI 요소 대신 URL 진입 여부로 안정적으로 검증한다.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: "/agents/" in d.current_url
                and d.current_url.rstrip("/").split("/agents/")[-1] != ""
            )
            self.logger.info(f"에이전트 상세 페이지 진입 확인: {self.driver.current_url}")
            return True
        except Exception:
            self.logger.warning("에이전트 상세 페이지 진입 실패")
            return False

    # ========== 대화 — 버튼 클릭 방식 (FHC-060) ==========

    def click_quick_reply(self, index: int = 0):
        """퀵 리플라이 프롬프트 버튼 클릭으로 대화 시작
        index: 0 = 첫 번째 버튼 (기본값)

        추천 프롬프트(한글 텍스트) 버튼이 렌더될 때까지 대기한 뒤 클릭한다.
        렌더 전 브랜드/로고 버튼을 잘못 클릭하던 레이스를 막고,
        프롬프트가 끝내 없으면(미제공) 명확한 메시지로 실패시킨다.
        """
        def _korean_prompt_buttons(driver):
            btns = driver.find_elements(*self.QUICK_REPLY_BUTTONS)
            korean = [b for b in btns if any('가' <= c <= '힣' for c in b.text)]
            return korean or False

        korean_buttons = self.wait.until(
            _korean_prompt_buttons,
            message="퀵 리플라이 프롬프트 버튼(한글)이 렌더되지 않음",
        )
        btn = korean_buttons[index]
        btn_text = btn.text.strip()
        self.js_click(btn)
        self.logger.info(f"퀵 리플라이 버튼 클릭: '{btn_text}'")
        return btn_text

    # ========== AI 응답 대기 (FHC-060) ==========

    def wait_for_ai_response(self, timeout: int = 60) -> bool:
        """AI 응답이 '완료'될 때까지 대기
        1) 대화방 URL(chatrooms) 전환 확인
        2) 응답 markdown이 data-status='complete' 가 될 때까지 대기 (스트리밍 종료)
        """
        try:
            # 대화방 URL로 전환 대기
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains("chatrooms")
            )
            self.logger.info("대화방 URL 전환 확인")

            # 응답 완료(스트리밍 종료) 대기
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.RESPONSE_COMPLETE)
            )
            self.logger.info("AI 응답 완료 확인 (data-status='complete')")
            return True
        except Exception:
            self.logger.warning("AI 응답 완료 대기 타임아웃")
            return False

    # ========== LNB 대화 목록 확인 (FHC-060) ==========

    def is_lnb_chatroom_visible(self, timeout: int = 15) -> bool:
        """LNB 사이드바에 대화 목록이 생겼는지 확인"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.LNB_CHATROOM_LINK)
            )
            count = len(self.driver.find_elements(*self.LNB_CHATROOM_LINK))
            self.logger.info(f"LNB 대화 목록 확인 ({count}개)")
            return True
        except Exception:
            self.logger.warning("LNB 대화 목록 미표시")
            return False
