from playwright.sync_api import Page, Locator, expect
from utils.logger import get_logger

class BasePage:
    def __init__(self, page: Page):
        self._page = page
        self._logger = get_logger(type(self).__name__)

    def __get_name(self, locator: Locator, name: str = None):
        """Returns the custom name if provided, else the locator string."""
        return name if name else str(locator)

    def navigate_to(self, url: str):
        self._logger.info(f"Navigating to: {url}")
        self._page.goto(url)

    def do_click(self, locator: Locator, name: str = None):
        element_log_name = self.__get_name(locator, name)
        self._logger.info(f"Clicking: '{element_log_name}' element")
        locator.click()

    def do_fill(self, locator: Locator, text: str, name: str = None):
        element_log_name = self.__get_name(locator, name)
        self._logger.info(f"Filling '{text}' into: '{element_log_name}' element")
        locator.fill(text)

    def do_press_sequentially(self, locator: Locator, text: str, delay: int = 0, name: str = None, is_secret = False):
        element_log_name = self.__get_name(locator, name)
        text_to_log = "*" * len(text) if is_secret else text
        self._logger.info(f"Typing '{text_to_log}' into: '{element_log_name}' element")
        locator.press_sequentially(text, delay=delay)

    def verify_text_element(self, locator: Locator, expected_text: str, name: str = None):
        element_log_name = self.__get_name(locator, name)
        self._logger.info(f"Verifying '{element_log_name}' element contains text: '{expected_text}'")
        try:
            expect(locator).to_contain_text(expected_text)
        except Exception as e:
            self._logger.error(f"Text verification failed for '{element_log_name}'. Error: {e}")
            raise e

    def verify_element_is_visible(self, locator: Locator, name: str = None):
        element_log_name = self.__get_name(locator, name)
        self._logger.info(f"Verifying '{element_log_name}' element is visible")
        try:
            expect(locator).to_be_visible()
        except Exception as e:
            self._logger.error(f"Visibility verification failed for '{element_log_name}'. Error: {e}")
            raise e

    def verify_url(self, url: str):
        self._logger.info(f"Verifying page URL is: {url}")
        try:
            expect(self._page).to_have_url(url)
        except Exception as e:
            self._logger.error(f"URL verification failed! Expected '{url}'. Error: {e}")
            raise e
