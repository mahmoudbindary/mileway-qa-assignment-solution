import os
import os.path

import pytest
from selenium import webdriver
from selenium.webdriver import ChromeOptions, FirefoxOptions, EdgeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from src.utilities import utilities

logger = utilities.custom_logger()


# Fixture to log start and finish of each test case
@pytest.fixture(autouse=True)
def setup_and_teardown(request):
    test_case_name = request.node.name
    logger.info(f"Starting test case: {test_case_name} ...")
    yield
    test_case_name = request.node.name
    logger.info(f"Test case: {test_case_name} finished.")


# Adding cmd options to control running web test cases
def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome",
        help="Select browser to run web tests. ex: --browser edge",
        choices=("chrome", "firefox", "edge")
    )
    parser.addoption(
        "--headless", action="store_true", default="",
        help="Select headless mode for web tests. ex: --headless"
    )


# Fixture to set up and teardown webdriver for each web test case
@pytest.fixture(scope="function")
def driver(request):
    global driver
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if browser.casefold() == "chrome":
        options = ChromeOptions()
        if headless: options.add_argument("--headless")
        driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

    elif browser.casefold() == "firefox":
        options = FirefoxOptions()
        if headless: options.add_argument("--headless")
        driver = webdriver.Firefox(options=options, service=Service(GeckoDriverManager().install()))

    elif browser.casefold() == "edge":
        options = EdgeOptions()
        if headless: options.add_argument("--headless")
        driver = webdriver.Edge(options=options, service=Service(EdgeChromiumDriverManager().install()))
    else:
        raise Exception("Browser name is not correct.")

    driver.maximize_window()
    driver.implicitly_wait(3)
    web_base_url = utilities.read_configs("web", "web_base_url")
    driver.get(web_base_url)
    yield driver
    driver.quit()


# Fixture to capture and add screenshot to report on web test cases failure
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            report_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/results/"))
            file_name = report.nodeid.replace("::", "_")
            if "web" in file_name:
                file_name = file_name.split(".")[1] + ".png"
                destination_file = os.path.join(report_directory, file_name)
                driver.save_screenshot(destination_file)
                extra.append(pytest_html.extras.image(file_name))
        report.extra = extra


# Set report title
def pytest_html_report_title(report):
    report.title = "Mileway Automation Report"
