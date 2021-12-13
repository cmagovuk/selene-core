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
# ## Gather Data (Selene)
# 1. Load the driver
# 1. Load the logger
# 1. Create a PageSelene object using the `from_url` function to navigate to the url
# 1. Take a screenshot
# 1. Find all elements on the page:
#     1. By class name
#     1. By tag
#     1. By xpath
#     1. By soup
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

# %%
driver = get_driver(width=1024, height=768)
logger = get_logger(level='DEBUG')

# %%
url = 'https://www.scrapethissite.com/pages/simple/'
page = PageSelene.from_url(driver, url, logger=logger)

# %%
page.screenshot_to_notebook(driver)

# %%
for element in page.find_all(driver, By.CLASS_NAME, 'country-name')[:3]:
    print(element.text)

# %%
for element in page.find_all(driver, By.TAG_NAME, 'h3')[:3]:
    print(element.text)

# %%
for element in page.find_all(driver, By.XPATH, '//*[contains(text(), \'An\')]')[:3]:
    print(element.text)

# %%
for element in page.find_all(driver, By.XPATH, '//*[contains(@class, \'country-area\')]')[:3]:
    print(element.text)

# %%
for element in page.find_all_soup('span', {'class': 'country-population'})[:3]:
    print(element.text)

# %%
stop_driver(driver)

# %%
