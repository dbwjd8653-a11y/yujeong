# pages/mypage/mypage_support_page.py
# 마이페이지 > 고객 센터 전용 Page 클래스
# FHC-089(고객 센터 AI)

import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.mypage.mypage_page import MyPage


class MyPage09(MyPage):

    # ========== Locators ==========
    START_CHAT_BUTTON = (By.CSS_SELECTOR,
        "a[data-ch-testid='new-chat-button'], button[data-ch-testid='new-chat-button']"
    )

    # ========== FHC-089: 고객 센터 AI ==========

    def click_start_chat(self):
        """ChannelTalk 위젯 내 'Start a chat' 버튼 클릭 (iframe 전환 포함)"""
        # 1) 메인 페이지에서 data-ch-testid 버튼 시도
        try:
            btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(self.START_CHAT_BUTTON)
            )
            self.js_click(btn)
            print("Start a chat 버튼 클릭 완료 (main frame)")
            return
        except Exception:
            pass

        # 2) ChannelTalk iframe 전환 후 버튼 찾기
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            try:
                src  = iframe.get_attribute("src")  or ""
                name = iframe.get_attribute("name") or ""
                if "channel" in src.lower() or "ch-plugin" in name.lower() or src == "":
                    self.driver.switch_to.frame(iframe)
                    try:
                        btn = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                "[data-ch-testid='new-chat-button'], "
                                "button[aria-label*='chat'], button[aria-label*='Chat']"
                            ))
                        )
                        self.js_click(btn)
                        self.driver.switch_to.default_content()
                        print("Start a chat 버튼 클릭 완료 (iframe)")
                        return
                    except Exception:
                        self.driver.switch_to.default_content()
            except Exception:
                self.driver.switch_to.default_content()

        # 3) JS ChannelIO API fallback
        result = self.driver.execute_script("""
            if (window.ChannelIO) {
                window.ChannelIO('openChat');
                return 'channelIO-api';
            }
            return 'not-found';
        """)
        if result == 'channelIO-api':
            time.sleep(1)
            print("Start a chat: ChannelIO API로 채팅 열기 완료")
        else:
            raise Exception("고객 센터 채팅 버튼을 찾을 수 없습니다")

    def is_chat_ai_displayed(self) -> bool:
        """AI 답변 또는 채팅창이 표시되는지 확인 (메인 페이지 + iframe 모두 검색)"""
        kws = ["안녕하세요", "Hello", "무엇을 도와", "How can I help",
               "Hi there", "chat", "Chat", "메시지"]
        # 1) 메인 페이지
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: any(kw in d.find_element(By.TAG_NAME, "body").text for kw in kws)
            )
            return True
        except Exception:
            pass
        # 2) iframe 내부
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        for iframe in iframes:
            try:
                self.driver.switch_to.frame(iframe)
                body_text = self.driver.find_element(By.TAG_NAME, "body").text
                if any(kw in body_text for kw in kws):
                    self.driver.switch_to.default_content()
                    return True
                self.driver.switch_to.default_content()
            except Exception:
                self.driver.switch_to.default_content()
        return False
