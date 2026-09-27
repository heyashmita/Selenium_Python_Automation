
import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_factory import DriverFactory
from utils.csv_reader import CSVReader
from utils.screenshot_util import ScreenshotUtil
from utils.logger import get_logger
from pages.login_page import LoginPage

logger = get_logger("test_login_unittest")


class TestLoginUnittest(unittest.TestCase):

    def setUp(self):
        logger.info(f"---- Starting test: {self._testMethodName} ----")
        self.driver = DriverFactory.get_driver()
        self.login_page = LoginPage(self.driver)

    def tearDown(self):
        
        logger.info(f"---- Finished test: {self._testMethodName} ----")
        self.driver.quit()

    def _assert_true(self, condition, message):
        
        if not condition:
            ScreenshotUtil.capture(self.driver, self._testMethodName)
            logger.error(f"Test FAILED: {self._testMethodName} (screenshot captured)")
        self.assertTrue(condition, message)

    def _assert_is_not_none(self, value, message):
        
        if value is None:
            ScreenshotUtil.capture(self.driver, self._testMethodName)
            logger.error(f"Test FAILED: {self._testMethodName} (screenshot captured)")
        self.assertIsNotNone(value, message)

    def test_login_page_loads_successfully(self):
        
        self.login_page.load()
        self._assert_true(
            self.login_page.is_login_form_displayed(),
            "Login form did not display on the /login page",
        )

    def test_login_with_invalid_credentials_shows_error(self):
        
        self.login_page.load()
        self.login_page.login("invalid_user_never_registered@example.com", "WrongPassword!1")
        error_text = self.login_page.get_login_error_text()
        self._assert_is_not_none(
            error_text,
            "Expected an error message for invalid login, but none was shown",
        )
        self.assertIn("incorrect", error_text.lower())

    def test_login_data_driven_from_csv(self):
        
        rows = CSVReader.read("login_data.csv")
        failure_rows = [r for r in rows if r["expected_result"] == "failure"]

        for row in failure_rows:
            with self.subTest(email=row["email"]):
                self.login_page.load()
                self.login_page.login(row["email"], row["password"])
                error_text = self.login_page.get_login_error_text()
                if error_text is None:
                    ScreenshotUtil.capture(
                        self.driver, f"{self._testMethodName}_{row['email']}"
                    )
                    logger.error(
                        f"Test FAILED: {self._testMethodName} "
                        f"(email={row['email']}, screenshot captured)"
                    )
                self.assertIsNotNone(
                    error_text,
                    f"Expected login failure for {row['email']} but no error was shown",
                )


if __name__ == "__main__":
    unittest.main()