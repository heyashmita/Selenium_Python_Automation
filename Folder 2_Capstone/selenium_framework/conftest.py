
import os
import pytest

from utils.driver_factory import DriverFactory
from utils.screenshot_util import ScreenshotUtil
from utils.logger import get_logger

logger = get_logger("conftest")


@pytest.fixture(scope="function")
def driver():
    logger.info("Initializing WebDriver")
    drv = DriverFactory.get_driver()
    yield drv
    logger.info("Quitting WebDriver")
    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver", None)
        if driver_fixture is not None:
            screenshot_path = ScreenshotUtil.capture(driver_fixture, item.name)
            if screenshot_path and os.path.exists(screenshot_path):
                _attach_screenshot_to_html_report(item, screenshot_path)
                logger.error(f"Test '{item.name}' failed. Screenshot saved: {screenshot_path}")


def _attach_screenshot_to_html_report(item, screenshot_path):
    try:
        import base64
        from pytest_html import extras

        with open(screenshot_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("utf-8")

        if "pytest_html" not in item.config.pluginmanager.list_name_plugin():
            return

        extra = getattr(item, "extra", [])
        extra.append(extras.image(encoded, mime_type="image/png"))
        extra.append(extras.url(screenshot_path))
        item.extra = extra
    except Exception as e:
        logger.warning(f"Could not attach screenshot to HTML report: {e}")


def pytest_configure(config):
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports", "html")
    os.makedirs(reports_dir, exist_ok=True)
