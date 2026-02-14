from playwright.sync_api import Page
from pages.base_page import BasePage

class CartPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.__page_title = page.locator("[data-test='title']")
        self.__checkout_button = page.locator("[data-test='checkout']")

    def validate_page_title_text(self, page_title: str):
        self.verify_text_element(self.__page_title, page_title, "Page Title")

    def click_checkout_button(self):
        self.do_click(self.__checkout_button, "Checkout Button")

