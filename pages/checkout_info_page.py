from playwright.sync_api import Page
from pages.base_page import BasePage

class CheckoutInfoPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.__page_title = page.locator("[data-test='title']")
        self.__first_name_field = page.locator("[data-test='firstName']")
        self.__last_name_field = page.locator("[data-test='lastName']")
        self.__postal_code_field = page.locator("[data-test='postalCode']")
        self.__continue_button = page.locator("[data-test='continue']")

    def validate_page_title_text(self, page_title: str):
        self.verify_text_element(self.__page_title, page_title, "Page Title")

    def fill_first_name(self, first_name: str):
        self.do_fill(self.__first_name_field, first_name, "First Name Field")

    def fill_last_name(self, last_name: str):
        self.do_fill(self.__last_name_field, last_name, "Last Name Field")

    def fill_postal_code(self, postal_code: str):
        self.do_fill(self.__postal_code_field, postal_code, "Postal Code Field")

    def click_continue_button(self):
        self.do_click(self.__continue_button, "Continue Button")

