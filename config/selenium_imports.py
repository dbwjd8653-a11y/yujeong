# config/selenium_imports.py
# 프로젝트 내 Selenium 공통 import 단일 지점

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
    StaleElementReferenceException,
)

__all__ = [
    "By",
    "WebDriverWait",
    "EC",
    "TimeoutException",
    "NoSuchElementException",
    "ElementNotInteractableException",
    "StaleElementReferenceException",
]
