import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select

from selene.core.config import *
from selene.core.selenium.scripts import *
from selene.core.selenium.driver import *
from selene.core.selenium.page import *
from selene.core.selenium.crawler import *

# initialise the driver
driver = get_driver()
url = "https://www.scrapethissite.com/"
page = PageSelene.from_url(driver=driver, url = url)

def test_bool_url_changed():
    assert bool_url_changed(driver, wait=1, logger=None, url = url) == False
    
def test_bool_url_expected():
    assert bool_url_expected(driver, wait=1, logger=None, url = url) == True
    
def test_bool_url_unexpected():
    alt_url = "https://www.scrapethissite.com/pages/simple/"
    assert bool_url_unexpected(driver, wait=1, logger=None, url = alt_url) == True
    
def test_bool_url_contains():
    assert bool_url_contains(driver, wait=1, logger=None, string = "scrape") == True
    
def test_bool_url_does_not_contain():
    assert bool_url_does_not_contain(driver, wait=1, logger=None, string = "scrape") == False
    
def test_bool_visible():
    assert bool_visible(driver, by = By.ID, identifier = 'nav-homepage', wait = 1) == True
    
def test_bool_invisible():
    assert bool_invisible(driver, by = By.ID, identifier = 'nav-homepage', wait = 1) == False
    
def test_bool_clickable():
    assert bool_clickable(driver, by = By.XPATH, identifier = '//*[@id="hero"]/div/div/div/a[1]', wait = 1) == True
    
def test_bool_yoffset_changed():
    page = PageSelene.from_url(driver=driver, url = "https://www.scrapethissite.com/pages/simple/")
    orig_offset = driver.execute_script("return window.pageYOffset")
    page.scroll_down(driver, wait = 1)
    assert bool_yoffset_changed(driver, wait = 1, yoffset = orig_offset, logger = None) == True
    
def test_bool_scroll_position_changed():
    page = PageSelene.from_url(driver=driver, url = "http://www.scrapethissite.com/pages/frames/")
    el = page.find(driver, by = By.ID, identifier = 'iframe')
    orig_pos = script_get_scroll_position(driver, el)
    el.scroll_to_bottom(driver)
    assert bool_scroll_position_changed(driver, element = el, wait = 1, position = orig_pos) == True
    
def test_bool_scroll_height_changed():
    page = PageSelene.from_url(driver=driver, url = "http://www.scrapethissite.com/pages/forms/")
    orig_height = script_get_scroll_height(driver)
    Select(driver.find_element_by_xpath('//*[@id="per_page"]')).select_by_value('100')
    assert bool_scroll_height_changed(driver, wait = 1, logger = None, height = orig_height) == True      
    
def test_bool_element_class_contains():
    page = PageSelene.from_url(driver=driver, url = "http://www.scrapethissite.com/pages/")
    test_element = page.find(driver, by = By.XPATH, identifier = '//*[@id="pages"]/section/div/div/div/div[1]') 
    assert bool_element_class_contains(driver, element = test_element, wait = 1, logger = None, string = "page") == True
    
def test_bool_element_class_does_not_contain():
    page = PageSelene.from_url(driver=driver, url = "http://www.scrapethissite.com/pages/")
    test_element = page.find(driver, by = By.XPATH, identifier = '//*[@id="pages"]/section/div/div/div/div[1]')
    assert bool_element_class_does_not_contain(driver, element = test_element, wait = 1, logger = None, string = "test") == True    
    
def test_bool_element_text_contains():
    page = PageSelene.from_url(driver=driver, url = "http://www.scrapethissite.com/")
    test_element = page.find(driver, by = By.XPATH, identifier = '//*[@id="hero"]/div/div/div/a[1]')
    assert bool_element_text_contains(driver, element = test_element, wait = 1, logger = None, string = "Sandbox") == True
    
def test_bool_element_text_does_not_contain():
    page = PageSelene.from_url(driver=driver, url = "http://www.scrapethissite.com/")
    test_element = page.find(driver, by = By.XPATH, identifier = '//*[@id="hero"]/div/div/div/a[1]')
    assert bool_element_text_does_not_contain(driver, element = test_element, wait = 1, logger = None, string = "Sandbox") == False
    
def test_bool_new_handle():
    page.new_tab(driver, url = "http://www.scrapethissite.com/")
    assert bool_new_handle(driver, n_handles_old = 1, wait = 1, logger = None) == True
      
def test_bool_correct_handle():
    # unclear how to write a test for this, how do we define the expected handle
    pass
    
def test_crawler_init():
    assert CrawlerSelene() is not None

def test_get_driver():
    driver = get_driver()
    assert driver.name is not None
    
def test_stop_driver():   
    with pytest.raises(Exception):
        stop_driver()
        driver.current_url

def test_restart_driver():
    assert True
    
def test_get_user_agent():
    assert True
    
def test_get_user_agent_random():
    assert True

# TEST ELEMENT


# TEST PAGE


# TEST SCRIPTS


# TEST TASKS