from bs4 import BeautifulSoup

from selene.core.config import *
from selene.core.element import Element


class ElementSoup(Element):
    """
    An element class to wrap beautiful soup functionality for finding and returning attributes from soup objects.
    """

    def __init__(self, element, logger=None):
        """
        Initialise an ElementSoup instance

         Parameters
        ----------
            element : html object
            logger : logging.Logger
                a logger instance (see core.logger.py)
        """
        Element.__init__(self, element, logger)
        self.attrs = element.attrs
        self.text = element.get_text()

    @classmethod
    def from_selene(cls, element_selene, logger=None):
        """
        Initialise an ElementSoup instance from an ElementSelene object.
        Allow interchangeability between selenium-based on soup-based elements

        Parameters
        ----------
            element_selene : selene.core.selenium.ElementSelene
            logger : logging.Logger
                a logger instance (see core.logger.py)
        """
        html = element_selene.element.get_attribute("innerHTML")
        soup = BeautifulSoup(html, "lxml")
        return cls(element=soup.body, logger=logger)

    def find(self, *args, **kwargs):
        """
        Find and return specific elements within the html

        Parameters
        ----------
            element : str
                the type of html element searched for e.g. 'div'
            attributes : dict
                attributes of the searched element e.g. {"class": "text-1"}
        Returns
        ----------
            el : ElementSoup
        """
        self.log(f'find: {"; ".join([str(arg) for arg in [*args]])}')
        el = self.element.find(*args, **kwargs)
        if el is None:
            return ElementSoupBlank()
        if not el.has_attr("href"):
            el.attrs["href"] = None
        return ElementSoup(el, self.logger)

    def find_all(self, *args, **kwargs):
        """
        Find and return all elements within the html that meet the given criteria

        Parameters
        ----------
            element : str
                the type of html element searched for e.g. 'div'
            attributes : dict
                attributes of the searched element e.g. {"class": "text-1"}
        Returns
        ----------
            els : list
                all  ElementSoup that meet criteria
        """
        self.log(f'find_all: {"; ".join([str(arg) for arg in [*args]])}')
        els = []
        for el in self.element.find_all(*args, **kwargs):
            if not el.has_attr("href"):
                el.attrs["href"] = None
            els.append(ElementSoup(el, self.logger))
        return els

    def get_text(self):
        """return text of object"""
        return self.text

    def has_attr(self, *args, **kwargs):
        """check whether element has a given attribute"""
        return self.element.has_attr(*args, **kwargs)

    def get(self, *args, **kwargs):
        """return a given attribute of the element"""
        return self.element.get(*args, **kwargs)


class ElementSoupBlank(ElementSoup):
    """
    A class for blank soup objects. Used in cases where another method has not returned anything
    """

    def __init__(self):
        """Initialise a ElementSoupBlank object"""
        self.element = None
        self.attrs = {"href": None, "id": None, "aria-label": None}
        self.find = lambda *x: ElementSoupBlank()
        self.find_all = lambda *x: []
        self.text = None
        self.has_attr = lambda *x: False
        self.get = lambda *x: None
        self.get_text: lambda: None
