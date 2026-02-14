import pytest
import allure
from pathlib import Path
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.items_page import ItemsPage
from pages.cart_page import CartPage
from pages.checkout_info_page import CheckoutInfoPage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.sidebar_menu import SidebarMenu
from utils.logger import get_logger

# Initialize logger
logger = get_logger(__name__)


# Configure viewport and video resolution for sharp recordings
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "record_video_size": {"width": 1920, "height": 1080},
    }


# Allure attachment hook - automatically attaches traces, videos, and screenshots after each test
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    # Store the test result in the item for later use
    if report.when == "call":
        item.test_failed = report.failed
        item.test_passed = report.passed

    # Attach artifacts after test execution (on teardown phase)
    if report.when == "call":
        # Get the page fixture if available
        if "page" in item.funcargs:
            page = item.funcargs["page"]

            # Attach screenshot (always, regardless of test result)
            try:
                screenshot_bytes = page.screenshot(full_page=True)
                allure.attach(
                    screenshot_bytes,
                    name="Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                logger.error(f"Failed to attach screenshot: {e}")

            # Mark that this test had video enabled (we'll find it later in test-results)
            # Note: With retain-on-failure, videos only exist for failed tests
            try:
                if hasattr(page, "video") and page.video:
                    item.has_video = True
            except Exception as e:
                logger.error(f"Failed to check video: {e}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_teardown(item):
    """Attach video and trace after test teardown when files are ready"""
    # Let the teardown complete first (including browser context closure)
    yield

    import time
    import os

    # Attach video from test-results directory (only for failed tests with retain-on-failure)
    if hasattr(item, "has_video") and hasattr(item, "test_failed") and item.test_failed:
        try:
            test_results_dir = Path("test-results")
            video_path = None

            if test_results_dir.exists():
                # Look for the most recently modified directory that contains a video.webm
                current_time = time.time()
                recent_dirs_with_video = []

                for dir_path in test_results_dir.iterdir():
                    if dir_path.is_dir():
                        video_file = dir_path / "video.webm"
                        # Only consider directories modified in the last 5 seconds with video
                        if video_file.exists() and (current_time - dir_path.stat().st_mtime < 5):
                            recent_dirs_with_video.append(dir_path)

                # Pick the most recent directory with video
                if recent_dirs_with_video:
                    most_recent = sorted(recent_dirs_with_video, key=lambda p: p.stat().st_mtime, reverse=True)[0]
                    video_path = most_recent / "video.webm"

            # Attach video if found
            if video_path and video_path.exists():
                time.sleep(0.3)  # Ensure file is fully written
                if video_path.stat().st_size > 0:
                    with open(video_path, "rb") as video_file:
                        allure.attach(
                            video_file.read(),
                            name="Video Recording",
                            attachment_type=allure.attachment_type.WEBM
                        )
                    logger.info(f"✓ Video attached for FAILED test: {video_path.name} ({video_path.stat().st_size} bytes)")
        except Exception as e:
            logger.error(f"✗ Failed to attach video: {e}")

    # Attach trace if available (only for failed tests with retain-on-failure)
    if "page" in item.funcargs and hasattr(item, "test_failed") and item.test_failed:
        try:
            test_results_dir = Path("test-results")
            trace_path = None

            if test_results_dir.exists():
                current_time = time.time()
                recent_dirs_with_trace = []

                for dir_path in test_results_dir.iterdir():
                    if dir_path.is_dir():
                        trace_file = dir_path / "trace.zip"
                        if trace_file.exists() and (current_time - dir_path.stat().st_mtime < 5):
                            recent_dirs_with_trace.append(dir_path)

                if recent_dirs_with_trace:
                    most_recent = sorted(recent_dirs_with_trace, key=lambda p: p.stat().st_mtime, reverse=True)[0]
                    trace_path = most_recent / "trace.zip"

            if trace_path and trace_path.exists() and trace_path.stat().st_size > 0:
                with open(trace_path, "rb") as trace_file:
                    allure.attach(
                        trace_file.read(),
                        name="Playwright Trace",
                        attachment_type=allure.attachment_type.ZIP
                    )
                logger.info(f"✓ Trace attached for FAILED test: {trace_path.name} ({trace_path.stat().st_size} bytes)")
        except Exception as e:
            logger.error(f"✗ Failed to attach trace: {e}")

# Global Fixtures
@pytest.fixture
def login_page(page: Page):
    logger.info("Global fixture: login_page")
    return LoginPage(page)

@pytest.fixture
def items_page(page: Page):
    return ItemsPage(page)

@pytest.fixture
def cart_page(page: Page):
    return CartPage(page)

@pytest.fixture
def checkout_info_page(page: Page):
    return CheckoutInfoPage(page)

@pytest.fixture
def checkout_overview_page(page: Page):
    return CheckoutOverviewPage(page)

@pytest.fixture
def checkout_complete_page(page: Page):
    return CheckoutCompletePage(page)

@pytest.fixture
def sidebar_menu(page: Page):
    return SidebarMenu(page)