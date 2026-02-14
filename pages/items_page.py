from playwright.sync_api import Page
from pages.base_page import BasePage

class ItemsPage(BasePage):

    ITEMS_PAGE_URL = "https://www.saucedemo.com/inventory.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.__shopping_cart_link = page.locator("[data-test='shopping-cart-link']")
        self.__page_title = page.locator("[data-test='title']")
        self.__shopping_cart_badge = page.locator("[data-test='shopping-cart-badge']")
        self.__item_card = page.locator('[data-test="inventory-item-description"]')


    def add_item_to_basket(self, item_name: str):
        items_to_choose = self.__item_card.filter(has=self._page.locator("[data-test='inventory-item-name']", has_text=item_name))
        add_to_cart_button = items_to_choose.get_by_role("button", name="Add to cart")
        self.do_click(add_to_cart_button, f"Add to cart button for {item_name}")

    def validate_shopping_cart_link_is_visible(self):
        self.verify_element_is_visible(self.__shopping_cart_link, "Shopping Cart Link")

    def validate_page_title_text(self, page_title: str):
        self.verify_text_element(self.__page_title, page_title, "Page Title")

    def validate_added_items_amount(self, items_amount: int):
        self.verify_text_element(self.__shopping_cart_badge, f"{items_amount}", "Shopping Cart Badge")

    def click_shopping_cart_link(self):
        self.do_click(self.__shopping_cart_link, "Shopping Cart Link")

    def validate_page_url(self, page_url: str = ITEMS_PAGE_URL):
        self.verify_url(page_url)

