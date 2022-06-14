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
from selene.core.selenium.tasks import *

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
    
# def test_bool_scroll_position_changed():
#     page = PageSelene.from_url(driver=driver, url = "http://www.scrapethissite.com/pages/frames/")
#     el = page.find(driver, by = By.ID, identifier = 'iframe')
#     orig_pos = script_get_scroll_position(driver, el)
#     el.scroll_to_bottom(driver)
#     assert bool_scroll_position_changed(driver, element = el, wait = 1, position = orig_pos, logger = None) == True
    
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
        
def test_get_driver_display():
    driver, display = get_driver(use_display=True)
    assert driver.name is not None
    assert display is not None
    
def test_stop_driver_display():   
    with pytest.raises(Exception):
        stop_driver(display=display)
        driver.current_url

def test_restart_driver():
    driver = get_driver()
    new_driver = restart_driver(driver, wait = 20)
    assert new_driver.name is not None
    
def test_get_user_agent():
    assert "Mozilla" in get_user_agent(10)
    
def test_get_user_agent_random():
    assert get_user_agent_random() is not None

def test_get_text():
    page = PageSelene.from_url(driver=driver, url = "http://www.scrapethissite.com/pages/")
    test_element = page.find(driver, by = By.XPATH, identifier = '//*[@id="pages"]/section/div/div/div/div[1]')
    assert "Countries of the World" in test_element.get_text()

def test_get_parent():
    page = PageSelene.from_url(driver=driver, url = "http://www.scrapethissite.com/pages/")
    test_element = page.find(driver, by = By.XPATH, identifier = '//*[@id="pages"]/section/div/div/div/div[1]')
    assert "Web Scraping Sandbox" in test_element.get_parent(driver).text

def test_find():
    page = PageSelene.from_url(driver=driver, url = "https://www.scrapethissite.com/pages/simple/")
    test_element = page.find(driver, by = By.XPATH, identifier = '//*[@id="countries"]/div/div[4]/div[3]')
    assert test_element.find(By.CLASS_NAME, identifier = "country-name").text == "Afghanistan"

def test_find_all():
    page = PageSelene.from_url(driver=driver, url = "https://www.scrapethissite.com/pages/simple/")
    test_element = page.find(driver, by = By.XPATH, identifier = '//*[@id="countries"]')
    countries = test_element.find_all(By.CLASS_NAME, identifier = "country-name")
    assert len(countries) > 100

def test_get_attribute():
    page = PageSelene.from_url(driver=driver, url = "https://www.scrapethissite.com/pages/simple/")
    test_element = page.find(driver, by = By.XPATH, identifier = '//*[@id="countries"]/div/div[4]/div[3]')
    assert test_element.get_attribute("class") == 'col-md-4 country'

def test_has_attribute():
    page = PageSelene.from_url(driver=driver, url = "https://www.scrapethissite.com/pages/frames/")
    test_element = page.find(driver, by = By.XPATH, identifier = '//*[@id="frames"]/div/div[3]/div[1]')
    assert test_element.has_attribute("class")

def test_click():
    page = PageSelene.from_url(driver=driver, url = "https://www.scrapethissite.com/pages/frames/")
    test_element = page.find(driver, by = By.XPATH, identifier = '//*[@id="frames"]/div/div[3]/div[2]/p/a')
    assert test_element.click(driver)

def test_scroll_down():
    page = PageSelene.from_url(driver=driver, url = "https://www.scrapethissite.com/pages/simple/")
    assert page.scroll_down(driver) is True

def test_scroll_to():
    page = PageSelene.from_url(driver=driver, url = "https://www.scrapethissite.com/pages/simple/")
    assert page.scroll_to(driver, position_new = 50) is True

def test_scroll_to_bottom():
    page = PageSelene.from_url(driver=driver, url = "https://www.scrapethissite.com/pages/simple/")
    assert page.scroll_to_bottom(driver) is True

def test_expand_scroll_height():
    page = PageSelene.from_url(driver=driver, url = "https://www.scrapethissite.com/pages/forms/")
    orig_offset = driver.execute_script("return window.pageYOffset")
    page.expand_scroll_height(driver)
    assert bool_yoffset_changed(driver, wait = 1, yoffset = orig_offset, logger = None) == True

def test_screenshot_to_local():
    page.screenshot_to_local(driver, "./", "test")
    
def test_close_all_tabs_except_specified_tab():
    tab_to_keep = driver.current_window_handle
    page_form = PageSelene.new_tab(driver=driver, url = "https://www.scrapethissite.com/pages/forms/")
    page_form.close_all_tabs_except_specified_tab(driver, handle_keep = tab_to_keep)
    handles = driver.window_handles
    assert len(handles) == 1
    assert handles[0] == tab_to_keep
    
def test_mouse_move():
    assert mouse_move(driver) >= 1
