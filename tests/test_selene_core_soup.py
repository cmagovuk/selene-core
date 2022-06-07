import pytest

from selene.core.soup.element import *
from selene.core.soup.page import *
from selene.core.selenium.driver import *
from selene.core.selenium.page import *

# initialise the driver, get a page, get its soup
driver = get_driver()
url = "https://www.scrapethissite.com/pages/simple/"
page = PageSelene.from_url(driver = driver, url = url)
soup = page.page_soup
element = soup.find('div', {'class': 'col-md-6 text-right'})

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
    assert "There are" in soup.find('div', {'class': 'col-md-6'}).text

def test_page_soup_find_all():
    assert len(soup.find_all('h3', {'class': 'country-name'})) > 200

def test_element_find():
    assert element.find('a', {'class': 'data-attribution'}) is not None

def test_element_find_all():
    el = soup.find('div', {'class': 'col-md-4 country'})
    spans = el.find_all('span')
    assert len(spans) > 1

def test_get_text():
    assert "Data via" in element.get_text()

def test_has_attr():
    assert element.find('a', {'class': 'data-attribution'}).has_attr("href")

def test_get():
    assert element.find('a', {'class': 'data-attribution'}).get("href")
    
def test_element_blank():
    element_blank = ElementSoupBlank()
    assert element_blank.text is None
