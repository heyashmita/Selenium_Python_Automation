
import time

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config_reader import ConfigReader


class HomePage(BasePage):

    PRODUCTS_NAV_LINK = (By.CSS_SELECTOR, "a[href='/products']")
    LOGGED_IN_AS_TEXT = (By.XPATH, "//a[contains(text(),'Logged in as')]")
    HOME_LOGO = (By.CSS_SELECTOR, "img[alt='Website for automation practice']")

    URL = ConfigReader.get_base_url()

    def load(self):
        self.open(self.URL)
        return self

    def is_loaded(self):
        return self.is_displayed(self.HOME_LOGO)

    def is_user_logged_in(self):
        return self.is_displayed(self.LOGGED_IN_AS_TEXT, timeout_override=10)

    def go_to_products_page(self, max_retries=2):
        
        for attempt in range(max_retries):
            self.click(self.PRODUCTS_NAV_LINK)
            time.sleep(1.5)  # give the ad script a moment to intercept, if it will
            current_url = self.get_current_url()

            if "/products" in current_url and "google_vignette" not in current_url:
                return  # real navigation succeeded

            self.logger.warning(
                f"Navigation to /products was intercepted (url={current_url}); "
                f"retry {attempt + 1}/{max_retries}"
            )
            self.open(self.URL)  # reset back to home and try again

        self.logger.warning(
            "Click-based navigation to /products kept getting intercepted by an "
            "ad overlay; falling back to direct URL navigation."
        )
        self.open(ConfigReader.get_base_url() + "/products")