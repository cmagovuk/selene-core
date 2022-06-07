from IPython.display import Image, display
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.action_chains import ActionChains

from selene.core.config import *
from selene.core.selenium.scripts import *
from selene.core.selenium.conditions import *

import random


def task_navigate_to_url(driver, url, string="", wait=WAIT_NORMAL, logger=None):
    """
    Navigate to a new url and check that the url is correct.

    Checking the correct url can be done in 2 ways:
        1. Checking for an exact match
        2. Checking whether the url contains a specified string.

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
        logger : logging.Logger
            a logger instance (see core.logger.py)

    Returns
    ----------
        output : bool
            True if the operation was successful, False otherwise
    """
    if logger:
        logger.debug(f'task_navigate_to_url: {"; ".join([url, string])}')
    # Get the original url
    url_prev = driver.current_url
    # If the original url is the same as the expected url, return True
    if not bool_url_unexpected(driver, WAIT_TINY, logger, url):
        return True
    # Navigate to new url, catching Webdriver failures
    try:
        driver.get(url)
    except WebDriverException as e:
        if logger:
            logger.exception(f"{e}")
        return False
    # Check that the url has changed
    if not bool_url_changed(driver, wait, logger, url_prev):
        return False
    # Check that the url is correct
    if string == "":
        return bool_url_expected(driver, wait, logger, url)
    else:
        return bool_url_contains(driver, wait, logger, string)


def task_navigate_to_url_in_new_tab(
    driver, url, string="", wait=WAIT_NORMAL, logger=None
):
    """
    Navigate to a new url in a new tab, and check that the url is correct.

    Checking the correct url can be done in 2 ways:
        1. Checking for an exact match
        2. Checking whether the url contains a specified string.

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
        logger : logging.Logger
            a logger instance (see core.logger.py)

    Returns
    ----------
        output : bool
            True if the operation was successful, False otherwise
    """
    if logger:
        logger.debug(f'task_navigate_to_url_in_new_tab: {"; ".join([url, string])}')
    # Get the current number of handles
    handles_prev = driver.window_handles
    n_handles_prev = len(handles_prev)
    # Open url in new tab
    try:
        driver.execute_script(f'window.open("{url}");')
    except JavascriptException as e:
        if logger:
            logger.exception(f"{e}")
        return False
    # Check that new handle has been created
    if not bool_new_handle(driver, n_handles_prev, WAIT_SMALL, logger):
        return False
    # Switch to new tab
    handle_new = [x for x in driver.window_handles if x not in handles_prev][0]
    try:
        driver.switch_to.window(handle_new)
    except WebDriverException as e:
        if logger:
            logger.exception(f"{e}")
        return False
    # Check that the current handle is now changed
    if not bool_correct_handle(driver, handle_new, WAIT_SMALL, logger):
        return False
    # Check that the url is corrects
    if string == "":
        return bool_url_expected(driver, wait, logger, url)
    else:
        return bool_url_contains(driver, wait, logger, string)


def task_close_tab_return_to_url_and_handle(
    driver, url, handle, string="", wait=WAIT_NORMAL, logger=None
):
    """
    Close the current tab and check that the driver is back at the expected handle and url.

    Checking the correct url can be done in 2 ways:
        1. Checking for an exact match
        2. Checking whether the url contains a specified string.

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        handle : str
            the handle to navigate to
        url : str
            the url to navigate to
        string : str
            a specified string for the new url to contain
        wait : int
            a number of seconds to wait before raising a TimeoutException
        logger : logging.Logger
            a logger instance (see core.logger.py)

    Returns
    ----------
        output : bool
            True if the operation was successful, False otherwise
    """
    if logger:
        logger.debug(
            f'task_close_tab_return_to_url_and_handle: {"; ".join([url, string])}'
        )
    # Close tab
    try:
        driver.execute_script(f"window.close();")
    except JavascriptException as e:
        if logger:
            logger.exception(f"{e}")
        return False
    # Switch to handle
    try:
        driver.switch_to.window(handle)
    except WebDriverException as e:
        if logger:
            logger.exception(f"{e}")
        return False
    # Check that the handle is the expected one
    if not bool_correct_handle(driver, handle, WAIT_SMALL, logger):
        return False
    # Check that the url is the expected one
    if string == "":
        return bool_url_expected(driver, wait, logger, url)
    else:
        return bool_url_contains(driver, wait, logger, string)


