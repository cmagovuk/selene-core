from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

from selene.core.config import *
from selene.core.selenium.scripts import *


def bool_url_changed(driver, wait, logger, url, message="URL has not changed."):
    """
    Wait a specified number of seconds until either:
        - The browser's url changes.
        - A TimeoutException is raised

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        wait : int
            a number of seconds to wait before raising a TimeoutException
        logger : logging.Logger
            a logger instance (see core.logger.py)
        url : str
            the original url
        message : str
            log message (default: "URL has not changed.")

    Returns
    ----------
        output : bool
            True if the url changes, False otherwise
    """
    if logger:
        logger.debug(f"bool_url_changed: {url}")
    try:
        WebDriverWait(driver, wait).until(method=EC.url_changes(url), message=message)
        return True
    except TimeoutException as e:
        if logger:
            logger.exception(e)
        return False


def bool_url_expected(driver, wait, logger, url, message="URL is not the expected URL."):
    """
    Wait a specified number of seconds until either:
        - The browser's url matches the expected url.
        - A TimeoutException is raised

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        wait : int
            a number of seconds to wait before raising a TimeoutException
        logger : logging.Logger
            a logger instance (see core.logger.py)
        url : str
            the expected url
        message : str
            log message (default: "URL is not the expected URL.")

    Returns
    ----------
        output : bool
            True if the url is the expected url, False otherwise
    """
    if logger:
        logger.debug(f"bool_url_expected: {url}")
    try:
        WebDriverWait(driver, wait).until(method=EC.url_to_be(url), message=message)
        return True
    except TimeoutException as e:
        if logger:
            logger.exception(f"{e}; {driver.current_url}")
        return False


def bool_url_unexpected(driver, wait, logger, url, message="URL is the unexpected URL."):
    """
    Wait a specified number of seconds until either:
        - The browser's url matches the UNexpected url.
        - A TimeoutException is raised

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        wait : int
            a number of seconds to wait before raising a TimeoutException
        logger : logging.Logger
            a logger instance (see core.logger.py)
        url : str
            the unexpected url
        message : str
            log message (default: "URL is the unexpected URL.")

    Returns
    ----------
        output : bool
            True if the url is the unexpected url, False otherwise
    """
    if logger:
        logger.debug(f"bool_url_unexpected: {url}")
    try:
        WebDriverWait(driver, wait).until_not(method=EC.url_to_be(url), message=message)
        return True
    except TimeoutException as e:
        if logger:
            logger.exception(f"{e}; {driver.current_url}")
        return False


def bool_url_contains(
    driver,
    wait,
    logger,
    string,
    message="URL does not contain the specified string.",
):
    """
    Wait a specified number of seconds until either:
        - The browser's url contains a specified string.
        - A TimeoutException is raised

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        wait : int
            a number of seconds to wait before raising a TimeoutException
        logger : logging.Logger
            a logger instance (see core.logger.py)
        message : str
            log message (default: "URL does not contain the specified string.")

    Returns
    ----------
        output : bool
            True if the url contains the specified string, False otherwise
    """
    if logger:
        logger.debug(f"bool_url_contains: {string}")
    if string == "":
        return False
    try:
        WebDriverWait(driver, wait).until(method=EC.url_contains(string), message=message)
        return True
    except TimeoutException as e:
        if logger:
            logger.exception(f"{e}; {driver.current_url}")
        return False


def bool_url_does_not_contain(
    driver, wait, logger, string, message="URL contains the specified string."
):
    """
    Wait a specified number of seconds until either:
        - The browser's url DOES NOT contain a specified string.
        - A TimeoutException is raised

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        wait : int
            a number of seconds to wait before raising a TimeoutException
        logger : logging.Logger
            a logger instance (see core.logger.py)
        message : str
            log message (default: "URL contains the specified string.")

    Returns
    ----------
        output : bool
            True if the url does not contain the specified string, False otherwise
    """
    if logger:
        logger.debug(f'bool_url_does_not_contain: {"; ".join([url, string])}')
    if string == "":
        return False
    try:
        WebDriverWait(driver, wait).until_not(
            method=EC.url_contains(string), message=message
        )
        return True
    except TimeoutException as e:
        if logger:
            logger.exception(f"{e}; {driver.current_url}")
        return False


def bool_visible(driver, by, identifier, wait=WAIT_NORMAL, logger=None):
    """
    Wait a specified number of seconds until either:
        - A found element is visible
        - A TimeoutException is raised

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
            True if the element is visible, False otherwise
    """
    if logger:
        logger.debug(f"bool_visible: {identifier}")
    try:
        WebDriverWait(driver, wait).until(
            EC.visibility_of_element_located((by, identifier)),
            message=f"Element not visible: {identifier}.",
        )
        return True
    except TimeoutException as e:
        if logger:
            logger.exception(e)
        return False


