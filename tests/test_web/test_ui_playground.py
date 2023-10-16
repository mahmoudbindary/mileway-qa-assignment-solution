import pytest

from src.helpers.WebPagesHelper import HomePage
from src.utilities import utilities

pytestmark = [pytest.mark.usefixtures("driver"), pytest.mark.web, pytest.mark.regression]

logger = utilities.custom_logger()


def test_class_attribute(driver):
    logger.info("Navigate to Class Attribute page")
    class_attribute_page = HomePage(driver).go_to_class_attribute_page()

    logger.info("Click on primary button using class css selector")
    class_attribute_page.click_on_primary_button()

    logger.warning("Check alert is displayed after right button clicked")
    class_attribute_page.assert_alert_is_present()
    expected_alert_text = "Primary button pressed"
    actual_alert_text = class_attribute_page.get_alert_text()

    logger.warning(f"Check alert text is as expected: {expected_alert_text}")
    assert actual_alert_text == expected_alert_text


def test_click(driver):
    logger.info("Navigate to Click page")
    click_page = HomePage(driver).go_to_click_page()
    expected_bad_button_class_before_click = "btn-primary"
    actual_bad_button_class_before_click = click_page.get_bad_button_class_attribute()

    logger.warning(f"Check button class is as expected: {actual_bad_button_class_before_click}")
    assert expected_bad_button_class_before_click in actual_bad_button_class_before_click

    logger.info("Click on button using javascript executor")
    click_page.click_on_bad_button_as_dom_event()
    actual_bad_button_class_after_dom_click = click_page.get_bad_button_class_attribute()

    logger.warning("Check button class is still the same")
    assert expected_bad_button_class_before_click in actual_bad_button_class_after_dom_click
    expected_bad_button_class_after_click = "btn-success"

    logger.info("Click on button using webdriver actions")
    click_page.click_on_bad_button_as_physical_mouse()
    actual_bad_button_class_after_physical_click = click_page.get_bad_button_class_attribute()

    logger.warning(f"Check button class is updated to: {actual_bad_button_class_after_physical_click}")
    assert expected_bad_button_class_after_click in actual_bad_button_class_after_physical_click


def test_dynamic_table(driver):
    logger.info("Navigate to Dynamic Table page")
    dynamic_table_page = HomePage(driver).go_to_dynamic_table_page()

    logger.info("Read chrome cpu value from label")
    expected_chrome_cpu_value = dynamic_table_page.get_chrome_cpu_value_from_label()

    logger.info("Read chrome cpu value from dynamic table")
    actual_chrome_cpu_value = dynamic_table_page.get_chrome_cpu_value_from_table()

    logger.warning(f"Check value from label: {expected_chrome_cpu_value}, "
                   f"is equal to value from table: {actual_chrome_cpu_value}")
    assert actual_chrome_cpu_value == expected_chrome_cpu_value


@pytest.mark.parametrize("username, password, valid", utilities.read_web_login_test_data())
def test_sample_app(driver, username, password, valid):
    logger.info("Navigate to Sample App page")
    sample_app_page = HomePage(driver).go_to_sample_app_page()

    logger.info(f"Login using username: {username}, password: {password}")
    sample_app_page.type_user_name_and_password(username, password)
    sample_app_page.click_login_button()
    login_status_text = sample_app_page.get_login_status_label_text()
    login_button_text = sample_app_page.get_login_button_text()
    login_button_text_before_successful_login = "Log In"
    if valid:
        login_button_text_after_successful_login = "Log Out"

        logger.warning(f"Check login status label after successful login is: Welcome, {username}")
        assert login_status_text == f"Welcome, {username}!"
        assert login_button_text == login_button_text_after_successful_login

        logger.info("Click logout button")
        sample_app_page.click_logout_button()
        login_status_text = sample_app_page.get_login_status_label_text()
        login_button_text = sample_app_page.get_login_button_text()
        logged_out_text = "User logged out."

        logger.warning(f"Check login status label after logging out is: {logged_out_text}")
        assert login_status_text == logged_out_text
        assert login_button_text == login_button_text_before_successful_login
    else:
        logger.warning("Check login status label after invalid login is: invalid_data_text")
        invalid_data_text = "Invalid username/password"
        assert login_status_text == invalid_data_text
        assert login_button_text == login_button_text_before_successful_login
