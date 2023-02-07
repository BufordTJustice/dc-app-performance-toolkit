import random

from selenium.webdriver.common.by import By

from selenium_ui.base_page import BasePage
from selenium_ui.conftest import print_timing
from selenium_ui.jira.pages.pages import Login, Issue
from util.conf import JIRA_SETTINGS


def app_specific_action(webdriver, datasets):
    page = BasePage(webdriver)
    if datasets['custom_issues']:
        issue_id = datasets['custom_issue_id']

    # To run action as specific user uncomment code bellow.
    # NOTE: If app_specific_action is running as specific user, make sure that app_specific_action is running
    # just before test_2_selenium_z_log_out action
    #
    @print_timing("selenium_app_specific_user_login")
    def measure():
        def app_specific_user_login(username='admin', password='admin'):
            login_page = Login(webdriver)
            login_page.delete_all_cookies()
            login_page.go_to()
            login_page.set_credentials(username=username, password=password)
            if login_page.is_first_login():
                login_page.first_login_setup()
            if login_page.is_first_login_second_page():
                login_page.first_login_second_page_setup()
            login_page.wait_for_page_loaded()
        app_specific_user_login(username='admin', password='admin')
    measure()

    @print_timing("selenium_app_custom_action")
    def measure():
        @print_timing("selenium_app_custom_action:custom_edit_issue")
        def sub_measure():
            page.go_to_url(f"{JIRA_SETTINGS.server_url}/secure/EditIssue!default.jspa?id={issue_id}")
            page.wait_until_visible((By.ID, "summary"))  # Wait for summary field visible
            page.wait_until_visible((By.ID, "customfield_11101"))  # Wait for you app-specific UI element by ID selector
        sub_measure()
    measure()


def app_specific_action2(webdriver, datasets):
    issue_page = Issue(webdriver, issue_id=datasets['custom_issue_id'])

    @print_timing("selenium_edit_issue_darin")
    def measure():
        @print_timing("selenium_edit_issue:darin_pen_edit_issue_form")
        def sub_measure():
            issue_page.go_to_edit_issue()  # open editor

        sub_measure()

        @print_timing("selenium_edit_issue:darin_save_edit_issue_form")
        def sub_measure():
            issue_page.edit_issue_submit()  # submit edit issue
            issue_page.wait_for_issue_title()

        sub_measure()        
    measure()
