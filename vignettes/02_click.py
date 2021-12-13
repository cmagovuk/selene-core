# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.4
#   kernelspec:
#     display_name: Python 3.9
#     language: python
#     name: py39
# ---

# %% [markdown]
# ## Click (Selene)
# 1. Load the driver
# 1. Load the logger
# 1. Create a PageSelene object using the `from_url` function to navigate to the url
# 1. Take a screenshot
# 1. Check table is not visible
# 1. Click an element
# 1. Wait for the table to become visible
# 1. Take a screenshot
# 1. Close the driver

# %%
import sys
sys.path.append('../../..')

# %%
from selenium.webdriver.common.by import By

# %%
from selene.core.logger import get_logger
from selene.core.selenium.driver import get_driver, stop_driver
from selene.core.selenium.page import PageSelene
from selene.core.selenium.conditions import *

# %%
driver = get_driver(width=1024, height=768)
logger = get_logger(level='DEBUG')

# %%
url = 'https://www.scrapethissite.com/pages/ajax-javascript/'
page = PageSelene.from_url(driver, url, logger=logger)

# %%
page.screenshot_to_notebook(driver)

# %%
element = page.find(driver, By.ID, '2015')
print(element.text)
print(bool_element_class_does_not_contain(driver, element, string='active', wait=0.1, logger=logger))
print(bool_invisible(driver, By.CLASS_NAME, 'table'))

# %%
element.click(driver)

# %%
print(bool_element_class_contains(driver, element, string='active', wait=0.1, logger=logger))
print(bool_visible(driver, By.CLASS_NAME, 'table'))

# %%
page.screenshot_to_notebook(driver)

# %%
stop_driver(driver)

# %%
