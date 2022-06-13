import os
import time
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from pyvirtualdisplay import Display
from selene.core.config import *


def get_driver(
    width=2560,
    height=1440,
    user_agent="default",
    incognito=False,
    disable_gpu=False,
    use_display=False,
):
    """
    Get an instance of selenium.webdriver and start browser

    Parameters
    ----------
        width : int
            the width of the browser
        height : int
            the height of the browser
        user_agent :
            If False, then no user agent is used.
            If 'default', then a default user agent is used.
            If 'random', then a random user agent is  selected.
            Otherwise, the specified user agent is used.
        incognito : bool
            whether or not to start the browser in incognito mode
        disable_gpu : bool
            whether or not to disable GPU
        use_display: bool
            whether or not to use a virtual display

    Returns
    ----------
        driver : selenium.webdriver
            selenium.webdriver instance
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if incognito:
        options.add_argument("--incognito")
    if disable_gpu:
        options.add_argument("--disable-gpu")
    if user_agent and user_agent == "random":
        user_agent = get_user_agent_random()
        options.add_argument(f"--user-agent={user_agent}")
    elif user_agent and user_agent == "default":
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4934.122 Safari/537.36"
        options.add_argument(f"--user-agent={user_agent}")
    elif user_agent:
        options.add_argument(f"--user-agent={user_agent}")

    # enable browser logging
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"browser": "ALL"}

    driver = webdriver.Chrome(options=options, desired_capabilities=desired_capabilities)
    driver.set_window_rect(x=0, y=0, width=width, height=height)

    if use_display:
        display = Display(visible=False, size=(width, height))
        display.start()
        return driver, display

    return driver


def stop_driver(driver, display=None):
    """
    Stop and close the selenium.webdriver instance

    Parameters
    ----------
        driver : selenium.webdriver
             the selenium webdriver instance to stop
        display : pyvirtualdisplay.Display optional
             if using a pyvirtual display, display to stop
    """
    if display != None:
        display.stop()
    driver.close()
    driver.quit()


def restart_driver(driver, wait=WAIT_BIG):
    """
    Stop and close the selenium.webdriver instance, wait for a specified
    number of seconds, then start a new instance

    Parameters
    ----------
        driver : selenium.webdriver
            the selenium webdriver instance to stop

    Returns
    ----------
        driver : selenium.webdriver
            The new selenium.webdriver instance
    """
    stop_driver(driver)
    time.sleep(wait)
    return get_driver()


def get_user_agent(i):
    """
    Get a specific user agent string from core.config.USER_AGENTS

    Parameters
    ----------
        i : int
            the list index

    Returns
    ----------
        user_agent : str
            The selected user agent
    """
    return USER_AGENTS[i]


def get_user_agent_random():
    """
    Get a random user agent string from core.config.USER_AGENTS

    Returns
    ----------
        user_agent : str
            The selected user agent
    """
    return str(np.random.choice(USER_AGENTS))
