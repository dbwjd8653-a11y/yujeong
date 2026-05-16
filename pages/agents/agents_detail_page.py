# pages/agents/agent_detail_page.py
# 에이전트 상세 페이지 및 대화 페이지 Page Object
# FHC-059, FHC-060 에서 사용

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class AgentDetailPage(BasePage):

    # ========== Locators ==========

    # 에이전트 상세 페이지 — 주요 기능 버튼 (퀵 리플라이)
    # main 영역 안의 텍스트가 있는 버튼들 (헤더·전송 버튼 제외)
    QUICK_REPLY_BUTTONS = (
        By.XPATH,
        "//main//button[contains(@class,'MuiButtonBase-root')"
        " and @type='button'"
        " and string-length(normalize-space(.)) > 0]",
    )

    # 채팅 입력창
    CHAT_INPUT = (
        By.CSS_SELECTOR,
        "textarea[placeholder='메시지를 입력해 주세요.']",
    )

    # 전송 버튼 (화살표 아이콘 버튼 — submit)
    SEND_BUTTON = (
        By.XPATH,
        "//button[@type='submit' or contains(@aria-label,'전송') or contains(@aria-label,'send')]",
    )

    # AI 응답 컨테이너 (data-with-artifact 속성이 붙으면 응답 완료)
    RESPONSE_CONTENT = (
        By.XPATH,
        "//div[@data-with-artifact]",
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
            print(f"주요 기능 버튼 확인: {names}")
            return len(names) > 0
        except Exception:
            return False

    # ========== 대화 — 버튼 클릭 방식 (FHC-060) ==========

    def click_quick_reply(self, index: int = 0):
        """퀵 리플라이 버튼 클릭으로 대화 시작
        index: 0 = 첫 번째 버튼 (기본값)
        """
        buttons = self.get_quick_reply_buttons()
        btn = buttons[index]
        btn_text = btn.text.strip()
        self.js_click(btn)
        print(f"퀵 리플라이 버튼 클릭: '{btn_text}'")
        return btn_text

    # ========== 대화 — 직접 입력 방식 (FHC-060) ==========

    def send_text_message(self, message: str):
        """채팅창에 텍스트 직접 입력 후 전송 (Enter 키)"""
        chat_input = self.wait.until(
            EC.visibility_of_element_located(self.CHAT_INPUT)
        )
        self.js_input(chat_input, message)
        time.sleep(0.3)

        # 전송 버튼 클릭 시도 → 실패하면 Enter 키
        try:
            send_btn = self.driver.find_element(*self.SEND_BUTTON)
            self.js_click(send_btn)
            print(f"전송 버튼 클릭 (메시지: '{message}')")
        except Exception:
            chat_input.send_keys(Keys.RETURN)
            print(f"Enter 키로 전송 (메시지: '{message}')")

    # ========== AI 응답 대기 (FHC-060) ==========

    def wait_for_ai_response(self, timeout: int = 60) -> bool:
        """AI 응답이 생성될 때까지 대기
        1) URL에 chatrooms 포함 확인
        2) 응답 컨테이너(data-with-artifact) 나타날 때까지 대기
        """
        try:
            # 대화방 URL로 전환 대기
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains("chatrooms")
            )
            print("대화방 URL 전환 확인")

            # 응답 컨텐츠 등장 대기
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.RESPONSE_CONTENT)
            )
            print("AI 응답 생성 확인")
            return True
        except Exception:
            print("AI 응답 대기 타임아웃")
            return False

    # ========== LNB 대화 목록 확인 (FHC-060) ==========

    def is_lnb_chatroom_visible(self, timeout: int = 15) -> bool:
        """LNB 사이드바에 대화 목록이 생겼는지 확인"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.LNB_CHATROOM_LINK)
            )
            count = len(self.driver.find_elements(*self.LNB_CHATROOM_LINK))
            print(f"LNB 대화 목록 확인 ({count}개)")
            return True
        except Exception:
            print("LNB 대화 목록 미표시")
            return False
