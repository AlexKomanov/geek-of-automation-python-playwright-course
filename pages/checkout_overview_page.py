from playwright.sync_api import Page
from pages.base_page import BasePage

class CheckoutOverviewPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.__page_title = page.locator("[data-test='title']")
        self.__payment_info_label = page.locator("[data-test='payment-info-label']")
        self.__shipping_info_label = page.locator("[data-test='shipping-info-label']")
        self.__total_info_label = page.locator("[data-test='total-info-label']")
        self.__finish_button = page.locator("[data-test='finish']")

    def validate_page_title_text(self, page_title: str):
        self.verify_text_element(self.__page_title, page_title, "Page Title")

    def validate_payment_info_label_is_visible(self):
        self.verify_element_is_visible(self.__payment_info_label, "Payment Info Label")

    def validate_shipping_info_label_text(self, shipping_text: str):
        self.verify_text_element(self.__shipping_info_label, shipping_text, "Shipping Info Label")

    def validate_total_info_label_is_visible(self):
        self.verify_element_is_visible(self.__total_info_label, "Total Info Label")

    def click_finish_button(self):
        self.do_click(self.__finish_button, "Finish Button")

