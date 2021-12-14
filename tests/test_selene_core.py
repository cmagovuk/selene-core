import sys
import os
import pytest

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import selene

from selene.core.crawler import Crawler
from selene.core.element import *
from selene.core.logger import get_logger
from selene.core.page import *
from selene.core.utils import *

from selene.core.selenium.driver import *

def test_crawler_init():
    assert Crawler() is not None
    
def test_crawler_logging():
    crawler = Crawler()
    assert crawler.log('test') is None
    
def test_crawler_screenshot():
    crawler = Crawler()
    driver = get_driver()
    assert crawler.screenshot_to_notebook(driver)


