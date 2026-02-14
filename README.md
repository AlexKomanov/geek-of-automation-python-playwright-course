# Playwright Python Test Automation Framework

A robust end-to-end test automation framework for the [Sauce Demo](https://www.saucedemo.com/) e-commerce application, built with **Playwright**, **pytest**, and **Allure Report 3**.

📺 **Watch the full course on YouTube:** [Playwright Python Course Playlist](https://www.youtube.com/playlist?list=PL1ZSrkGSJEGNdbf7k4Uf1m8rMXBITacsD)

## Features

- **Page Object Model (POM)** — Clean separation of test logic and page interactions
- **Allure Report 3** — Rich HTML reports with screenshots, videos, traces, and step-by-step execution details
- **Data-Driven Testing** — CSV-powered parameterized tests for negative scenarios
- **Auto-Attached Artifacts** — Screenshots on every test; video and trace on failure
- **Custom Logging** — Every page action is logged with descriptive element names
- **Sensitive Data Masking** — Passwords are masked in logs automatically

## Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.12+ | Language |
| Playwright | 1.55+ | Browser automation |
| pytest | 8.4+ | Test runner |
| pytest-playwright | 0.7+ | Playwright-pytest integration |
| allure-pytest | 2.15+ | Allure reporting |
| Allure CLI | 3.1+ | Report generation |

## Quick Start

```bash
# Clone and install
pip install -r requirements.txt
playwright install chromium

# Run all tests
pytest

# Run by marker
pytest -m sanity
pytest -m regression

# View Allure report
allure serve allure-results
```

## Project Structure

```
├── pages/                  # Page Object classes
│   ├── base_page.py        # Base class with shared actions
│   ├── login_page.py       # Login page
│   ├── items_page.py       # Product catalog
│   ├── cart_page.py        # Shopping cart
│   ├── checkout_info_page.py
│   ├── checkout_overview_page.py
│   ├── checkout_complete_page.py
│   └── sidebar_menu.py     # Hamburger menu
├── tests/                  # Test suite
│   ├── conftest.py         # Fixtures & Allure hooks
│   ├── test_e_2_e_scenario.py
│   ├── test_negative_scenarios.py
│   ├── test_login_with_success.py
│   └── test_allure_example.py
├── data/                   # Test data (CSV)
├── utils/                  # Logging utilities
├── pytest.ini              # Pytest configuration
└── requirements.txt        # Python dependencies
```

## Test Markers

| Marker | Description |
|---|---|
| `sanity` | Core smoke tests |
| `regression` | Full regression suite |
| `login_page` | Login functionality |
| `checkout` | Checkout process |
| `ui` | UI component tests |
| `api` | API tests |

## Allure Reporting

Tests automatically generate results in `allure-results/`. View reports with:

```bash
allure serve allure-results
```

Reports include screenshots, video recordings, Playwright traces, step-by-step execution, severity levels, and Epic/Feature/Story organization.

See [CLAUDE.md](CLAUDE.md) for detailed Allure usage guide and full project documentation.