def task_find(parent, by, identifier, wait=WAIT_NORMAL, logger=None):
    """
    Find an element using a By. selector and an identifier.

    For more info, see:
    https://selenium-python.readthedocs.io/locating-elements.html

    If the operation is to find an element on the whole page, then
    the parent variable is a Selenium Webdriver instance (usually named driver).

    If the operation is to find an element on the whole page, then
    the parent variable is a Selenium WebElement instance
    (NOT a core.selenium.element.Element instance).

    Parameters
    ----------
        parent : EITHER selenium.webdriver OR selenium.webdriver.remote.webelement.WebElement
            where to search for the element
        by : selenium.webdriver.common.by.By
            see https://selenium-python.readthedocs.io/locating-elements.html
        identifier : str
            see https://selenium-python.readthedocs.io/locating-elements.html
        wait : int
            a number of seconds to wait before raising a TimeoutException
        logger : logging.Logger
            a logger instance (see core.logger.py)

    Returns
    ----------
        output : [None, selenium.webdriver.remote.webelement.WebElement]
            returns the webelement if it is found; None otherwise
    """
    if logger:
        logger.debug(f"task_find: {identifier}")
    try:
        return WebDriverWait(parent, wait).until(
            EC.presence_of_element_located((by, identifier)),
            message=f"Element not found: {identifier}",
        )
    except TimeoutException as e:
        if logger:
            logger.exception(e)
        return None


def task_find_all(parent, by, identifier, wait=WAIT_NORMAL, logger=None):
    """
    Find a list of elements using a By. selector and an identifier.

    For more info, see:
    https://selenium-python.readthedocs.io/locating-elements.html

    If the operation is to find an element on the whole page, then
    the parent variable is a Selenium Webdriver instance (usually named driver).

    If the operation is to find an element on the whole page, then
    the parent variable is a Selenium WebElement instance
    (NOT a core.selenium.element.Element instance).

    Parameters
    ----------
        parent : EITHER selenium.webdriver OR selenium.webdriver.remote.webelement.WebElement
            where to search for the element
        by : selenium.webdriver.common.by.By
            see https://selenium-python.readthedocs.io/locating-elements.html
        identifier : str
            see https://selenium-python.readthedocs.io/locating-elements.html
        wait : int
            a number of seconds to wait before raising a TimeoutException
        logger : logging.Logger
            a logger instance (see core.logger.py)

    Returns
    ----------
        output : list
            returns a list of webelements if one or more are found; an empty list otherwise
    """
    if logger:
        logger.debug(f"task_find_all: {identifier}")
    try:
        WebDriverWait(parent, wait).until(
            EC.presence_of_element_located((by, identifier)),
            message=f"No elements found: {identifier}",
        )
    except TimeoutException as e:
        if logger:
            logger.exception(e)
        return []
    return parent.find_elements(by, identifier)


def task_click(driver, by, identifier, wait=WAIT_NORMAL, logger=None):
    """
    Click an element using a By. selector and an identifier.

    For more info, see:
    https://selenium-python.readthedocs.io/locating-elements.html

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
        logger : logging.Logger
            a logger instance (see core.logger.py)

    Returns
    ----------
        output : bool
            True if the operation was successful, False otherwise
    """
    if logger:
        logger.debug(f"task_click: {identifier}")
    if not bool_clickable(driver, by, identifier, wait=wait, logger=logger):
        return False
    element = task_find(driver, by, identifier, wait=wait, logger=logger)
    return script_click_element(driver, element)


def task_screenshot_to_notebook(driver, width, height, logger):
    """
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
    if logger:
        logger.debug(f"screenshot_to_notebook")
    image = Image(driver.get_screenshot_as_png(), width=width, height=height)
    display(image)


def task_screenshot_to_local(driver, dirpath, filestem, logger):
    """
    Save a browser screenshot to a local directory

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        dirpath : str
            the directory path
        filestem : str
            a string to add to a datetime to create the filename TODO tidy up workflow?
        logger : logging.Logger
            a logger instance (see core.logger.py)
    """
    if logger:
        logger.debug(f'task_screenshot_to_local: {"; ".join([dirpath, filestem])}')
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    str_datetime = datetime.now().strftime("%Y%m%d%H%M%S%f")
    filename = f"{str_datetime}_{filestem}.png"
    filepath = f"{dirpath}/{filename}"
    driver.save_screenshot(filepath)


def mouse_move(driver, max_mouse_moves=10):
    """performs mouse move, for help with bot mitigation, partially ported from OpenWPM"""

    # bot mitigation: move the mouse randomly around a number of times
    window_size = driver.get_window_size()
    num_moves = 0
    num_fails = 0
    while num_moves < max_mouse_moves and num_fails < max_mouse_moves:
        try:
            if num_moves == 0:  # move to the center of the screen
                x = int(round(window_size["height"] / 2))
                y = int(round(window_size["width"] / 2))
            else:  # move a random amount in some direction
                move_max = random.randint(0, 500)
                x = random.randint(-move_max, move_max)
                y = random.randint(-move_max, move_max)
            action = ActionChains(driver)
            action.move_by_offset(x, y)
            action.perform()
            num_moves += 1
        except:
            num_fails += 1
            pass
    return num_moves
