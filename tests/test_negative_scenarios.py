import pytest
import csv
import allure


def load_test_data_from_csv(file_path):
    with open(file_path, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        return [tuple(row) for row in reader]

test_data = load_test_data_from_csv("data/test_data.csv")

@allure.epic("Authentication")
@allure.feature("Login Validation")
@allure.title("Login with Invalid Credentials - Verify Error Messages")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.sanity
@pytest.mark.regression
@pytest.mark.parametrize("username,password,error_message_text", test_data)
def test_negative_scenarios(login_page, username: str, password: str, error_message_text: str):
    with allure.step(f"Navigate to login page"):
        login_page.navigate_to_login_page()

    with allure.step(f"Enter credentials: username='{username}', password='***'"):
        allure.attach(username, name="Username", attachment_type=allure.attachment_type.TEXT)
        login_page.fill_username(username)
        login_page.type_password(password)

    with allure.step("Click login button"):
        login_page.click_login_button()

    with allure.step(f"Verify error message: '{error_message_text}'"):
        allure.attach(error_message_text, name="Expected Error Message", attachment_type=allure.attachment_type.TEXT)
        login_page.validate_login_error_message(error_message_text)
        login_page.validate_page_url()

