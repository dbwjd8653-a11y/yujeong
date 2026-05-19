# pages/chat_page.py
# 메인 채팅 / 검색 기능 Page Object
# FHC-020 / FHC-021 / FHC-022 / FHC-023 / FHC-024 / FHC-025

import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class ChatPage(BasePage):

    BASE_URL = "https://qaproject.elice.io/ai-helpy-chat"

    # ========== LNB Locators ==========

    # '새 대화' LNB 버튼 (anchor 태그, href="/ai-helpy-chat")
    LNB_NEW_CHAT = (
        By.XPATH,
        "//span[normalize-space(text())='새 대화']/ancestor::a",
    )

    # '검색' LNB 버튼 (div[role='button'])
    LNB_SEARCH = (
        By.XPATH,
        "//span[normalize-space(text())='검색']/ancestor::*[@role='button' or local-name()='a'][1]",
    )

    # LNB 기존 대화 목록 아이템 (chats 경로를 가진 링크)
    LNB_CHAT_ITEMS = (
        By.XPATH,
        "//a[contains(@href,'ai-helpy-chat/chats/')]",
    )

    # LNB 대화 아이템의 제목 텍스트
    LNB_CHAT_ITEM_TITLE = (
        By.XPATH,
        ".//p[contains(@class,'MuiTypography-inherit')]",
    )

    # ========== Chat Window Locators ==========

    # 채팅 에이전트 헤더 (Helpy Pro Agent)
    AGENT_HEADER = (
        By.XPATH,
        "//*[contains(text(),'Helpy Pro Agent')]",
    )

    # 메시지 입력 textarea
    CHAT_INPUT = (
        By.CSS_SELECTOR,
        "textarea[name='input'][placeholder='메시지를 입력해 주세요.']",
    )

    # 전송 버튼 (화살표)
    SEND_BUTTON = (
        By.XPATH,
        "//button[@type='submit' or contains(@aria-label,'전송') or contains(@aria-label,'send')]",
    )

    # '생각 중...' 로딩 텍스트 (AI 응답 생성 중 표시)
    THINKING_INDICATOR = (
        By.XPATH,
        "//*[contains(text(),'생각 중')]",
    )

    # AI 응답 완료 컨테이너 (data-with-artifact 속성)
    RESPONSE_CONTENT = (
        By.XPATH,
        "//div[@data-with-artifact]",
    )

    # ========== Search Modal Locators ==========

    # 검색 모달/다이얼로그
    SEARCH_MODAL = (
        By.XPATH,
        "//*[@role='dialog']",
    )

    # 검색 모달 내 텍스트 입력 필드
    SEARCH_MODAL_INPUT = (
        By.XPATH,
        "//*[@role='dialog']//input[@type='text' or @type='search' or not(@type)]",
    )

    # 검색 결과 아이템 텍스트 (span)
    SEARCH_RESULT_ITEMS = (
        By.XPATH,
        "//*[@role='dialog']//span[contains(@class,'MuiListItemText-primary')]",
    )

    # 검색 결과 클릭 가능 아이템 (버튼/링크)
    SEARCH_RESULT_CLICKABLE = (
        By.XPATH,
        "//*[@role='dialog']//*[@role='button' or local-name()='a']"
        "[.//span[contains(@class,'MuiListItemText-primary')]]",
    )

    # ========== 페이지 이동 ==========

    def open(self):
        """메인 채팅 페이지로 이동"""
        self.driver.get(self.BASE_URL)
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        print("메인 채팅 페이지 이동 완료")

    # ========== LNB 탭 클릭 ==========

    def click_new_chat_from_lnb(self):
        """LNB '새 대화' 탭 클릭"""
        link = self.wait.until(EC.element_to_be_clickable(self.LNB_NEW_CHAT))
        self.js_click(link)
        print("LNB '새 대화' 탭 클릭 완료")

    def click_search_from_lnb(self):
        """LNB '검색' 탭 클릭"""
        btn = self.wait.until(EC.element_to_be_clickable(self.LNB_SEARCH))
        self.js_click(btn)
        print("LNB '검색' 탭 클릭 완료")

    # ========== 채팅 창 상태 확인 ==========

    def is_chat_window_open(self) -> bool:
        """AI 대화창이 열렸는지 확인 (채팅 입력 필드 존재 여부)"""
        try:
            self.wait.until(EC.visibility_of_element_located(self.CHAT_INPUT))
            print("채팅 입력 필드 표시 확인")
            return True
        except Exception:
            return False

    def is_default_agent_helpy_pro(self) -> bool:
        """기본 에이전트가 Helpy Pro Agent인지 확인"""
        try:
            self.wait.until(EC.presence_of_element_located(self.AGENT_HEADER))
            print("Helpy Pro Agent 헤더 확인")
            return True
        except Exception:
            return False

    # ========== 메시지 전송 ==========

    def send_message(self, text: str):
        """메시지 입력 후 전송"""
        chat_input = self.wait.until(EC.visibility_of_element_located(self.CHAT_INPUT))
        self.js_input(chat_input, text)
        time.sleep(0.3)  # React 상태 반영 대기

        try:
            send_btn = self.driver.find_element(*self.SEND_BUTTON)
            if send_btn.is_enabled():
                self.js_click(send_btn)
                print(f"전송 버튼 클릭 (메시지: '{text}')")
                return
        except Exception:
            pass

        chat_input.send_keys(Keys.RETURN)
        print(f"Enter 키로 전송 (메시지: '{text}')")

    # ========== AI 응답 대기 ==========

    def wait_for_ai_response(self, timeout: int = 60) -> bool:
        """AI 응답이 완료될 때까지 대기
        1) URL에 /chats/ 포함 확인 (대화방 생성)
        2) 응답 컨테이너(data-with-artifact) 나타날 때까지 대기
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains("/ai-helpy-chat/chats/")
            )
            print("대화방 URL 전환 확인")

            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.RESPONSE_CONTENT)
            )
            print("AI 응답 생성 확인")
            return True
        except Exception:
            print("AI 응답 대기 타임아웃")
            return False

    # ========== LNB 대화 목록 ==========

    def is_lnb_chat_list_visible(self, timeout: int = 15) -> bool:
        """LNB에 기존 대화 목록이 표시되는지 확인"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.LNB_CHAT_ITEMS)
            )
            count = len(self.driver.find_elements(*self.LNB_CHAT_ITEMS))
            print(f"LNB 대화 목록 확인 ({count}개)")
            return count > 0
        except Exception:
            print("LNB 대화 목록 미표시")
            return False

    def click_random_lnb_chat(self) -> str:
        """LNB 기존 대화 목록에서 랜덤 아이템 클릭, 제목 반환"""
        items = self.wait.until(
            EC.presence_of_all_elements_located(self.LNB_CHAT_ITEMS)
        )
        idx = random.randint(0, len(items) - 1)
        try:
            title = items[idx].find_element(*self.LNB_CHAT_ITEM_TITLE).text.strip()
        except Exception:
            title = "(제목 파악 불가)"
        # stale element 방지: 클릭 직전 재탐색 (크기가 달라질 수 있으므로 modulo 처리)
        items = self.driver.find_elements(*self.LNB_CHAT_ITEMS)
        if not items:
            raise Exception("LNB 채팅 목록을 찾을 수 없습니다")
        self.js_click(items[idx % len(items)])
        print(f"LNB 대화 '{title}' 클릭 완료")
        return title

    # ========== 검색 모달 ==========

    def is_search_modal_open(self) -> bool:
        """검색 모달/다이얼로그가 열렸는지 확인"""
        try:
            self.wait.until(EC.presence_of_element_located(self.SEARCH_MODAL))
            print("검색 모달 열림 확인")
            return True
        except Exception:
            return False

    def enter_search_keyword(self, keyword: str):
        """검색 모달에 키워드 입력"""
        try:
            search_input = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.SEARCH_MODAL_INPUT)
            )
            search_input.clear()
            search_input.send_keys(keyword)
        except Exception:
            # 입력 필드가 없으면 모달 자체에 포커스 후 타이핑
            modal = self.driver.find_element(*self.SEARCH_MODAL)
            modal.click()
            modal.send_keys(keyword)
        time.sleep(0.5)  # 검색 결과 필터링 반영 대기
        print(f"검색 키워드 입력: '{keyword}'")

    def is_search_results_displayed(self) -> bool:
        """검색 결과 목록이 표시되는지 확인"""
        try:
            items = self.wait.until(
                EC.presence_of_all_elements_located(self.SEARCH_RESULT_ITEMS)
            )
            print(f"검색 결과 확인 ({len(items)}개)")
            return len(items) > 0
        except Exception:
            return False

    def click_random_search_result(self) -> str:
        """검색 결과에서 랜덤 아이템 클릭, 제목 반환"""
        items = self.wait.until(
            EC.presence_of_all_elements_located(self.SEARCH_RESULT_CLICKABLE)
        )
        item = random.choice(items)
        try:
            title = item.find_element(
                By.XPATH, ".//span[contains(@class,'MuiListItemText-primary')]"
            ).text.strip()
        except Exception:
            title = "(제목 파악 불가)"
        self.js_click(item)
        print(f"검색 결과 '{title}' 클릭 완료")
        return title

    # ========== 대화 상세 화면 확인 ==========

    def is_chat_detail_displayed(self, timeout: int = 10) -> bool:
        """대화 상세 화면으로 이동했는지 확인 (URL에 /chats/UUID 포함)"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains("/ai-helpy-chat/chats/")
            )
            print("대화 상세 화면 이동 확인")
            return True
        except Exception:
            return False
