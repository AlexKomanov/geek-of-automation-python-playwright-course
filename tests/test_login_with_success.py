import pytest
import allure
# Local Fixtures
# @pytest.fixture
# def login_page(page: Page):
#     print("Local fixture: login_page")
#     return LoginPage(page)

@allure.epic("Authentication")
@allure.feature("Login Functionality")
@allure.title("Login with Standard User - Verify Successful Login")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.sanity
@pytest.mark.login_page
@pytest.mark.skip_browser("webkit")
@pytest.mark.regression
def test_login_with_standard_user(login_page, items_page):
    with allure.step("Navigate to login page"):
        login_page.navigate_to_login_page()

    with allure.step("Enter standard user credentials and login"):
        allure.attach("standard_user", name="Username", attachment_type=allure.attachment_type.TEXT)
        login_page.fill_username("standard_user")
        login_page.type_password("secret_sauce")
        login_page.click_login_button()

    with allure.step("Verify successful login and products page is displayed"):
        items_page.validate_page_title_text("Products")
        items_page.validate_page_url()
        items_page.validate_shopping_cart_link_is_visible()

@allure.epic("Authentication")
@allure.feature("Login Functionality")
@allure.title("Login with Problem User - Verify Login with Known Issues")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.login_page
@pytest.mark.skip_browser("webkit")
@pytest.mark.regression
def test_login_with_problem_user(login_page, items_page):
    with allure.step("Navigate to login page"):
        login_page.navigate_to_login_page()

    with allure.step("Enter problem user credentials and login"):
        allure.attach("problem_user", name="Username", attachment_type=allure.attachment_type.TEXT)
        login_page.fill_username("problem_user")
        login_page.type_password("secret_sauce")
        login_page.click_login_button()

    with allure.step("Verify successful login despite known UI issues"):
        items_page.validate_page_title_text("Products")
        items_page.validate_page_url()
        items_page.validate_shopping_cart_link_is_visible()

@allure.epic("Authentication")
@allure.feature("Login Functionality")
@allure.title("Login with Performance Glitch User - Verify Slow Login")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.sanity
@pytest.mark.login_page
@pytest.mark.skip_browser("webkit")
@pytest.mark.regression
def test_login_with_performance_glitch_user(login_page, items_page):
    with allure.step("Navigate to login page"):
        login_page.navigate_to_login_page()

    with allure.step("Enter performance glitch user credentials and login"):
        allure.attach("performance_glitch_user", name="Username", attachment_type=allure.attachment_type.TEXT)
        login_page.fill_username("performance_glitch_user")
        login_page.type_password("secret_sauce")
        login_page.click_login_button()

    with allure.step("Verify successful login with performance delay"):
        items_page.validate_page_title_text("Products")
        items_page.validate_page_url()
        items_page.validate_shopping_cart_link_is_visible()


@allure.epic("Authentication")
@allure.feature("Login Functionality")
@allure.title("Login with Error User - Verify Login with Error Conditions")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.login_page
@pytest.mark.regression
def test_login_with_error_user(login_page, items_page):
    with allure.step("Navigate to login page"):
        login_page.navigate_to_login_page()

    with allure.step("Enter error user credentials and login"):
        allure.attach("error_user", name="Username", attachment_type=allure.attachment_type.TEXT)
        login_page.fill_username("error_user")
        login_page.type_password("secret_sauce")
        login_page.click_login_button()

    with allure.step("Verify successful login"):
        items_page.validate_page_title_text("Products")
        items_page.validate_page_url()
        items_page.validate_shopping_cart_link_is_visible()

@allure.epic("Authentication")
@allure.feature("Login Functionality")
@allure.title("Login with Visual User - Verify Login with Visual Differences")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.login_page
@pytest.mark.regression
def test_login_with_visual_user(login_page, items_page):
    with allure.step("Navigate to login page"):
        login_page.navigate_to_login_page()

    with allure.step("Enter visual user credentials and login"):
        allure.attach("visual_user", name="Username", attachment_type=allure.attachment_type.TEXT)
        login_page.fill_username("visual_user")
        login_page.type_password("secret_sauce")
        login_page.click_login_button()

    with allure.step("Verify successful login with visual differences"):
        items_page.validate_page_title_text("Products")
        items_page.validate_page_url()
        items_page.validate_shopping_cart_link_is_visible()