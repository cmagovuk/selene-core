from selene.core.element import Element
from selene.core.selenium.tasks import *
from selene.core.selenium.scripts import *
from selene.core.selenium.conditions import *


class ElementSelene(Element):
    """
    An element class to wrap a selenium.webdriver.remote.webelement.WebElement object,
    in order to:
        - provide extra functionality
        - make it easier to crawlers to change between handling
        Selenium workflows and BeautifulSoup workflows.

    Inherits selene.core.element.Element
    """

    def __init__(self, element, logger=None):
        """
        Initialise an ElementSelene instance.

        Parameters
        ----------
            element : selenium.webdriver.remote.webelement.WebElement object
                the WebElement to wrap
            logger : logging.Logger
                a logger instance (see core.logger.py)
        """
        Element.__init__(self, element, logger)
        self.location = element.location
        self.size = element.size
        self.text = element.text

    def get_text(self):
        """
        Get the element's text

        TODO this is redundant, but removing it might break some things

        Returns
        ----------
            text : str
        """
        return self.text

    def get_parent(self, driver):
        """
        Get the element's parent

        Returns
        ----------
            out : ElementSelene object wrapping the parent element
        """
        return ElementSelene(script_get_parent(driver, self.element))

    def find(self, by, identifier, wait=WAIT_NORMAL, log=True):
        """
        This:
            - wraps core.selenium.tasks.task_find
            - finds only elements which are **within** this element.

        Parameters
        ----------
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
        element = task_find(self.element, by, identifier, wait=wait, logger=logger)
        if element is not None:
            try:
                return ElementSelene(element, logger)
            except StaleElementReferenceException as e:
                self.log(f"{e}", "EXCEPTION")
                return self.find(by, identifier, wait, log)
        return None

    def find_all(self, by, identifier, wait=WAIT_NORMAL, log=True):
        """
        This:
            - wraps core.selenium.tasks.task_find_all
            - finds only elements which are **within** this element.

        Parameters
        ----------
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
        elements = task_find_all(self.element, by, identifier, wait=wait, logger=logger)
        try:
            elements = [ElementSelene(el, logger) for el in elements]
        except StaleElementReferenceException as e:
            self.log(f"{e}", "EXCEPTION")
            return self.find_all(by, identifier, wait, log)
        return elements

    def get_attribute(self, *args, **kwargs):
        """
        Gets an attribute from the element. E.g. self.get_attribute('href') would
        return the hyperlink.

        Returns
        ----------
            output : str
                the attribute
        """
        return self.element.get_attribute(*args, **kwargs)

    def has_attribute(self, *args, **kwargs):
        """
        Check whether the element contains a specified attribute.

        Returns
        ----------
            output : bool
               True of the element has the attribute, False otherwise
        """
        return self.element.get_attribute(*args, **kwargs) is not None

    def click(self, driver):
        """
        Click the element.

        Returns
        ----------
            output : bool
                True if the operation was successful, False otherwise
        """
        return script_click_element(driver, self.element)

    def scroll_down(self, driver, wait=WAIT_NORMAL):
        """
        Scroll down the element IF the element has a scrollbar.

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
        height_window = driver.get_window_size()["height"]
        height = script_get_scroll_height(driver, self.element)
        position = script_get_scroll_position(driver, self.element)
        position_new = position + int(0.5 * height_window)
        position_new = min(position_new, height)
        script_scroll_to(driver, position_new, self.element)
        return bool_scroll_position_changed(
            driver, self.element, wait, self.logger, position
        )

    def scroll_to(self, driver, position_new, wait=WAIT_NORMAL):
        """
        Scroll to a new position on the element IF the element has a scrollbar.

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
        position = script_get_scroll_position(driver, self.element)
        script_scroll_to(driver, position_new, self.element)
        return bool_scroll_position_changed(
            driver, self.element, wait, self.logger, position
        )

    def scroll_to_bottom(self, driver, wait=WAIT_NORMAL):
        """
        Scroll to the bottom of the element IF the element has a scrollbar.

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
        height = script_get_scroll_height(driver, self.element)
        script_scroll_to(driver, height, self.element)
        return bool_scroll_height_changed(
            driver, wait, self.logger, height, element=self.element
        )
