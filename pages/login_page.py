from playwright.sync_api import Page
from pages.base_page import BasePage

# type + __name__ => LoginPage
# __name__ => pages.login_page


class LoginPage(BasePage):

    BASE_URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        super().__init__(page)

        self.__username_textfield = page.locator("[data-test='username']")
        self.__password_textfield = page.locator("[data-test='password']")
        self.__login_button = page.get_by_role("button", name="Login")
        self.__error_message = page.locator("[data-test='error']")
        self.__login_container = page.locator("[data-test='login-container'] div").filter(has_text="Login").first

    def navigate_to_login_page(self, url: str = BASE_URL):
        self.navigate_to(url)

    def fill_username(self, username: str):
        self.do_fill(self.__username_textfield, username, "Username Textfield")

    def type_password(self, password: str):
        self.do_press_sequentially(self.__password_textfield, password, name="Password Textfield", delay=350, is_secret=True)

    def click_login_button(self):
        self.do_click(self.__login_button, "Login Button")

    def validate_login_error_message(self, error_message_text: str):
        self.verify_text_element(self.__error_message, error_message_text, "Login Error Message")

    def validate_page_url(self, page_url: str = BASE_URL):
        self.verify_url(page_url)

    def validate_login_container_is_visible(self):
        self.verify_element_is_visible(self.__login_container, "Login Container")
