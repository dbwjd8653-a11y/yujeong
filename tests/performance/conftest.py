import pytest
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import DEFAULT_WAIT
from config.browser_factory import make_simple_firefox_driver
from config.login_helpers import do_login, close_token_banner


@pytest.fixture(scope="module")
def login_module():
    driver = make_simple_firefox_driver()
    wait = WebDriverWait(driver, DEFAULT_WAIT)
    do_login(driver, wait)
    close_token_banner(driver, wait)
    yield driver, wait
    driver.quit()
