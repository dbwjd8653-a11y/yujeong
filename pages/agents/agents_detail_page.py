# pages/agents/agents_detail_page.py
# 에이전트 상세 페이지 및 대화 페이지 Page Object
# FHC-059, FHC-060 에서 사용

from config.selenium_imports import By, EC, WebDriverWait

from pages.base_page import BasePage


class AgentDetailPage(BasePage):

    # ========== Locators ==========

    # 에이전트 상세 페이지 — 주요 기능 버튼 (퀵 리플라이)
    # main 영역 안의 텍스트가 있는 버튼들 (헤더·전송 버튼 제외)
    QUICK_REPLY_BUTTONS = (
        By.XPATH,
        "//button[@type='button'"
        " and string-length(normalize-space(.)) > 0"
        " and not(ancestor::header)"
        " and not(contains(@aria-label,'전송') or contains(@aria-label,'send') or contains(@aria-label,'Submit'))]",
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

    def get_quick_reply_buttons(self):
        """주요 기능 퀵 리플라이 버튼 목록 반환"""
        return self.wait.until(
            EC.presence_of_all_elements_located(self.QUICK_REPLY_BUTTONS)
        )

    def is_main_features_displayed(self) -> bool:
        """에이전트 주요 기능 버튼이 1개 이상 표시되는지 확인"""
        try:
            buttons = self.get_quick_reply_buttons()
            names = [b.text.strip() for b in buttons if b.text.strip()]
            self.logger.info(f"주요 기능 버튼 확인: {names}")
            return len(names) > 0
        except Exception:
            return False

    # ========== 대화 — 버튼 클릭 방식 (FHC-060) ==========

    def click_quick_reply(self, index: int = 0):
        """퀵 리플라이 버튼 클릭으로 대화 시작
        index: 0 = 첫 번째 버튼 (기본값)
        """
        buttons = self.get_quick_reply_buttons()
        # 한국어 텍스트가 포함된 버튼만 실제 퀵 리플라이로 간주
        korean_buttons = [b for b in buttons if any('가' <= c <= '힣' for c in b.text)]
        target_buttons = korean_buttons if korean_buttons else buttons
        btn = target_buttons[index]
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
