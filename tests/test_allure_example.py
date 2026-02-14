"""
Example test file demonstrating advanced Allure reporting features.
This file shows best practices for using @allure.step as a decorator function.
"""

import pytest
import allure


# Helper functions with @allure.step decorator
@allure.step("Login with username: '{username}'")
def perform_login(login_page, username: str, password: str):
    """Reusable login helper with step reporting"""
    login_page.navigate_to_login_page()
    login_page.fill_username(username)
    login_page.type_password(password)
    login_page.click_login_button()
    allure.attach(username, name="Logged in Username", attachment_type=allure.attachment_type.TEXT)


@allure.step("Add items to cart: {items}")
def add_items_to_cart(items_page, items: list):
    """Add multiple items to cart with step reporting"""
    for item in items:
        items_page.add_item_to_basket(item)
    allure.attach(f"Added {len(items)} items", name="Cart Summary", attachment_type=allure.attachment_type.TEXT)


@allure.step("Complete checkout with customer info: {first_name} {last_name}, {postal_code}")
def fill_checkout_information(checkout_info_page, first_name: str, last_name: str, postal_code: str):
    """Fill checkout form with step reporting"""
    checkout_info_page.fill_first_name(first_name)
    checkout_info_page.fill_last_name(last_name)
    checkout_info_page.fill_postal_code(postal_code)
    checkout_info_page.click_continue_button()
    # Attach customer info
    customer_info = f"Name: {first_name} {last_name}\nPostal Code: {postal_code}"
    allure.attach(customer_info, name="Customer Information", attachment_type=allure.attachment_type.TEXT)


@allure.step("Verify order completion and logout")
def verify_and_logout(checkout_complete_page, sidebar_menu, login_page):
    """Verify successful order and logout with step reporting"""
    checkout_complete_page.validate_complete_header_is_visible()
    checkout_complete_page.validate_page_title_text("Checkout: Complete!")
    checkout_complete_page.click_back_to_products_button()

    sidebar_menu.click_menu_button()
    sidebar_menu.click_logout_sidebar_link()
    login_page.validate_login_container_is_visible()


# Example Test 1: Using helper functions with @allure.step decorators
@allure.epic("E-commerce")
@allure.feature("Order Processing")
@allure.title("Complete Order Flow Using Helper Functions")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
This test demonstrates a complete order flow using reusable helper functions
decorated with @allure.step for better code organization and reporting.
""")
@pytest.mark.regression
@pytest.mark.checkout
def test_order_with_helper_functions(login_page, items_page, cart_page, checkout_info_page,
                                     checkout_overview_page, checkout_complete_page, sidebar_menu):
    # Using helper functions - each will appear as a step in Allure report
    perform_login(login_page, "standard_user", "secret_sauce")

    with allure.step("Verify products page loaded"):
        items_page.validate_page_title_text("Products")
        items_page.validate_page_url()

    items_to_purchase = ["Sauce Labs Backpack", "Sauce Labs Bike Light"]
    add_items_to_cart(items_page, items_to_purchase)

    with allure.step("Navigate to cart and proceed to checkout"):
        items_page.click_shopping_cart_link()
        cart_page.validate_page_title_text("Your Cart")
        cart_page.click_checkout_button()

    fill_checkout_information(checkout_info_page, "John", "Smith", "90210")

    with allure.step("Review and complete order"):
        checkout_overview_page.validate_page_title_text("Checkout: Overview")
        checkout_overview_page.click_finish_button()

    verify_and_logout(checkout_complete_page, sidebar_menu, login_page)


# Example Test 2: Nested steps for complex workflows
@allure.epic("E-commerce")
@allure.feature("Shopping Experience")
@allure.title("Multi-Step Shopping with Nested Steps")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("Demonstrates nested steps for complex workflows")
@pytest.mark.regression
def test_nested_steps_example(login_page, items_page, cart_page):

    with allure.step("User Authentication"):
        with allure.step("Navigate to login page"):
            login_page.navigate_to_login_page()

        with allure.step("Enter credentials"):
            login_page.fill_username("standard_user")
            login_page.type_password("secret_sauce")

        with allure.step("Submit login form"):
            login_page.click_login_button()

    with allure.step("Shopping Phase"):
        with allure.step("Verify products page"):
            items_page.validate_page_title_text("Products")
            items_page.validate_shopping_cart_link_is_visible()

        with allure.step("Add first item"):
            items_page.add_item_to_basket("Sauce Labs Backpack")
            allure.attach("Sauce Labs Backpack - $29.99", name="Item 1", attachment_type=allure.attachment_type.TEXT)

        with allure.step("Add second item"):
            items_page.add_item_to_basket("Sauce Labs Bike Light")
            allure.attach("Sauce Labs Bike Light - $9.99", name="Item 2", attachment_type=allure.attachment_type.TEXT)

    with allure.step("Cart Verification"):
        with allure.step("Navigate to cart"):
            items_page.click_shopping_cart_link()

        with allure.step("Validate cart contents"):
            cart_page.validate_page_title_text("Your Cart")


# Example Test 3: Parameterized test with different severities
@allure.epic("Authentication")
@allure.feature("Multi-User Login")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.sanity
@pytest.mark.login_page
@pytest.mark.parametrize("username,expected_result", [
    ("standard_user", "success"),
    ("performance_glitch_user", "success"),
    ("problem_user", "success"),
])
def test_multiple_user_login(login_page, items_page, username, expected_result):
    """Test login with different user types"""
    allure.dynamic.title(f"Login Test - {username}")
    allure.dynamic.description(f"Verify login functionality for user type: {username}")

    with allure.step(f"Login with user: {username}"):
        login_page.navigate_to_login_page()
        login_page.fill_username(username)
        login_page.type_password("secret_sauce")
        login_page.click_login_button()
        allure.attach(username, name="Test User", attachment_type=allure.attachment_type.TEXT)

    with allure.step(f"Verify {expected_result} result"):
        items_page.validate_page_title_text("Products")
        items_page.validate_page_url()


# Example Test 4: Link to external resources
@allure.epic("E-commerce")
@allure.feature("Product Catalog")
@allure.title("Product Page Navigation")
@allure.severity(allure.severity_level.MINOR)
@allure.link("https://www.saucedemo.com", name="Application URL")
@allure.issue("JIRA-123", name="Related Jira Ticket")
@allure.testcase("TC-001", name="Test Case ID")
@pytest.mark.ui
def test_with_links(login_page, items_page):
    """Test with external links in Allure report"""

    with allure.step("Login and verify products page"):
        perform_login(login_page, "standard_user", "secret_sauce")
        items_page.validate_page_title_text("Products")
        items_page.validate_shopping_cart_link_is_visible()

    allure.attach("Test completed successfully", name="Test Result", attachment_type=allure.attachment_type.TEXT)
