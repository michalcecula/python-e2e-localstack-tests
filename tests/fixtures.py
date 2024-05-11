import json
import pytest
import os
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from api.post_sign_in import sign_in
from pages.home_page import HomePage
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def chrome_browser():
    options = Options()
    options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    browser = Chrome(service=service, options=options)
    yield browser
    browser.quit()


@pytest.fixture
def logged_in_test(chrome_browser):
    chrome_browser.get(os.getenv("FRONTEND_URL"))
    login_response = sign_in(os.getenv("ADMIN_USERNAME"), os.getenv("ADMIN_PASSWORD"))
    token = login_response["token"]
    setup_user_local_storage(chrome_browser, login_response)
    chrome_browser.get(os.getenv("FRONTEND_URL"))
    return HomePage(chrome_browser), token


def setup_user_local_storage(browser, login_response):
    browser.execute_script(
        "window.localStorage.setItem(arguments[0], arguments[1])",
        "user",
        json.dumps(login_response),
    )
