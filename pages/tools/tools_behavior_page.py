# pages/tools/tools_behavior_page.py
# '행동특성 및 종합의견' 도구 전용 Page 클래스
# BaseToolPage에 없는 인성·태도 키워드 선택 로직을 담당

import time

from config.selenium_imports import By, EC


from pages.tools.base_tool_page import BaseToolPage


class BehaviorPage(BaseToolPage):

    TOOL_NAME = "행동특성 및 종합의견"

    # ========== Locators ==========

    # 키워드 모달 — 인성·태도 아코디언
    CHARACTER_ACCORDION = (
        By.XPATH,
        "//div[contains(@class,'MuiAccordionSummary-root') and (contains(.,'인성') or contains(.,'Character'))]",
    )
    # 예의 바르고 배려심 있음 칩
    COURTESY_CHIP = (
        By.XPATH,
        "//div[contains(@class,'MuiChip-outlined') and "
        "(contains(.,'예의 바르고 배려심 있음') or contains(.,'Polite') or contains(.,'Considerate'))]",
    )

    # ========== 키워드 선택 — 인성·태도 ==========

    def select_character_keyword(self):
        """인성·태도(품성·책임감) 아코디언 → 예의 바르고 배려심 있음 칩 선택"""
        accordion = self.wait.until(EC.element_to_be_clickable(self.CHARACTER_ACCORDION))
        self.js_click(accordion)
        self.logger.info("인성·태도(품성·책임감) 아코디언 펼치기 완료")

        chip = self.wait.until(EC.element_to_be_clickable(self.COURTESY_CHIP))
        self.js_click(chip)
        self.logger.info("예의 바르고 배려심 있음 선택 완료")
