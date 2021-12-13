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

# %% [raw]
# !conda install dask -y

# %% [markdown]
# ## Dask (Selene)
# 1. Create a page object to perform a set of simple tasks
# 1. Load the driver
# 1. Load the logger
# 1. Create some instances of the page object
# 1. Loop through the instances, in parallel, performing the tasks on each instance
# 1. Close the driver

# %%
import sys
import numpy as np
import pandas as pd
import multiprocessing
sys.path.append('../../..')

# %%
import dask
import dask.dataframe as dd
from dask.distributed import Client, progress

# %%
n_workers = multiprocessing.cpu_count()
threads_per_worker = 2
memory_limit = '1GB'
print(n_workers, threads_per_worker, memory_limit)

# %%
client = Client(n_workers=n_workers, threads_per_worker=threads_per_worker, memory_limit='1GB')
client

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
def thread_execute(row):
    try:
        url = row.name
    except:
        url = row
    driver = get_driver()
    page = PageForm.from_url(driver, url)
    df = page.execute(driver)
    return df


# %%
urls = [f'https://www.scrapethissite.com/pages/forms/?page_num={i}' for i in range(1, 3, 1)]
urls

# %%
# %%time
thread_execute(urls[0])

# %%
df = pd.DataFrame()
df['url'] = urls
df

# %%
ddf = dd.from_pandas(df, npartitions=n_workers*threads_per_worker)

# %%
meta = {
    'team_name': 'O',
    'year': 'i8',
    'wins': 'i8',
    'losses': 'i8',
    'ot_losses': 'i8',
    'win_%': 'f8',
    'goals_for_(gf)': 'i8',
    'goals_against_(ga)': 'i8',
    '+_/_-': 'i8',
    'source': 'O'
}

# %%
# %%time
ddf = ddf.groupby('url').apply(thread_execute, meta=meta).compute().reset_index().drop(columns='level_1')

# %%
ddf

# %%
