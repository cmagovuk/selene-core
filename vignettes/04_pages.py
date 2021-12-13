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
# ## Page Objects (Selene)
# 1. Create a page object to perform a set of simple tasks
# 1. Load the driver
# 1. Load the logger
# 1. Create some instances of the page object
# 1. Loop through the instances, performing the tasks on each instance
# 1. Close the driver

# %%
import sys
import pandas as pd
sys.path.append('../../..')

# %%
from selenium.webdriver.common.by import By

# %%
from selene.core.logger import get_logger
from selene.core.selenium.driver import get_driver, stop_driver
from selene.core.selenium.page import PageSelene
from selene.core.selenium.conditions import *


# %%
class PageForm(PageSelene):
    
    def get_table_data(self, driver):
        self.log(f'{self.url}: get_table_data')
        
        values = []
        table = self.find(driver, By.CLASS_NAME, 'table')
        for i, row in enumerate(table.find_all(By.TAG_NAME, 'tr')):
            if i == 0:
                cols = row.find_all(By.TAG_NAME, 'th')
                cols = [col for col in cols if col.text is not None]
                colnames = [col.text.strip().lower().replace(' ', '_') for col in cols]
                continue
            cols = row.find_all(By.TAG_NAME, 'td')
            cols = [col for col in cols if col.text is not None]
            values.append([col.text.strip().lower() for col in cols])
        df = pd.DataFrame(columns=colnames, data=values)
        df['source'] = self.url
        return df


# %%
driver = get_driver(width=1024, height=768)
logger = get_logger(level='DEBUG')

# %%
urls = [f'https://www.scrapethissite.com/pages/forms/?page_num={i}' for i in range(1, 11, 1)]
urls

# %%
# %%time
df = pd.DataFrame()
for i, url in enumerate(urls):
    page = PageForm.from_url(driver, url, logger=logger)
    df = df.append(page.get_table_data(driver))
    page.screenshot_to_notebook(driver)

# %%
df

# %%
stop_driver(driver)

# %%
