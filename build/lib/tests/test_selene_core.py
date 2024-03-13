import sys
import os
import pytest
import time

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
    
def test_element_init():
    el = "test_element"
    logger = get_logger()
    element = Element(el, logger)
    assert element.element == "test_element"
        
def test_element_logging():
    el = "test_element"
    element = Element(el, logger = get_logger())
    assert element.log('test') is None
       
def test_logger_init():
    logger = get_logger()
    assert logger is not None
       
def test_logger_to_file():
    logger = get_logger(to_file=True, 
                        dirpath=".",
                        filename ="test_logger.log",
                        overwrite=True)
    crawler = Crawler()
    crawler.log('test')
    assert os.path.isfile("./test_logger.log")
    
def test_page_init():
    test_url = "https://www.scrapethissite.com/"
    page = Page(url=test_url, logger = get_logger())
    assert page is not None
    
def test_page_logging():
    test_url = "https://www.scrapethissite.com/"
    logger = get_logger(to_file=True, 
                        dirpath=".",
                        filename ="test_logger.log",
                        overwrite=True)
    page = Page(url=test_url, logger = logger)
    page.log('test log message')
    assert os.path.isfile("./test_logger.log")
    

def test_utils_get_domain():
    url = "https://www.scrapethissite.com/"
    assert get_domain(url) == "www.scrapethissite.com"
      
def test_random_wait():
    @random_wait(seconds_min=2, seconds_max=3)
    def test_func(x):
        print(x)
    test_url = "https://www.scrapethissite.com/"
    page = Page(url=test_url, logger = get_logger())
    start_time = time.time()  
    test_func(page)
    end_time = time.time()
    time_elapsed = end_time - start_time
    assert time_elapsed >= 2
      
def test_validate_url():
    url = "https://www.scrapethissite.com/"
    assert validateUrl(url) is True