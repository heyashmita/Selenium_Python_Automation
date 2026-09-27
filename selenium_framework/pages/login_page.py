
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config_reader import ConfigReader


class LoginPage(BasePage):


    SIGNUP_LOGIN_LINK = (By.CSS_SELECTOR, "a[href='/login']")
    LOGIN_EMAIL_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    LOGIN_PASSWORD_INPUT = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[data-qa='login-button']")
    LOGIN_ERROR_MESSAGE = (By.XPATH, "//p[contains(text(),'incorrect')]")
    LOGGED_IN_AS_TEXT = (By.XPATH, "//a[contains(text(),'Logged in as')]")
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href='/logout']")
    LOGIN_FORM_TITLE = (By.XPATH, "//div[@class='login-form']//h2")

    URL = ConfigReader.get_base_url() + "/login"

    def load(self):
        self.open(self.URL)
        return self

    def navigate_via_header(self):
        
        self.open(ConfigReader.get_base_url())
        self.click(self.SIGNUP_LOGIN_LINK)
        return self

    def is_login_form_displayed(self):
        return self.is_displayed(self.LOGIN_FORM_TITLE)

    def login(self, email, password):
        self.type_text(self.LOGIN_EMAIL_INPUT, email)
        self.type_text(self.LOGIN_PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def is_login_successful(self):
        return self.is_displayed(self.LOGGED_IN_AS_TEXT, timeout_override=10)

    def get_login_error_text(self):
        if self.is_displayed(self.LOGIN_ERROR_MESSAGE, timeout_override=10):
            return self.get_text(self.LOGIN_ERROR_MESSAGE)
        return None

    def logout(self):
        self.click(self.LOGOUT_LINK)
