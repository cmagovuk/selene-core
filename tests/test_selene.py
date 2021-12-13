# conda install -c anaconda pytest
# conda install -c conda-forge selenium
import sys
import os
import pytest
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from selene import selene
from selene import logger as logging

class TestLogger:
    
    def test_fail_no_path(self, tmpdir):
        logdir_path = ""
        logfile_name = ""
        with pytest.raises(FileNotFoundError):
            logging.start_logger(logdir_path, logfile_name=logfile_name)
        
    def test_success_create_default_name(self, tmpdir):
        logdir_path = tmpdir
        logfile_name = ""
        logger = logging.start_logger(logdir_path, logfile_name=logfile_name)
        assert os.path.exists(tmpdir + "/log.log")
        
    def test_success_create_choose_name(self, tmpdir):
        logdir_path = tmpdir
        logfile_name = "test.log"
        logger = logging.start_logger(logdir_path, logfile_name=logfile_name)
        assert os.path.exists("{}/{}".format(tmpdir, logfile_name))

class TestSeleniumHelperBasic:
    
    def make_class_success(self, tmpdir):
        # Make sure the SeleniumHelper instance is created with no errors
        webdriver_path = selene.WEBDRIVER_PATH
        logdir_path = tmpdir
        screenshots_path = tmpdir
        selenium_helper = selene.SeleniumHelper(webdriver_path=webdriver_path, logdir_path=logdir_path, screenshots_path=screenshots_path)
        return selenium_helper

class TestSeleniumHelperInitialise(TestSeleniumHelperBasic):
    
    def make_class_wrong_webdriver_path(self, tmpdir):
        # Make sure the wrong webdriver path raises error
        webdriver_path = ""
        logdir_path = tmpdir
        screenshots_path = tmpdir
        selenium_helper = selene.SeleniumHelper(webdriver_path=webdriver_path, logdir_path=logdir_path, screenshots_path=screenshots_path)
        
    def make_class_wrong_logdir_path(self, tmpdir):
        # Make sure the wrong logs directory path raises error    
        webdriver_path = selene.WEBDRIVER_PATH
        logdir_path = ""
        screenshots_path = tmpdir
        selenium_helper = selene.SeleniumHelper(webdriver_path=webdriver_path, logdir_path=logdir_path, screenshots_path=screenshots_path)
            
    def make_class_wrong_screenshots_path(self, tmpdir):
        # Make sure the wrong screenshots directory path raises error
        webdriver_path = selene.WEBDRIVER_PATH
        logdir_path = tmpdir
        screenshots_path = ""
        selenium_helper = selene.SeleniumHelper(webdriver_path=webdriver_path, logdir_path=logdir_path, screenshots_path=screenshots_path)
    
    def test_make_class_instance(self, tmpdir):
        
        with pytest.raises(FileNotFoundError):
            self.make_class_wrong_webdriver_path(tmpdir)
        
        with pytest.raises(FileNotFoundError):
            self.make_class_wrong_logdir_path(tmpdir)
        
        with pytest.raises(FileNotFoundError):
            self.make_class_wrong_screenshots_path(tmpdir)

        selenium_helper = self.make_class_success(tmpdir)
        assert selenium_helper
        assert selenium_helper.webdriver_path == selene.WEBDRIVER_PATH
        assert selenium_helper.logdir_path == tmpdir
        assert selenium_helper.screenshots_path == tmpdir
        
    def test_success_initialise_and_stop_webdriver(self, tmpdir):
        
        selenium_helper = self.make_class_success(tmpdir)
        
        # Initialise webdriver
        assert selenium_helper.initialise_webdriver()
        
        # Check the logs
        logfile_path = "{}/{}".format(tmpdir, "selenium.log")
        assert os.path.exists(logfile_path)
        with open(logfile_path, "r") as logfile:
            log_text = logfile.read()
        assert "Driver started at" in log_text
        
        # Make sure the driver is there
        assert selenium_helper.get_driver()
        
        # Stop the driver
        assert selenium_helper.stop_webdriver()
        
        # Check the logs
        with open(logfile_path, "r") as logfile:
            log_text = logfile.read()
        assert "Driver stopped at" in log_text

