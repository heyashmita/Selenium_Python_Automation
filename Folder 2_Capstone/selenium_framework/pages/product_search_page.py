
from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config_reader import ConfigReader


class ProductSearchPage(BasePage):

    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BUTTON = (By.ID, "submit_search")
    SEARCHED_PRODUCTS_TITLE = (By.XPATH, "//h2[@class='title text-center']")
    PRODUCT_CARDS = (By.CSS_SELECTOR, ".product-image-wrapper")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".productinfo p")
    NO_PRODUCTS_MESSAGE = (By.XPATH, "//*[contains(text(),'No products') or contains(text(),'no products')]")

    URL = ConfigReader.get_base_url() + "/products"

    def load(self):
        self.open(self.URL)
        return self

    def search_product(self, product_name):
        self.type_text(self.SEARCH_INPUT, product_name)
        self.click(self.SEARCH_BUTTON)

    def is_search_results_header_displayed(self):
        return self.is_displayed(self.SEARCHED_PRODUCTS_TITLE, timeout_override=10)

    def get_result_count(self):
        try:
            cards = self.find_all(self.PRODUCT_CARDS)
            return len(cards)
        except Exception:
            return 0

    def get_product_names(self):
        try:
            elements = self.find_all(self.PRODUCT_NAMES)
            return [el.text.strip() for el in elements]
        except Exception:
            return []

    def all_results_contain(self, keyword):
        
        names = self.get_product_names()
        if not names:
            return False
        keyword_lower = keyword.lower()
        return all(keyword_lower in name.lower() for name in names)
