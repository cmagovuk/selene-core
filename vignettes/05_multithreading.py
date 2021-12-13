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
# ## Multithreading (Selene)
# Webscraping is an I/O-bound problem, which is why we're concentrating on multithreading rather than multiprocessing.
# 1. Create a page object to perform a set of simple tasks
# 1. Load the driver
# 1. Load the logger
# 1. Create some instances of the page object
# 1. Loop through the instances, in parallel, performing the tasks on each instance
# 1. Close the driver

# %%
import sys
import threading
import numpy as np
import pandas as pd
import concurrent.futures
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
    
    def execute(self, driver):
        return self.get_table_data(driver)
    
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
THREAD_LOCAL = threading.local()


# %%
def thread_get_driver():
    driver = getattr(THREAD_LOCAL, 'driver', None)
    if driver is None:
        driver = get_driver()
        setattr(THREAD_LOCAL, 'driver', driver)
    return driver

def thread_get_page_from_url(url, PageObject):
    page = getattr(THREAD_LOCAL, 'page', None)
    if page is None:
        driver = thread_get_driver()
        page = PageObject.from_url(driver, url)
        setattr(THREAD_LOCAL, 'page', page)
    return page

def thread_page_execute(url, PageObject, args):
    driver = thread_get_driver()
    page = thread_get_page_from_url(url, PageObject)
    return page.execute(driver, *args)


# %%
urls = [f'https://www.scrapethissite.com/pages/forms/?page_num={i}' for i in range(1, 11, 1)]
urls

# %%
page_objects = [PageForm for url in urls]
args = [() for url in urls] 

# %%
# %%time
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    dfs = executor.map(thread_page_execute, urls, page_objects, args)
df = pd.concat(dfs)

# %%
df

# %%
