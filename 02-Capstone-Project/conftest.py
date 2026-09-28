import pytest
from pytest_html import extras

from helpers import launch_browser, load_test_data, take_screenshot


# Command line option:  pytest --headless
def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store_true", default=False,
        help="Run Chrome without opening a visible window",
    )


# Fixtures
@pytest.fixture(scope="session")
def test_data():
    return load_test_data()


@pytest.fixture(scope="module")
def driver(request):
    browser = launch_browser(headless=request.config.getoption("--headless"))
    yield browser          # tests run here
    browser.quit()         # teardown


# HTML report customisation
def pytest_html_report_title(report):
    report.title = "E-Commerce Automation - Execution Report"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        browser = item.funcargs.get("driver")
        if browser is not None:
            try:
                take_screenshot(browser, item.name)
                image = browser.get_screenshot_as_base64()
                report.extras = getattr(report, "extras", []) + [extras.image(image)]
            except Exception as exc:  # screenshot problems must not break the run
                print(f"Could not capture screenshot for {item.name}: {exc}")