def bool_invisible(driver, by, identifier, wait=WAIT_NORMAL, logger=None):
    """
    Wait a specified number of seconds until either:
        - A found element is NOT visible
        - A TimeoutException is raised

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
            True if the element is invisible, False otherwise
    """
    if logger:
        logger.debug(f"bool_invisible: {identifier}")
    try:
        WebDriverWait(driver, wait).until(
            EC.invisibility_of_element((by, identifier)),
            message=f"Element visible: {identifier}.",
        )
        return True
    except TimeoutException as e:
        if logger:
            logger.exception(e)
        return False


def bool_clickable(driver, by, identifier, wait=WAIT_NORMAL, logger=None):
    """
    Wait a specified number of seconds until either:
        - A found element is clickable
        - A TimeoutException is raised

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
            True if the element is clickable, False otherwise
    """
    if logger:
        logger.debug(f"bool_clickable: {identifier}")
    try:
        WebDriverWait(driver, wait).until(
            EC.element_to_be_clickable((by, identifier)),
            message=f"Element not clickable: {identifier}",
        )
        return True
    except TimeoutException as e:
        if logger:
            logger.exception(e)
        return False


def bool_yoffset_changed(
    driver, wait, logger, yoffset, message="Y-offset did not change."
):
    """
    Wait a specified number of seconds until either:
        - The y-offset changes. This is what changes as you scroll down a page
        - A TimeoutException is raised

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        wait : int
            a number of seconds to wait before raising a TimeoutException
        logger : logging.Logger
            a logger instance (see core.logger.py)
        yoffset : float
            the original y-offset value
        message : str
            log message (default: "Y-offset did not change.")

    Returns
    ----------
        output : bool
            True if the y-offset has changed, False otherwise
    """
    if logger:
        logger.debug(f"bool_yoffset_changed: {yoffset}")
    try:
        WebDriverWait(driver, wait).until(
            method=lambda wd: yoffset
            != driver.execute_script("return window.pageYOffset"),
            message=message,
        )
        return True
    except TimeoutException as e:
        if logger:
            logger.exception(e)
        return False


def bool_scroll_position_changed(
    driver, element, wait, logger, position, message="Scroll position did not change."
):
    """
    Wait a specified number of seconds until either:
        - An element's scroll position changes. This is what changes
          as you scroll down a scrollable element.
        - A TimeoutException is raised

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        element : EITHER selenium.webdriver.remote.webelement.WebElement OR core.selenium.element.Element
            the scrollable element
        wait : int
            a number of seconds to wait before raising a TimeoutException
        logger : logging.Logger
            a logger instance (see core.logger.py)
        position : float
            the original scroll position value
        message : str
            log message (default: "Scroll position did not change.")

    Returns
    ----------
        output : bool
            True if the element's scroll position has changed, False otherwise
    """
    if logger:
        logger.debug(f"bool_scroll_position_changed: {position}")
    try:
        WebDriverWait(driver, wait).until(
            method=lambda wd: position != script_get_scroll_position(driver, element),
            message=message,
        )
        return True
    except TimeoutException as e:
        if logger:
            logger.exception(e)
        return False


def bool_scroll_height_changed(
    driver, wait, logger, height, element=None, message="Scroll height did not change."
):
    """
    Wait a specified number of seconds until either:
        - The page OR an element's scroll height changes. This is what changes
          if the height of the page or element increases due to dynamically-generated content.
        - A TimeoutException is raised

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        wait : int
            a number of seconds to wait before raising a TimeoutException
        logger : logging.Logger
            a logger instance (see core.logger.py)
        height : float
            the original scroll height value
        element : EITHER selenium.webdriver.remote.webelement.WebElement OR core.selenium.element.Element OR None
            the scrollable element. If None, then the page itself is the element.
        message : str
            log message (default: "Scroll height did not change.")

    Returns
    ----------
        output : bool
            True if the scroll height has changed, False otherwise
    """
    if logger:
        logger.debug(f"bool_scroll_height_changed: {height}")
    try:
        WebDriverWait(driver, wait).until(
            method=lambda wd: height != script_get_scroll_height(driver, element),
            message=message,
        )
        return True
    except TimeoutException as e:
        if logger:
            logger.exception(e)
        return False


def bool_element_class_contains(
    driver, element, wait, logger, string, message="Element class does not contain"
):
    """
    Wait a specified number of seconds until either:
        - An element's class contains a specified string
        - A TimeoutException is raised

    This is useful for cases where, for example, a dropdown element's class contains "expanded"
    only if and when the dropdown has been expanded.

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        element : core.selenium.element.Element
            the instance of the Element class representing the web element
        wait : int
            a number of seconds to wait before raising a TimeoutException
        logger : logging.Logger
            a logger instance (see core.logger.py)
        string : str
            the string to be found
        message : str
            log message (default: "Element class does not contain {string}")

    Returns
    ----------
        output : bool
            True if the element's class contains the string, False otherwise
    """
    if logger:
        logger.debug(f"bool_element_class_contains: {string}")
    try:
        WebDriverWait(driver, wait).until(
            method=lambda wd: string in element.get_attribute("class"),
            message=f"{message} {string}.",
        )
        return True
    except TimeoutException as e:
        if logger:
            logger.exception(e)
        return False


