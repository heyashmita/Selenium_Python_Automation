
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
)

from utils.config_reader import ConfigReader
from utils.logger import get_logger


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, ConfigReader.get_explicit_wait())
        self.logger = get_logger(self.__class__.__name__)

    def open(self, url):
        self.logger.info(f"Navigating to URL: {url}")
        self.driver.get(url)

    def find(self, locator):
        return self.wait.until(
            EC.presence_of_element_located(locator),
            message=f"Element not found: {locator}",
        )

    def find_clickable(self, locator):
        return self.wait.until(
            EC.element_to_be_clickable(locator),
            message=f"Element not clickable: {locator}",
        )

    def find_visible(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator),
            message=f"Element not visible: {locator}",
        )

    def find_all(self, locator):
        return self.wait.until(
            EC.presence_of_all_elements_located(locator),
            message=f"Elements not found: {locator}",
        )

    def click(self, locator):
        try:
            self.find_clickable(locator).click()
        except ElementClickInterceptedException:
            self.logger.warning(f"Click intercepted on {locator}, retrying via JS click")
            element = self.find(locator)
            self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator, text, clear_first=True):
        element = self.find_visible(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find_visible(locator).text

    def is_displayed(self, locator, timeout_override=None):
        try:
            if timeout_override:
                WebDriverWait(self.driver, timeout_override).until(
                    EC.visibility_of_element_located(locator)
                )
            else:
                self.find_visible(locator)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def scroll_to(self, locator):
        element = self.find(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        return element

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url
