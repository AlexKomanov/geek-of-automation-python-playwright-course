# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Playwright Python test automation framework for testing the Sauce Demo e-commerce application (https://www.saucedemo.com/). The project uses the Page Object Model (POM) design pattern with pytest as the test framework and Allure Report 3 for comprehensive test reporting.

## Running Tests

### Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Install Allure CLI (if not already installed)
npm install -g allure
allure --version  # Verify Allure 3.x is installed
```

### Run All Tests
```bash
pytest
```

### Run Tests by Marker
```bash
pytest -m sanity           # Run sanity tests
pytest -m regression       # Run regression tests
pytest -m login_page       # Run login page tests
pytest -m checkout         # Run checkout tests
pytest -m ui               # Run UI tests
pytest -m api              # Run API tests
```

### Run Specific Test File
```bash
pytest tests/test_e_2_e_scenario.py
pytest tests/test_negative_scenarios.py
pytest tests/test_login_with_success.py
pytest tests/test_allure_example.py
```

### Run Single Test
```bash
pytest tests/test_e_2_e_scenario.py::test_e_2_e
pytest tests/test_negative_scenarios.py::test_negative_scenarios
pytest tests/test_login_with_success.py::test_login_with_standard_user
```

### Run Tests with Custom Options
```bash
pytest --headed              # Run with visible browser
pytest --browser firefox     # Run with Firefox
pytest -v                    # Verbose output
```

## Test Configuration

The `pytest.ini` file configures:
- **Log Settings**: Console logging with INFO level, formatted with timestamp/name/level/message
- **Default Options**: Tests run headed in Chrome (`--browser chromium --browser-channel chrome`) with tracing and video on failure (`--tracing retain-on-failure --video retain-on-failure`), screenshots always on (`--screenshot on --full-page-screenshot`)
- **Allure Integration**: Automatically saves test results to `allure-results/` directory (`--alluredir=allure-results`)
- **Custom Markers**: sanity, regression, login_page, checkout, ui, api

## Architecture

### Page Object Model Pattern

All page objects inherit from `BasePage` (`pages/base_page.py`) which provides:
- Common actions: `do_click()`, `do_fill()`, `do_press_sequentially()`
- Verification methods: `verify_text_element()`, `verify_element_is_visible()`, `verify_url()`
- Integrated logging via `utils/logger.py` — every action is logged with custom element names
- Uses Playwright's `expect()` API for assertions

### Page Objects (`pages/`)

| Page Object | File | Description |
|---|---|---|
| `BasePage` | `base_page.py` | Abstract base with shared actions and verifications |
| `LoginPage` | `login_page.py` | Login form interactions, error validation, URL: `https://www.saucedemo.com/` |
| `ItemsPage` | `items_page.py` | Product catalog — add to cart, cart badge, page title, URL: `/inventory.html` |
| `CartPage` | `cart_page.py` | Cart page — title validation, checkout button |
| `CheckoutInfoPage` | `checkout_info_page.py` | Checkout form — first name, last name, postal code, continue |
| `CheckoutOverviewPage` | `checkout_overview_page.py` | Order review — payment/shipping/total labels, finish button |
| `CheckoutCompletePage` | `checkout_complete_page.py` | Order confirmation — header, text, back to products |
| `SidebarMenu` | `sidebar_menu.py` | Hamburger menu — open menu, reset app state, logout |

#### BasePage Methods

```python
navigate_to(url)                    # Navigate to URL
do_click(locator, name)             # Click element with logging
do_fill(locator, text, name)        # Fill text input with logging
do_press_sequentially(locator, text, delay, name, is_secret)  # Type char-by-char with optional masking
verify_text_element(locator, expected_text, name)   # Assert element contains text
verify_element_is_visible(locator, name)            # Assert element is visible
verify_url(url)                     # Assert page URL matches
```

### Test Files (`tests/`)

| Test File | Markers | Description |
|---|---|---|
| `test_e_2_e_scenario.py` | regression, checkout | Full E2E: login → add 5 items → checkout → complete → logout |
| `test_negative_scenarios.py` | sanity, regression | Parameterized invalid login tests (CSV-driven: locked user, empty fields, wrong password) |
| `test_login_with_success.py` | sanity, regression, login_page | Login tests for all user types: standard, problem, performance_glitch, error, visual |
| `test_allure_example.py` | regression, checkout, sanity, login_page, ui | Advanced Allure examples: helper functions with `@allure.step`, nested steps, parameterized multi-user login, external links |

Root-level test files (non-POM, standalone):
- `test_main.py` — Basic Playwright test with aria snapshot assertion
- `test_successful_login_scenarios.py` — Simple Playwright login test without POM

### Fixtures (`tests/conftest.py`)

