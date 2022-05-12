import pytest

from selene.core.soup.element import *
from selene.core.soup.page import *
from selene.core.selenium.driver import *
from selene.core.selenium.page import *

# initialise the driver, get a page, get its soup
driver = get_driver()
url = "https://www.scrapethissite.com/"
page = PageSelene.from_url(driver=driver, url = url)
soup = page.page_soup

def test_page_soup_from_soup():
    page_from_soup = PageSoup.from_soup(url = url, soup = soup)
    assert page_from_soup is not None

def test_page_soup_from_html():
    page_from_html = PageSoup.from_html(url = url, html = driver.page_source)
    assert page_from_html is not None

def test_page_soup_from_request():
    page_from_request = PageSoup.from_request(url = url)
    assert page_from_request is not None

def test_page_soup_find():
    pass

def test_page_soup_find_all():
    pass

def test_element_from_selene():
    pass

def test_element_find():
    pass

def test_element_find_all():
    pass

def test_get_text():
    pass

def test_has_attr():
    pass

def test_get():
    pass

def test_element_blank():
    pass