def bool_element_class_does_not_contain(
    driver, element, wait, logger, string, message="Element class contains"
):
    """
    Wait a specified number of seconds until either:
        - An element's text contains a specified string
        - A TimeoutException is raised

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        element : core.selenium.element.Element
            the instance of the Element class representing the web element
        wait : int
            a number of seconds to wait before raising a TimeoutException
        logger : logging.Logger
            a logger instance (see core.logger.py)
        string : str
            the string to be found
        message : str
            log message (default: "Element class contains {string}.")

    Returns
    ----------
        output : bool
            True if the element's class contains the string, False otherwise
    """
    if logger:
        logger.debug(f"bool_element_class_does_not_contain: {string}")
    try:
        WebDriverWait(driver, wait).until(
            method=lambda wd: string not in element.get_attribute("class"),
            message=f"{message} {string}.",
        )
        return True
    except TimeoutException as e:
        if logger:
            logger.exception(e)
        return False


def bool_element_text_contains(
    driver, element, wait, logger, string, message="Element text does not contain"
):
    """
    Wait a specified number of seconds until either:
        - An element's text contains a specified string
        - A TimeoutException is raised

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        element : core.selenium.element.Element
            the instance of the Element class representing the web element
        wait : int
            a number of seconds to wait before raising a TimeoutException
        logger : logging.Logger
            a logger instance (see core.logger.py)
        string : str
            the string to be found
        message : str
            log message (default: "Element text does not contain {string}.")

    Returns
    ----------
        output : bool
            True if the element's text contains the string, False otherwise
    """
    if logger:
        logger.debug(f"bool_element_text_contains: {string}")
    try:
        WebDriverWait(driver, wait).until(
            method=lambda wd: string in element.text, message=f"{message} {string}."
        )
        return True
    except TimeoutException as e:
        if logger:
            logger.exception(e)
        return False


def bool_element_text_does_not_contain(
    driver, element, wait, logger, string, message="Element text contains"
):
    """
    Wait a specified number of seconds until either:
        - An element's text DOES NOT contain a specified string
        - A TimeoutException is raised

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        element : core.selenium.element.Element
            the instance of the Element class representing the web element
        wait : int
            a number of seconds to wait before raising a TimeoutException
        logger : logging.Logger
            a logger instance (see core.logger.py)
        string : str
            the string to be found
        message : str
            log message (default: "Element text contains {string}.")

    Returns
    ----------
        output : bool
            True if the element's text does not contain the string, False otherwise
    """
    if logger:
        logger.debug(f"bool_element_text_does_not_contain: {string}")
    try:
        WebDriverWait(driver, wait).until(
            method=lambda wd: string not in element.text, message=f"{message} {string}."
        )
        return True
    except TimeoutException as e:
        if logger:
            logger.exception(e)
        return False


def bool_new_handle(driver, n_handles_old, wait, logger, message="No new handles found."):
    """
    Wait a specified number of seconds until either:
        - The number of window handles (i.e. the number of tabs open) has increased by one
        - A TimeoutException is raised

    This is useful when navigating between different tabs.

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        n_handles_old : int
            the previous number of existing window handles
        wait : int
            a number of seconds to wait before raising a TimeoutException
        logger : logging.Logger
            a logger instance (see core.logger.py)
        message : str
            log message (default: "No new handles found.")

    Returns
    ----------
        output : bool
            True if the number of handles has increased by one, False otherwise
    """
    if logger:
        logger.debug(f"bool_new_handle")
    try:
        WebDriverWait(driver, wait).until(
            method=lambda wd: len(driver.window_handles) == n_handles_old + 1,
            message=f"{message}.",
        )
        return True
    except TimeoutException as e:
        if logger:
            logger.exception(e)
        return False


def bool_correct_handle(driver, handle, wait, logger, message="Incorrect handle."):
    """
    Wait a specified number of seconds until either:
        - The active handle i.e. tab) is the expected one
        - A TimeoutException is raised

    This is useful when navigating between different tabs.

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        handle : str
            the expected handle
        wait : int
            a number of seconds to wait before raising a TimeoutException
        logger : logging.Logger
            a logger instance (see core.logger.py)
        message : str
            log message (default: "Incorrect handle.")

    Returns
    ----------
        output : bool
            True if the active handle is the same as the expected handle, False otherwise
    """
    if logger:
        logger.debug(f"bool_correct_handle")
    try:
        WebDriverWait(driver, wait).until(
            method=lambda wd: driver.current_window_handle == handle,
            message=f"{message}.",
        )
        return True
    except TimeoutException as e:
        if logger:
            logger.exception(e)
        return False
