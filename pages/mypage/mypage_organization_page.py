# pages/mypage/mypage_organization_page.py
# 마이페이지 > 내 기관 전용 Page 클래스
# FHC-081(UI 확인) / FHC-082(qaproject 링크) / FHC-083(헬프 센터 링크)

from config.selenium_imports import By, EC, WebDriverWait

from pages.mypage.mypage_page import MyPage


class MyPage07(MyPage):

    # ========== Locators ==========
    QAPROJECT_LINK = (By.XPATH,
        "//a[contains(@href,'qaproject.elice.io')]"
        " | //*[contains(text(),'qaproject.elice.io') or contains(text(),'qa 프로젝트')]"
        "/ancestor::a"
    )
    HELP_CENTER_LINK = (By.XPATH,
        "//a[contains(@href,'helpcenter.elice.io')]"
        " | //*[contains(text(),'헬프 센터') or contains(text(),'Help Center')]"
        "/ancestor::a[1]"
        " | //*[contains(text(),'헬프 센터')]/ancestor::*[@role='button'][1]"
    )

    # ========== FHC-081: 내 기관 UI 확인 ==========

    def is_org_info_displayed(self) -> bool:
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: len(d.find_element(By.TAG_NAME, "body").text.strip()) > 50
            )
            return True
        except Exception:
            return False

    # ========== FHC-082: qaproject 링크 ==========

    def click_qaproject_link(self):
        self.js_click(
            self.wait.until(EC.element_to_be_clickable(self.QAPROJECT_LINK))
        )
        self.logger.info("qaproject 링크 클릭 완료")

    # ========== FHC-083: 헬프 센터 링크 ==========

    def click_help_center_link(self):
        self.js_click(
            self.wait.until(EC.element_to_be_clickable(self.HELP_CENTER_LINK))
        )
        self.logger.info("헬프 센터 링크 클릭 완료")
