import os
import time
import requests
from datetime import datetime
from bs4 import BeautifulSoup

from ..page import *
from ..config import *

from .element import ElementSoup, ElementSoupBlank


class PageSoup(Page):
    """
    A page class to assist any workflow which requires BeautifulSoup.

    This is really a way to make Selenium WebDriver and BeautifulSoup more interchangeable, in as far as
    you can instantiate either a PageSoup or a PageSelene object, and the .find and .find_all function work in
    similar ways.

    Inherits selene.core.page.Page
    """

    def __init__(self, url, soup, logger=None):
        """
        Initialise a PageSoup instance from existing, parsed soup.

        Parameters
        ----------
            url : str
                the url of the page
            soup :
            logger : logging.Logger
                a logger instance (see core.logger.py)
        """
        Page.__init__(self, url, logger)
        self.soup = soup

    @classmethod
    def from_soup(cls, url, soup, logger=None):
        """
        Initialise a PageSoup instance from existing, parsed soup.

        Parameters
        ----------
            url : str
                the url of the page
            soup :
            logger : logging.Logger
                a logger instance (see core.logger.py)
        """
        return cls(url, soup, logger)

    @classmethod
    def from_html(cls, url, html, logger=None):
        """
        Initialise a PageSoup instance from existing html source code.

        Parameters
        ----------
            url : str
                the url of the page
            html : str
                the html code to parse
            logger : logging.Logger
                a logger instance (see core.logger.py)
        """
        soup = BeautifulSoup(html, "lxml")
        return cls(url, soup, logger)

    @classmethod
    def from_request(cls, url, logger=None):
        """
        Initialise a PageSoup instance by parsing a request to a web url.

        Parameters
        ----------
            url : str
                the url of the page
            logger : logging.Logger
                a logger instance (see core.logger.py)
        """
        user_agent = str(np.random.choice(USER_AGENTS))
        headers = {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        }
        with requests.Session() as session:
            page = session.get(url, headers=headers).content.decode()
            soup = BeautifulSoup(page, "lxml")
            return cls(url, soup, logger)

    def find(self, *args, **kwargs):
        """
        Find and return specific a specific element within the page html

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
        el = self.soup.find(*args, **kwargs)
        if el is None:
            return ElementSoupBlank()
        if not el.has_attr("href"):
            el.attrs["href"] = None
        return ElementSoup(el, self.logger)

    def find_all(self, *args, **kwargs):
        """
        Find and return all elements within the page html that meet the given criteria

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
        for el in self.soup.find_all(*args, **kwargs):
            if not el.has_attr("href"):
                el.attrs["href"] = None
            els.append(ElementSoup(el, self.logger))
        return els
