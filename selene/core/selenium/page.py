import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from selene.core.page import *
from selene.core.config import *
from selene.core.selenium.tasks import *
from selene.core.selenium.driver import *
from selene.core.selenium.scripts import *
from selene.core.selenium.element import *
from selene.core.selenium.conditions import *

from selene.core.soup.page import PageSoup


class PageSelene(Page):
    """
    A page class to assist any workflow which requires selenium webdriver.

    - A website is made out of pages.
    - Dynamically-generated pages require Selenium Webdriver.
    - Each page will need general functionality (e.g. finding and element, scrolling etc.).
    - Inheriting this class provides that general functionality

    NOTE 1: Generally, the way to use this object is to initalise using the from_url() method,
    as this will attach the url to the page AND navigate to the url.

    NOTE 2: Any PageSelene object will also contain a PageSoup object (see core.soup.page).
    This is an attempt to allow both the use of Selenium (for dynamic elements)
    and BeautifulSoup (for static elements) when scraping.

    Inherits selene.core.page.Page
    """

    def __init__(self, driver, url, logger=None, *args, **kwargs):
        """
        Initialise a PageSelene instance.

        Parameters
        ----------
            driver : selenium.webdriver
                the initialised webdriver instance
            url : str
                the url of the page
            logger : logging.Logger
                a logger instance (see core.logger.py)
        """
        Page.__init__(self, url, logger, *args, **kwargs)
        # Get the PageSoup object
        self.page_soup = self.get_page_soup(driver)

    @classmethod
    def from_url(cls, driver, url, string="", logger=None, *args, **kwargs):
        """
        Initialise a PageSelene instance and navigate to the instance's specified url

        Checking the correct url can be done in 2 ways:
            1. Checking for an exact match
            2. Checking whether the url contains a specified string.

        Parameters
        ----------
            driver : selenium.webdriver
                the initialised webdriver instance
            url : str
                the url of the page
            string : str
                a specified string for the new url to contain
            logger : logging.Logger
                a logger instance (see core.logger.py)
        """
        if logger:
            logger.debug(f"navigate to: {url}")
        task_navigate_to_url(driver, url, string=string, wait=WAIT_NORMAL, logger=logger)
        return cls(driver, url, logger, *args, **kwargs)

    @classmethod
    def new_tab(cls, driver, url, string="", logger=None):
        """
        Initialise a PageSelene instance and navigate to the instance's specified url in a new tab

        Checking the correct url can be done in 2 ways:
            1. Checking for an exact match
            2. Checking whether the url contains a specified string.

        Parameters
        ----------
            driver : selenium.webdriver
                the initialised webdriver instance
            url : str
                the url of the page
            string : str
                a specified string for the new url to contain
            logger : logging.Logger
                a logger instance (see core.logger.py)
        """
        if logger:
            logger.debug(f"navigate to: {url} in new tab")
        task_navigate_to_url_in_new_tab(
            driver, url, string=string, wait=WAIT_NORMAL, logger=logger
        )
        return cls.from_url(driver=driver, url=url, string=string, logger=None)

    def get_page_soup(self, driver):
        """
        Get a PageSoup object (see core.soup.page) with the current source html code
        as found by the webdriver instance.

        Parameters
        ----------
            driver : selenium.webdriver
                the initialised webdriver instance

        Returns
        ----------
            output : PageSoup
                PageSoup object initialised using the page's source html code.
        """
        return PageSoup.from_html(self.url, driver.page_source, self.logger)

    def refresh(self, driver, wait=0):
        """
        Refresh the page by refreshing the driver and re-initialising the PageSelene object.

        Parameters
        ----------
            driver : selenium.webdriver
                the initialised webdriver instance
            wait : int
                a number of seconds to wait before re-initialising

        Returns
        ----------
            output : PageSelene
                re-initialised PageSelene object
        """
        self.log(f"refreshing driver: {self.url}")
        driver.refresh()
        self.log(f"waiting {wait} seconds")
        time.sleep(wait)
        return self.from_url(driver, self.url, logger=self.logger)

    def refresh_until_true(self, driver, func, message, attempts, *args, **kwargs):
        """
        This wraps other functions such as self.find.

        If the wrapped function returns anything other than False or None, then this function returns True.

        If the wrapped function returns False or None,
        then this function calls self.refresh. It does so for a number of attempts. If all attempts fail,
        then this function returns False

        This becomes useful if a web page did not load properly, and therefore needs to be refreshed.

        Parameters
        ----------
            driver : selenium.webdriver
                the initialised webdriver instance
            func : function
                the function to be wrapped
            message : str
                the error message to print to the logs
            attempts : int
                the number of attempts before returning False

        Returns
        ----------
            output : bool
                False if the function fails a specified number of times; True if it succeeds
        """
        kwargs["driver"] = driver
        for attempt in range(attempts):
            if func(*args, **kwargs):
                self.log(f"function {func.__name__} succeeded; returning True")
                return True
            self.log(f"{message}: {self.url}", "EXCEPTION")
            self.screenshot_to_notebook(driver)
            if attempt < attempts:
                self.log(f"attempting refresh: attempts: {attempt+1}")
                self.refresh(driver, wait=(attempt + 1) * 30)
            else:
                self.log(f"function {func.__name__} failed; returning False", "EXCEPTION")
                return False

    def navigate_to_url(
        self,
        driver,
        url,
        string="",
        wait=WAIT_NORMAL,
    ):
        """
        This wraps core.selenium.tasks.task_navigate_to_url

        Parameters
        ----------
            driver : selenium.webdriver
                a selenium webdriver instance
            url : str
                the url to navigate to
            string : str
                a specified string for the new url to contain
            wait : int
                a number of seconds to wait before raising a TimeoutException

        Returns
        ----------
            output : bool
                True if the operation was successful, False otherwise
        """
        self.log(f'navigate_to_url: {"; ".join([url, string])}')
        task_navigate_to_url(driver, url, string, wait, logger=self.logger)

    def find(self, driver, by, identifier, wait=WAIT_NORMAL, log=True):
        """
        This:
            - wraps core.selenium.tasks.task_find
            - returns the result, not as a selenium.webdriver.remote.webelement.WebElement object,
            but instead as a core.selenium.element.ElementSelene wrapper object, which gives added functionality.

        Parameters
        ----------
            driver : selenium.webdriver
                a selenium webdriver instance
            by : selenium.webdriver.common.by.By
                see https://selenium-python.readthedocs.io/locating-elements.html
            identifier : str
                see https://selenium-python.readthedocs.io/locating-elements.html
            wait : int
                a number of seconds to wait before raising a TimeoutException

        Returns
        ----------
            output : None or core.selenium.element.ElementSelene
                returns the element if an element is found, None otherwise
        """
        logger = self.logger if log else None
        element = task_find(driver, by, identifier, wait=wait, logger=logger)
        if element is not None:
            try:
                return ElementSelene(element, logger)
            except StaleElementReferenceException as e:
                self.log(f"{e}", "EXCEPTION")
                return self.find(driver, by, identifier, wait, log)
        return None

    def find_all(self, driver, by, identifier, wait=WAIT_NORMAL, log=True):
        """
        This:
            - wraps core.selenium.tasks.task_find_all
            - returns the result, not as a list of selenium.webdriver.remote.webelement.WebElement objects,
            but instead as a list of core.selenium.element.ElementSelene wrapper objects, which gives added functionality.

        Parameters
        ----------
            driver : selenium.webdriver
                a selenium webdriver instance
            by : selenium.webdriver.common.by.By
                see https://selenium-python.readthedocs.io/locating-elements.html
            identifier : str
                see https://selenium-python.readthedocs.io/locating-elements.html
            wait : int
                a number of seconds to wait before raising a TimeoutException

        Returns
        ----------
            output : list
                returns the elements if one or more element is found, an empty list otherwise
        """
        logger = self.logger if log else None
        elements = task_find_all(driver, by, identifier, wait=wait, logger=logger)
        try:
            elements = [ElementSelene(el, logger) for el in elements]
        except StaleElementReferenceException as e:
            self.log(f"{e}", "EXCEPTION")
            return self.find_all(driver, by, identifier, wait, log)
        return elements

    def find_soup(self, *args, **kwargs):
        """
        Each PageSelene object contains a PageSoup object.
        This wraps the core.soup.page.PageSoup.find function, so it
        can use BeautifulSoup to find elements.

        Returns
        ----------
            output : core.soup.element.ElementSoup
                the ElementSoup instance relating to the found webelement
        """
        return self.page_soup.find(*args, **kwargs)

    def find_all_soup(self, *args, **kwargs):
        """
        Each PageSelene object contains a PageSoup object.
        This wraps the core.soup.page.PageSoup.find_all function, so it
        can use BeautifulSoup to find elements.

        Returns
        ----------
            output : list
                the list of ElementSoup instances relating to the found webelements
        """
        return self.page_soup.find_all(*args, **kwargs)

    def click(self, driver, by, identifier, wait=WAIT_NORMAL):
        """
        Find and click an element on the page.

        Parameters
        ----------
            driver : selenium.webdriver
                a selenium webdriver instance
            by : selenium.webdriver.common.by.By
                see https://selenium-python.readthedocs.io/locating-elements.html
            identifier : str
                see https://selenium-python.readthedocs.io/locating-elements.html
            wait : int
                a number of seconds to wait before raising a TimeoutException

        Returns
        ----------
            output : bool
                True if the operation was successful, False otherwise
        """
        if not bool_clickable(driver, by, identifier, wait=wait, logger=self.logger):
            return False
        element = self.find(driver, by, identifier, wait=wait)
        return element.click(driver)

    def scroll_down(self, driver, wait=WAIT_NORMAL):
        """
        Scroll down the page.

        Parameters
        ----------
            driver : selenium.webdriver
                a selenium webdriver instance
            wait : int
                a number of seconds to wait before raising a TimeoutException

        Returns
        ----------
            output : bool
                True if the operation was successful, False otherwise
        """
        self.log(f"scroll_down")
        height_window = driver.get_window_size()["height"]
        height = script_get_scroll_height(driver)
        position = script_get_scroll_position(driver)
        position_new = position + int(0.5 * height_window)
        position_new = min(position_new, height)
        script_scroll_to(driver, position_new)
        return bool_yoffset_changed(driver, wait, self.logger, position)

    def scroll_to(self, driver, position_new, wait=WAIT_NORMAL):
        """
        Scroll to a new position on the page.

        Parameters
        ----------
            driver : selenium.webdriver
                a selenium webdriver instance
            position_new : int
                y position in pixels
            wait : int
                a number of seconds to wait before raising a TimeoutException

        Returns
        ----------
            output : bool
                True if the operation was successful, False otherwise
        """
        self.log(f"scroll_to")
        position = script_get_scroll_position(driver)
        script_scroll_to(driver, position_new)
        return bool_yoffset_changed(driver, wait, self.logger, position)

    def scroll_to_bottom(self, driver, wait=WAIT_NORMAL):
        """
        Scroll to the bottom of the page.

        Parameters
        ----------
            driver : selenium.webdriver
                a selenium webdriver instance
            wait : int
                a number of seconds to wait before raising a TimeoutException

        Returns
        ----------
            output : bool
                True if the operation was successful, False otherwise
        """
        self.log(f"scroll_to_bottom")
        position = script_get_scroll_position(driver)
        height = script_get_scroll_height(driver)
        script_scroll_to(driver, height)
        return bool_yoffset_changed(driver, wait, self.logger, position)

    def expand_scroll_height(self, driver, wait=WAIT_SMALL):
        """
        Keep scrolling to the bottom of the page, as the page dynamically
        expands due to the continued scrolling.

        Parameters
        ----------
            driver : selenium.webdriver
                a selenium webdriver instance
            wait : int
                a number of seconds to wait before raising a TimeoutException

        Returns
        ----------
            output : bool
                True if the operation was successful, False otherwise
        """
        self.log(f"expand_scroll_height")
        while True:
            height = script_get_scroll_height(driver)
            script_scroll_to(driver, height)
            if not bool_scroll_height_changed(driver, wait, self.logger, height):
                return

    @staticmethod
    def screenshot_to_notebook(driver, width=600, height=400, logger=None):
        """
        This wraps core.selenium.tasks.task_screenshot_to_notebook

        Display a browser screenshot in a Jupyter notebook.

        Parameters
        ----------
            driver : selenium.webdriver
                a selenium webdriver instance
            width : int
                the width of the image
            height : int
                the height of the image
            logger : logging.Logger
                a logger instance (see core.logger.py)
        """
        task_screenshot_to_notebook(driver, width=width, height=height, logger=logger)

    @staticmethod
    def screenshot_to_local(driver, dirpath, filestem, logger=None):
        """
        This wraps core.selenium.tasks.screenshot_to_local

        Save a browser screenshot to a local directory

        Parameters
        ----------
            driver : selenium.webdriver
                a selenium webdriver instance
            dirpath : str
                directory to save file
            filestem : str
                a string to add to a datetime to create the filename
            logger : logging.Logger
                a logger instance (see core.logger.py)
        """
        task_screenshot_to_local(driver, dirpath, filestem, logger=logger)

    @staticmethod
    def close_all_tabs_except_specified_tab(driver, handle_keep, attempts=3):
        """
        Closes all open tabs EXCEPT for the tab given by the specified handle.

        Useful for cleanup of any open tabs.

        It has an attempts variable, in case it doesn't work first time.

        Parameters
        ----------
            driver : selenium.webdriver
                a selenium webdriver instance
            handle_keep : str
                the tab/handle to not close.
            attempts : int
                a number of attempts before returning False

        Returns
        ----------
            output : bool
                True if the operation was successful, False otherwise
        """
        if attempts == 0:
            return False
        elif handle_keep not in driver.window_handles:
            return False
        for handle in driver.window_handles:
            if handle != handle_keep:
                driver.switch_to.window(handle)
                driver.close()
                driver.switch_to.window(handle_keep)

        if (
            len(driver.window_handles) == 1
            and driver.current_window_handle == handle_keep
        ):
            return True
        return close_all_tabs_except_current_tab(
            driver, handle_keep, attempts=attempts - 1
        )
