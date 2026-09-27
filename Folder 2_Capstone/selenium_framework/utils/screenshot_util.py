
import os
import time

from utils.config_reader import ConfigReader, PROJECT_ROOT


class ScreenshotUtil:

    @staticmethod
    def _screenshot_dir():
        directory = os.path.join(PROJECT_ROOT, ConfigReader.get_path("screenshot_dir"))
        os.makedirs(directory, exist_ok=True)
        return directory

    @staticmethod
    def capture(driver, test_name):
        if driver is None:
            return None
        try:
            safe_name = "".join(
                c if c.isalnum() or c in ("_", "-") else "_" for c in test_name
            )
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            file_name = f"{safe_name}_{timestamp}.png"
            file_path = os.path.join(ScreenshotUtil._screenshot_dir(), file_name)
            driver.save_screenshot(file_path)
            return file_path
        except Exception as e:
            print(f"[ScreenshotUtil] Failed to capture screenshot: {e}")
            return None
