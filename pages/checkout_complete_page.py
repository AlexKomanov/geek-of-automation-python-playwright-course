from playwright.sync_api import Page
from pages.base_page import BasePage

class CheckoutCompletePage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.__page_title = page.locator("[data-test='title']")
        self.__complete_header = page.locator("[data-test='complete-header']")
        self.__complete_text = page.locator("[data-test='complete-text']")
        self.__back_to_products_button = page.locator("[data-test='back-to-products']")

    def validate_page_title_text(self, page_title: str):
        self.verify_text_element(self.__page_title, page_title, "Page Title")

    def validate_complete_header_is_visible(self):
        self.verify_element_is_visible(self.__complete_header, "Complete Header")

    def validate_complete_text(self, complete_text: str):
        self.verify_text_element(self.__complete_text, complete_text, "Complete Text")

    def validate_back_to_products_button_is_visible(self):
        self.verify_element_is_visible(self.__back_to_products_button, "Back Home Buttom")

    def click_back_to_products_button(self):
        self.do_click(self.__back_to_products_button, "All Items Button")

