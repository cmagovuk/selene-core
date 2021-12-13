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
# ## Navigate to Page (Selene)
# 1. Load the driver
# 1. Load the logger
# 1. Create a PageSelene object using the `from_url` function to navigate to the url
# 1. Take a screenshot
# 1. Close the driver

# %%
import sys
sys.path.append('../../..')

# %%
from selene.core.logger import get_logger
from selene.core.selenium.driver import get_driver, stop_driver
from selene.core.selenium.page import PageSelene

# %%
driver = get_driver(width=1024, height=768)
logger = get_logger(level='DEBUG')

# %%
url = 'https://www.scrapethissite.com'
page = PageSelene.from_url(driver, url, string=url, logger=logger)

# %%
page.screenshot_to_notebook(driver)

# %%
stop_driver(driver)

# %%
