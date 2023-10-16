from selenium.common import TimeoutException, NoAlertPresentException
from selenium.webdriver import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


# Custom class to contain reusable classes by other classes
class PageFactory:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 2)
        self.actions = ActionChains(self.driver)

    def get_element(self, locator):
        selector, value = locator
        return self.driver.find_element(selector, value)

    @staticmethod
    def get_element_children(parent, children_locator):
        selector, value = children_locator
        return parent.find_elements(selector, value)

    def click_on_element_using_actions(self, locator):
        element = self.get_element(locator)
        self.actions.move_to_element(element).click(element).perform()

    def type_into_element(self, locator, text):
        self.get_element(locator).clear()
        self.get_element(locator).send_keys(text)

    def get_element_attribute(self, locator, attribute):
        return self.get_element(locator).get_attribute(attribute)

    def get_alert(self):
        return self.wait.until(expected_conditions.alert_is_present())


class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.page_factory = PageFactory(self.driver)

        # Locators
        self.class_attribute_button = (By.LINK_TEXT, "Class Attribute")
        self.click_button = (By.LINK_TEXT, "Click")
        self.dynamic_table_button = (By.LINK_TEXT, "Dynamic Table")
        self.sample_app_button = (By.LINK_TEXT, "Sample App")

    # Methods
    # Return the class of the page navigated to
    def go_to_class_attribute_page(self):
        self.page_factory.get_element(self.class_attribute_button).click()
        return ClassAttributePage(self.driver)

    def go_to_click_page(self):
        self.page_factory.get_element(self.click_button).click()
        return ClickPage(self.driver)

    def go_to_dynamic_table_page(self):
        self.page_factory.get_element(self.dynamic_table_button).click()
        return DynamicTablePage(self.driver)

    def go_to_sample_app_page(self):
        self.page_factory.get_element(self.sample_app_button).click()
        return SampleAppPage(self.driver)


class ClassAttributePage:
    def __init__(self, driver):
        self.driver = driver
        self.page_factory = PageFactory(self.driver)
        # Locators
        self.primary_button = (By.CSS_SELECTOR, ".container .btn-primary")

    # Methods
    def click_on_primary_button(self):
        self.page_factory.get_element(self.primary_button).click()

    def assert_alert_is_present(self):
        try:
            self.page_factory.get_alert()
        except TimeoutException:
            # Raise exception if alert is not present after waiting timeout
            raise NoAlertPresentException

    def get_alert_text(self):
        return self.page_factory.get_alert().text

    def accept_alert(self):
        self.page_factory.get_alert().accept()


class ClickPage:
    def __init__(self, driver):
        self.driver = driver
        self.page_factory = PageFactory(self.driver)
        # locators
        self.bad_button = (By.ID, "badButton")

    # Methods
    def get_bad_button_class_attribute(self):
        return self.page_factory.get_element_attribute(self.bad_button, "class")

    def click_on_bad_button_as_dom_event(self):
        self.driver.execute_script(f"$('#{self.bad_button[1]}').click()")

    def click_on_bad_button_as_physical_mouse(self):
        self.page_factory.click_on_element_using_actions(self.bad_button)


class DynamicTablePage:
    def __init__(self, driver):
        self.driver = driver
        self.page_factory = PageFactory(self.driver)
        # Locators
        self.chrome_cpu_label = (By.CLASS_NAME, "bg-warning")
        self.dynamic_table = (By.CSS_SELECTOR, "[role='table'][aria-label='Tasks']")
        self.table_row_groups = (By.CSS_SELECTOR, "[role='rowgroup']")
        self.table_headers_columns = (By.CSS_SELECTOR, "[role='columnheader']")
        self.table_cells_rows = (By.CSS_SELECTOR, "[role='row']")
        self.table_cells = (By.CSS_SELECTOR, "[role='cell']")

    # Methods
    def get_chrome_cpu_value_from_label(self):
        chrome_cpu_label_text = self.page_factory.get_element(self.chrome_cpu_label).text
        # Convert text from -> Chrome Cpu: *value*, to -> *value*
        return chrome_cpu_label_text.split(":")[1].strip()

    def get_chrome_cpu_value_from_table(self):
        dynamic_table = self.page_factory.get_element(self.dynamic_table)
        table_row_groups = self.page_factory.get_element_children(
            dynamic_table, self.table_row_groups)
        # Split row groups array from the table
        table_headers_row_group = table_row_groups[0]
        table_cells_row_group = table_row_groups[1]

        table_headers_columns = self.page_factory.get_element_children(
            table_headers_row_group, self.table_headers_columns)
        table_cells_rows = self.page_factory.get_element_children(
            table_cells_row_group, self.table_cells_rows)
        # Loop over the dynamic table headers to get the index of CPU header
        cpu_column_index = [i for i, column in enumerate(table_headers_columns) if column.text == "CPU"][0]
        chrome_cpu_table_value = ""
        # Loop to get Chrome row then get it's CPU column value
        for row in table_cells_rows:
            cells = self.page_factory.get_element_children(row, self.table_cells)
            name_cell = cells[0]
            if name_cell.text == "Chrome":
                chrome_cpu_table_value = cells[cpu_column_index].text.strip()
        return chrome_cpu_table_value


class SampleAppPage:
    def __init__(self, driver):
        self.driver = driver
        self.page_factory = PageFactory(self.driver)
        # Locators
        self.login_status_label = (By.ID, "loginstatus")
        self.login_button = (By.ID, "login")
        self.user_name_field = (By.CSS_SELECTOR, "input[name='UserName']")
        self.password_field = (By.CSS_SELECTOR, "input[name='Password']")

    # Methods
    def get_login_status_label_text(self):
        return self.page_factory.get_element(self.login_status_label).text.strip()

    def get_login_button_text(self):
        return self.page_factory.get_element(self.login_button).text

    def click_login_button(self):
        self.page_factory.get_element(self.login_button).click()

    def click_logout_button(self):
        self.page_factory.get_element(self.login_button).click()

    def type_user_name_and_password(self, username, password):
        self.page_factory.type_into_element(self.user_name_field, username)
        self.page_factory.type_into_element(self.password_field, password)
