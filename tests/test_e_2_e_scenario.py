import pytest
import allure

items_to_add = ["Sauce Labs Backpack", "Sauce Labs Bike Light",
                "Sauce Labs Bolt T-Shirt", "Sauce Labs Fleece Jacket", "Sauce Labs Onesie"]

@allure.epic("E-commerce")
@allure.feature("Complete Purchase Flow")
@allure.title("End-to-End Checkout: Add Multiple Items and Complete Order")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.regression
@pytest.mark.checkout
def test_e_2_e(login_page, items_page, cart_page,
               checkout_info_page, checkout_overview_page,
               checkout_complete_page, sidebar_menu) -> None:

    with allure.step("Login to the application"):
        login_page.navigate_to_login_page()
        login_page.fill_username("standard_user")
        login_page.type_password("secret_sauce")
        login_page.click_login_button()

    with allure.step("Verify Items page is loaded and validate elements"):
        items_page.validate_page_title_text("Products")
        items_page.validate_page_url()
        items_page.validate_shopping_cart_link_is_visible()

    with allure.step(f"Add {len(items_to_add)} items to the shopping cart"):
        for item in items_to_add:
            items_page.add_item_to_basket(item)

    with allure.step("Verify cart badge and navigate to cart"):
        items_page.validate_added_items_amount(len(items_to_add))
        items_page.click_shopping_cart_link()

    with allure.step("Verify cart page and proceed to checkout"):
        cart_page.validate_page_title_text("Your Cart")
        cart_page.click_checkout_button()

    with allure.step("Fill checkout information (First Name, Last Name, Postal Code)"):
        checkout_info_page.validate_page_title_text("Checkout: Your Information")
        checkout_info_page.fill_first_name("Alex")
        checkout_info_page.fill_last_name("Komanov")
        checkout_info_page.fill_postal_code("20100")
        checkout_info_page.click_continue_button()

    with allure.step("Verify checkout overview and complete the order"):
        checkout_overview_page.validate_page_title_text("Checkout: Overview")
        checkout_overview_page.validate_payment_info_label_is_visible()
        checkout_overview_page.validate_shipping_info_label_text("Shipping Information:")
        checkout_overview_page.validate_total_info_label_is_visible()
        checkout_overview_page.click_finish_button()

    with allure.step("Verify order completion message"):
        checkout_complete_page.validate_complete_header_is_visible()
        checkout_complete_page.validate_page_title_text("Checkout: Complete!")
        checkout_complete_page.validate_complete_text("Your order has been dispatched, and will arrive just as fast as the pony can get there!")
        checkout_complete_page.validate_back_to_products_button_is_visible()

    with allure.step("Return to products page and logout"):
        checkout_complete_page.click_back_to_products_button()
        sidebar_menu.click_menu_button()
        sidebar_menu.click_reset_sidebar_link()
        sidebar_menu.click_logout_sidebar_link()

    with allure.step("Verify successful logout"):
        login_page.validate_login_container_is_visible()