class TestSeleniumHelperNavigate(TestSeleniumHelperBasic):
    
    def test_navigate_to_url(self, tmpdir):
        
        selenium_helper = self.make_class_success(tmpdir)
        
        # Initialise webdriver
        assert selenium_helper.initialise_webdriver()
        
        # function returns false if exact_url is false and expected_string is null
        new_url = "https://scrapethissite.com/pages/"
        assert not selenium_helper.navigate_to_url(new_url, exact_url=False)
        
        # function passes if successfully navigated to new page
        new_url = "https://scrapethissite.com/pages/simple/"
        assert selenium_helper.navigate_to_url(new_url, exact_url=True)
        
        # function raises assertion error if exact_url is true and the new_url does not match
        new_url = "https://bit.ly/2msVL4V"
        expected_string = "scrapethissite.com/pages/"
        with pytest.raises(AssertionError):
            selenium_helper.navigate_to_url(new_url, exact_url=True)
        
        # function raises assertion error if exact_url is false and expected_string not found
        new_url = "https://bit.ly/2mwFuvZ"
        expected_string = "testing_testing"
        with pytest.raises(AssertionError):
            selenium_helper.navigate_to_url(new_url, exact_url=False, expected_string=expected_string)
            
        # function passes if expected_string is found in the final url   
        new_url = "https://bit.ly/2msVL4V"
        expected_string = "scrapethissite.com/pages/"
        assert selenium_helper.navigate_to_url(new_url, exact_url=False, expected_string=expected_string)

        # Stop the driver
        assert selenium_helper.stop_webdriver()

class TestSeleniumHelperFindElements(TestSeleniumHelperBasic):
    
    def find_element_on_page(self, selenium_helper):
        element = selenium_helper.find_element(By.CLASS_NAME, "glyphicon-education")
        return element
    
    def find_child_within_parent(self, selenium_helper):
        parent = selenium_helper.find_element(By.ID, "footer")
        child = selenium_helper.find_child(parent, By.CLASS_NAME, "container")
        return child
    
    def element_does_not_exist_on_page(self, selenium_helper):
        element = selenium_helper.find_element(By.CLASS_NAME, "not_exist")
        return element
    
    def child_does_not_exist_within_parent(self, selenium_helper):
        parent = selenium_helper.find_element(By.CLASS_NAME, "glyphicon-education")
        child = selenium_helper.find_child(parent, By.CLASS_NAME, "container")
        return child
    
    def find_elements_on_page(self, selenium_helper):
        elements = selenium_helper.find_elements(By.CLASS_NAME, "team")
        return len(elements) > 0
    
    def find_children_within_parent(self, selenium_helper):
        parent = selenium_helper.find_element(By.CLASS_NAME, "table")
        children = selenium_helper.find_children(parent, By.CLASS_NAME, "year")
        return len(children) > 0
    
    def no_elements_exist_on_page(self, selenium_helper):
        elements = selenium_helper.find_elements(By.CLASS_NAME, "not_exist")
        return elements
    
    def no_elements_exist_within_parent(self, selenium_helper):
        parent = selenium_helper.find_element(By.CLASS_NAME, "glyphicon-education")
        children = selenium_helper.find_children(parent, By.CLASS_NAME, "team")
        return children
        
    def test_finding_elements(self, tmpdir):
        
        selenium_helper = self.make_class_success(tmpdir)
        
        # Initialise webdriver
        assert selenium_helper.initialise_webdriver()
        
        # function passes if successfully navigated to new page
        new_url = "https://scrapethissite.com/pages/forms/"
        assert selenium_helper.navigate_to_url(new_url, exact_url=True)
        
        assert self.find_element_on_page(selenium_helper)
        
        assert self.find_child_within_parent(selenium_helper)
        
        assert self.element_does_not_exist_on_page(selenium_helper) is None
        
        assert self.child_does_not_exist_within_parent(selenium_helper) is None
        
        assert self.find_elements_on_page(selenium_helper)
        
        assert self.find_children_within_parent(selenium_helper)
        
        assert self.no_elements_exist_on_page(selenium_helper) is None
        
        assert self.no_elements_exist_within_parent(selenium_helper) is None
        
        # Stop the driver
        assert selenium_helper.stop_webdriver()

class TestSeleniumHelperElementPosition(TestSeleniumHelperBasic):
    
    def find_element_on_visible_page(self, selenium_helper):
        element = selenium_helper.find_element(By.CLASS_NAME, "firstHeading")
        return element
    
    def element_off_page_still_displayed(self, selenium_helper):
        return selenium_helper.wait_until_displayed(By.CLASS_NAME, "reflist")
    
    def find_element_off_visible_page(self, selenium_helper):
        element = selenium_helper.find_element(By.CLASS_NAME, "reflist")
        return element
    
    def test_location_of_elements(self, tmpdir):
        
        selenium_helper = self.make_class_success(tmpdir)
        
        # Initialise webdriver
        assert selenium_helper.initialise_webdriver()
        
        # function passes if successfully navigated to new page
        new_url = "https://en.wikipedia.org/wiki/Alan_Turing"
        assert selenium_helper.navigate_to_url(new_url, exact_url=True)
        
        # Make sure an obviously visible element is visible without scrolling
        assert selenium_helper.is_element_displayed_on_page_without_scrolling(By.CLASS_NAME, "firstHeading")
        
        # Make sure an obviously not visible element exists
        assert self.element_off_page_still_displayed(selenium_helper)
        element = self.find_element_off_visible_page(selenium_helper)
        assert element is not None
        
        # Make sure an obviously not visible element is not visible without scrolling
        assert not selenium_helper.is_element_displayed_on_page_without_scrolling(By.CLASS_NAME, "reflist")