**Session-scoped:**
- `browser_context_args` — Sets viewport and video resolution to 1920×1080

**Function-scoped page object fixtures:**
- `login_page`, `items_page`, `cart_page`, `checkout_info_page`, `checkout_overview_page`, `checkout_complete_page`, `sidebar_menu`

**Hooks:**
- `pytest_runtest_makereport` — Attaches screenshots (always) after each test call phase
- `pytest_runtest_teardown` — Attaches video and trace files for **failed tests only** (retain-on-failure)

### Test Data (`data/`)

- `test_data.csv` — CSV with columns: `Username`, `Password`, `Error Message`
  - Test scenarios: locked out user, empty username, empty password, wrong password
- Loaded via `csv.reader()` in `test_negative_scenarios.py` with `@pytest.mark.parametrize`

### Utilities (`utils/`)

- `logger.py` — `get_logger(name)` function returning a configured `logging.Logger` with console handler, INFO level, timestamped format

## Allure Reporting

The project uses Allure Report 3 for comprehensive test reporting with rich visualizations, step-by-step execution details, test history, and automatic attachment of screenshots, videos, and traces.

### Prerequisites

- **Allure CLI 3.1.0+**: Installed via npm (`npm install -g allure`)
- **allure-pytest 2.15.3**: Python package (included in requirements.txt)

### Generate and View Allure Reports

```bash
# Tests automatically generate Allure results (configured in pytest.ini)
pytest

# Generate and open HTML report in browser (easiest method)
allure serve allure-results

# Or generate static HTML report (Allure 3.x syntax)
allure generate --output allure-report allure-results
allure open allure-report
```

### Run Tests and View Report

```bash
# Run specific tests and view report
pytest tests/test_e_2_e_scenario.py
allure serve allure-results

# Run with markers
pytest -m sanity
allure serve allure-results

# Clean old results before new run
rm -rf allure-results allure-report
pytest
allure serve allure-results
```

### Automatic Attachments

The `conftest.py` hooks automatically attach these artifacts to Allure reports:

| Artifact | Format | When Attached |
|---|---|---|
| Screenshot (full-page) | PNG | After every test (pass or fail) |
| Video recording | WEBM | After **failed** tests only (retain-on-failure) |
| Playwright trace | ZIP | After **failed** tests only (retain-on-failure) |

Videos and traces are located by scanning `test-results/` for the most recently modified directory within a 5-second window.

### Allure Decorators and Annotations

Import Allure in your test files:
```python
import allure
```

#### Test Organization

**Epic, Feature, Story** — Organize tests hierarchically:
```python
@allure.epic("E-Commerce")
@allure.feature("Shopping Cart")
@allure.story("Add Items to Cart")
def test_add_item_to_cart(items_page, cart_page):
    pass
```

**Title and Description** — Customize test display:
```python
@allure.title("User can successfully add item to cart")
@allure.description("This test verifies that a user can add an item to the shopping cart")
def test_add_item(items_page):
    pass
```

**Dynamic Titles** — Use placeholders for parameterized tests:
```python
@allure.title("Login with credentials: {username}")
@pytest.mark.parametrize("username,password", [("user1", "pass1"), ("user2", "pass2")])
def test_login(username, password, login_page):
    pass
```

**Dynamic Allure Attributes** — Set at runtime:
```python
allure.dynamic.title(f"Login Test - {username}")
allure.dynamic.description(f"Verify login for user type: {username}")
```

#### Severity Levels

Mark test importance for prioritization:

| Severity | When to Use | Example |
|---|---|---|
| `BLOCKER` | Blocks testing or critical path | Login, authentication failures |
| `CRITICAL` | Core functionality | Checkout, payment processing, user registration |
| `NORMAL` | Standard features (default) | Product filtering, search, cart operations |
| `MINOR` | Secondary features | Tooltips, sorting, UI enhancements |
| `TRIVIAL` | Cosmetic issues | Styling, text formatting, minor UI glitches |

```python
@allure.severity(allure.severity_level.BLOCKER)
def test_login(login_page):
    pass

@allure.severity(allure.severity_level.CRITICAL)
def test_checkout(checkout_page):
    pass
```

#### Links and Issue Tracking

Link tests to external systems:
```python
@allure.link("https://www.saucedemo.com", name="Sauce Demo Website")
@allure.issue("JIRA-123", name="Bug: Cart not updating")
@allure.testcase("TC-456", name="Test Case: Add to Cart")
def test_cart_functionality(items_page, cart_page):
    pass
```

#### Test Steps

Create detailed step-by-step reporting using two approaches:

**A. Context Manager (inline steps):**
```python
def test_login(login_page):
    with allure.step("Navigate to login page"):
        login_page.navigate_to_login_page()

    with allure.step("Enter credentials and submit"):
        login_page.fill_username("user")
        login_page.type_password("pass")
        login_page.click_login_button()
```

