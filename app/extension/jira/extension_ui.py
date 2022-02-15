import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login
from util.conf import JIRA_SETTINGS


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_issues']:
        issue_id = datasets['custom_issue_id']
    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out action
    #
    # @print_timing("selenium_app_specific_user_login")
    # def measure():
    #     def app_specific_user_login(username='admin', password='admin'):
    #         login_page = Login(webdriver)
    #         login_page.delete_all_cookies()
    #         login_page.go_to()
    #         login_page.set_credentials(username=username, password=password)
    #         if login_page.is_first_login():
    #             login_page.first_login_setup()
    #         if login_page.is_first_login_second_page():
    #             login_page.first_login_second_page_setup()
    #         login_page.wait_for_page_loaded()
    #     app_specific_user_login(username='admin', password='admin')
    # measure()

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:edit_issue")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/EditIssue!default.jspa?id={issue_id}")
            page.wait_until_visible((By.ID, "summary-val"))  # Wait for summary field visible
            page.wait_until_visible((By.ID, "aac-customfield_10202"))  # Wait for your app-specific UI element by ID selector
        sub_measure()
    measure()

def app_specific_action2(webdriver, datasets):
    page = BasePage(webdriver)
    
    @print_timing("selenium_app_custom_action2")
    def measure():
        @print_timing("selenium_app_custom_action:view_admin")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/plugins/servlet/fancyfields/admin")
            page.wait_until_visible((By.ID, "apikey"))  # Wait for ui element
            page.wait_until_visible((By.ID, "addresstypes"))  # Wait for ui element
        sub_measure()
    measure()
