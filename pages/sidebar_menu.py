from playwright.sync_api import Page
from pages.base_page import BasePage

class SidebarMenu(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)
        self.__menu_button = page.get_by_role("button", name="Open Menu")
        self.__reset_sidebar_link = page.locator("[data-test='reset-sidebar-link']")
        self.__logout_sidebar_link = page.locator("[data-test='logout-sidebar-link']")

    def click_menu_button(self):
        self.do_click(self.__menu_button, "Menu Button")

    def click_reset_sidebar_link(self):
        self.do_click(self.__reset_sidebar_link, "Reset Sidebar Link")

    def click_logout_sidebar_link(self):
        self.do_click(self.__logout_sidebar_link, "Logout Sidebar Link")