**B. Decorator (reusable helper functions):**
```python
@allure.step("Login with username: '{username}'")
def perform_login(login_page, username: str, password: str):
    login_page.navigate_to_login_page()
    login_page.fill_username(username)
    login_page.type_password(password)
    login_page.click_login_button()
```

**Nested Steps** — Steps inside steps for complex workflows:
```python
with allure.step("User Authentication"):
    with allure.step("Navigate to login page"):
        login_page.navigate_to_login_page()
    with allure.step("Enter credentials"):
        login_page.fill_username("standard_user")
        login_page.type_password("secret_sauce")
    with allure.step("Submit login form"):
        login_page.click_login_button()
```

#### Manual Attachments

Add custom attachments in tests:
```python
# Attach text
allure.attach("Additional info", name="Notes", attachment_type=allure.attachment_type.TEXT)

# Attach JSON
import json
data = {"key": "value"}
allure.attach(json.dumps(data, indent=2), name="Test Data", attachment_type=allure.attachment_type.JSON)

# Attach HTML
allure.attach("<h1>Test Results</h1>", name="HTML Report", attachment_type=allure.attachment_type.HTML)

# Attach file
with open("test_data.csv", "rb") as file:
    allure.attach(file.read(), name="Test Data CSV", attachment_type=allure.attachment_type.CSV)

# Attach screenshot manually
screenshot = page.screenshot()
allure.attach(screenshot, name="Custom Screenshot", attachment_type=allure.attachment_type.PNG)
```

**Available Attachment Types:**
`TEXT`, `CSV`, `JSON`, `XML`, `HTML`, `PNG`, `JPG`, `WEBM` (videos), `MP4`, `ZIP` (traces)

#### Parameters

Parameters are automatically shown in Allure report with `@pytest.mark.parametrize`:
```python
@pytest.mark.parametrize("username,password,expected_error", [
    ("invalid_user", "secret_sauce", "Epic sadface: Username and password do not match"),
    ("", "", "Epic sadface: Username is required"),
])
def test_invalid_login(username, password, expected_error, login_page):
    pass
```

### Allure Report Features

**Report Navigation:**
- **Overview** — Test execution summary, trends, and statistics
- **Categories** — Test failures grouped by error type
- **Suites** — Tests organized by test files/suites
- **Graphs** — Visual charts (severity, duration, status)
- **Timeline** — Chronological test execution view
- **Behaviors** — Tests grouped by Epic/Feature/Story
- **Packages** — Tests organized by package structure

**Report Capabilities:**
- Click on any test to see detailed execution steps
- View screenshots, videos, and traces inline
- Download Playwright traces and open with `playwright show-trace trace.zip`
- Filter tests by status (passed/failed/skipped)
- Sort by duration, severity, or name
- View test history across multiple runs
- Retry pattern analysis for flaky tests

### Allure Troubleshooting

**Video is 0 KB or not playing:**
- Ensure tests complete fully (video is finalized after browser context closes)
- Check `conftest.py` hooks are properly configured
- Verify `pytest.ini` has `--video retain-on-failure` in addopts

**Traces not showing:**
- Verify `--tracing retain-on-failure` is in pytest.ini addopts
- Check `test-results/` directory contains `trace.zip` files
- Ensure `pytest_runtest_teardown` hook is working in conftest.py

**Report not generating:**
- Verify Allure CLI is installed: `allure --version`
- Check `allure-results/` directory exists and contains `.json` files
- Use `allure serve` instead of `allure generate` for quick debugging

**Report shows no history:**
- Keep `allure-results/history` folder from previous runs before generating new reports

**Steps not showing in report:**
- Ensure you're using `with allure.step():` context manager or `@allure.step` decorator

## Directory Structure

```
playwright_python_24/
├── CLAUDE.md                     # This guidance file
├── README.md                     # Project readme
├── pytest.ini                    # Pytest configuration (markers, addopts, logging)
├── requirements.txt              # Python dependencies
├── test_main.py                  # Standalone basic Playwright test (non-POM)
├── test_successful_login_scenarios.py  # Standalone login test (non-POM)
├── pages/                        # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py              # Base class with shared actions & verifications
│   ├── login_page.py             # Login page interactions
│   ├── items_page.py             # Product catalog page
│   ├── cart_page.py              # Shopping cart page
│   ├── checkout_info_page.py     # Checkout information form
│   ├── checkout_overview_page.py # Order review page
│   ├── checkout_complete_page.py # Order confirmation page
│   └── sidebar_menu.py           # Hamburger sidebar menu
├── tests/                        # Test files and configuration
│   ├── __init__.py
│   ├── conftest.py               # Fixtures, hooks, Allure attachments
│   ├── test_e_2_e_scenario.py    # Full E2E checkout test
│   ├── test_negative_scenarios.py # Parameterized invalid login tests
│   ├── test_login_with_success.py # Login tests for all user types
│   └── test_allure_example.py    # Advanced Allure reporting examples
├── data/                         # Test data files
│   ├── __init__.py
│   └── test_data.csv             # CSV: negative login test data
├── utils/                        # Utility modules
│   ├── __init__.py
│   └── logger.py                 # Logging configuration
├── test-results/                 # Playwright artifacts (traces, videos, screenshots)
├── allure-results/               # Allure test results (JSON, auto-generated)
└── allure-report/                # Generated Allure HTML reports (if using allure generate)
```

