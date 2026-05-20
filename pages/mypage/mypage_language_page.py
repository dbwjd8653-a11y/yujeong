# pages/mypage/mypage_language_page.py
# 마이페이지 > 언어 설정 전용 Page 클래스
# FHC-086(언어 변경) / FHC-087(로그아웃 후 언어 확인) / FHC-088(재로그인 후 언어 유지)

import time

from config.selenium_imports import By, EC, WebDriverWait

from pages.mypage.mypage_page import MyPage


class MyPage08(MyPage):

    # ========== FHC-086: 언어 설정 ==========

    def is_language_setting_displayed(self) -> bool:
        try:
            self.wait.until(EC.presence_of_element_located(self.LANGUAGE_SELECT))
            return True
        except Exception:
            return False

    # ========== FHC-087/088 공통: 로그아웃 ==========

    def logout_via_profile_menu(self):
        """accounts.elice.io 우상단 아바타 클릭 → 로그아웃 메뉴 클릭"""
        # accounts.elice.io로 이동 (헤더에 아바타 버튼 있음)
        self.driver.get(self.ACCOUNT_URL)
        self.wait.until(EC.url_contains("members"))
        time.sleep(1)

        # header 안의 MuiAvatar 버튼 클릭 (Selenium 네이티브 click)
        avatar_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "header button.MuiAvatar-root")
            )
        )
        avatar_btn.click()
        print("accounts.elice.io 아바타 버튼 클릭 완료")
        time.sleep(0.8)  # MUI 드롭다운 렌더링 대기

        # 로그아웃 menuitem 클릭 (normalize-space로 중첩 텍스트 포함)
        logout_item = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                "//li[@role='menuitem' and ("
                "contains(normalize-space(.),'로그아웃')"
                " or contains(normalize-space(.),'Logout')"
                " or contains(normalize-space(.),'Log out')"
                " or contains(normalize-space(.),'Sign out')"
                ")]"
            ))
        )
        before_url = self.driver.current_url
        logout_item.click()
        print("로그아웃 메뉴 클릭 완료")
        time.sleep(1.5)  # 리다이렉트 완료 대기

        # URL이 members 페이지를 벗어나거나 signin/login 포함 시 완료
        WebDriverWait(self.driver, 10).until(
            lambda d: (
                d.current_url != before_url
                and "members" not in d.current_url
            )
        )
        print(f"로그아웃 완료 -> {self.driver.current_url}")

    # ========== FHC-087: 로그인 페이지 언어 확인 ==========

    def is_login_page_in_english(self) -> bool:
        """현재 로그인 페이지가 영어로 표시되는지 확인"""
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: len(d.find_element(By.TAG_NAME, "body").text.strip()) > 10
            )
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            return any(kw in body_text for kw in ["Email", "Sign in", "Password", "Sign In", "Log in"])
        except Exception:
            return False

    # ========== FHC-088: 재로그인 후 언어 유지 확인 ==========

    def is_language_maintained(self, expected_lang: str = "en-US") -> bool:
        """재로그인 후 언어 설정이 유지되는지 언어 설정 페이지에서 확인"""
        self.navigate_to_language()
        try:
            select_el = self.wait.until(EC.presence_of_element_located(self.LANGUAGE_SELECT))
            select_text = select_el.text.strip()
            if expected_lang == "en-US":
                return "English" in select_text
            elif expected_lang == "ko-KR":
                return "한국어" in select_text
            return False
        except Exception:
            return False