## Development Guidelines

### Adding New Page Objects

1. Create new file in `pages/` directory
2. Inherit from `BasePage`
3. Define locators as private attributes with `__` prefix (name-mangled)
4. Use `data-test` attributes for selectors when available
5. Provide custom element names to BasePage methods for readable logs
6. Add page URL as class constant if applicable
7. Create corresponding fixture in `tests/conftest.py`

Example:
```python
class LoginPage(BasePage):
    BASE_URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.__username_textfield = page.locator("[data-test='username']")

    def fill_username(self, username: str):
        self.do_fill(self.__username_textfield, username, "Username Textfield")
```

### Writing Tests

1. Place tests in `tests/` directory
2. Use descriptive test names starting with `test_`
3. Apply appropriate markers (`@pytest.mark.sanity`, `@pytest.mark.regression`, etc.)
4. Add Allure annotations: `@allure.epic()`, `@allure.feature()`, `@allure.title()`, `@allure.severity()`
5. Inject required page object fixtures as test parameters
6. Follow the pattern: navigate → interact → validate
7. Wrap logical groups of actions in `with allure.step("...")` blocks
8. For data-driven tests, use CSV files in `data/` directory with `@pytest.mark.parametrize`

### Locator Strategy

Priority order:
1. `data-test` attributes: `page.locator("[data-test='element-id']")`
2. Semantic roles: `page.get_by_role("button", name="Login")`
3. Text/labels: `page.get_by_text("text")`
4. Other attributes as last resort

### Sensitive Data Handling

When typing passwords or sensitive data, use `do_press_sequentially()` with `is_secret=True` parameter to mask values in logs:
```python
self.do_press_sequentially(locator, password, name="Password", is_secret=True)
```

## Common Patterns

### E2E Test Flow
Login → Navigate to items → Add items to cart → Checkout → Complete order → Logout

### Parameterized Negative Tests
Load test data from CSV and parameterize tests to validate error messages for invalid inputs.

### Allure Best Practices for This Framework

1. **Use Markers with Allure** — Combine pytest markers with Allure annotations:
   ```python
   @pytest.mark.sanity
   @pytest.mark.login_page
   @allure.epic("Authentication")
   @allure.feature("Login")
   @allure.severity(allure.severity_level.BLOCKER)
   def test_successful_login(login_page, items_page):
       pass
   ```

2. **Leverage Auto-Attachments** — Screenshots, videos, and traces are automatically attached; no manual code needed

3. **Add Steps to Page Objects** — Decorate page object methods with `@allure.step()` for detailed reporting:
   ```python
   @allure.step("Fill login credentials: {username}")
   def login(self, username: str, password: str):
       self.fill_username(username)
       self.fill_password(password)
       self.click_login_button()
   ```

4. **Use Reusable Helper Functions** — Decorate helpers with `@allure.step` for clean, DRY test code:
   ```python
   @allure.step("Login with username: '{username}'")
   def perform_login(login_page, username: str, password: str):
       login_page.navigate_to_login_page()
       login_page.fill_username(username)
       login_page.type_password(password)
       login_page.click_login_button()
   ```

5. **Organize Tests Hierarchically** — Use Epic (project area) → Feature (functionality) → Story (user story) structure

6. **Set Appropriate Severity** — Mark tests by business impact for better prioritization

7. **Link to Test Cases** — Use `@allure.testcase()` and `@allure.issue()` to link tests to external systems

8. **Use Descriptive Titles** — Prefer `@allure.title("Login with Valid Credentials - Verify Dashboard Loads")` over `@allure.title("Test login")`

9. **Attach Relevant Data** — Attach test data, API responses, or custom screenshots at critical points

10. **Review Traces for Failures** — Download `trace.zip` from failed tests and open with `playwright show-trace trace.zip` for detailed debugging

### Page Validation

- Always validate page elements after navigation
- Verify page titles, URLs, and key element visibility
- Use descriptive validation method names: `validate_page_title_text()`, `validate_page_url()`
