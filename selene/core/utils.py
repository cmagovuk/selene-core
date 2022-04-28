import re
import time
import functools
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains


def get_domain(url):
    """
    Get the domain of a web url. Pretty rudimentary - there might be edge cases.

    Parameters
    ----------
        url : str
            the url to be trimmed

    Returns
    ----------
        domain : str
            the domain
    """
    if "https" in url:
        return url.split("https://")[1].split("/")[0]
    else:
        return url.split("http://")[1].split("/")[0]


def random_wait(_func=None, *, seconds_min=0, seconds_max=1):
    """
    Wraps core.Page, core.selenium.Page and core.Soup.Page functions in order to
    pause a number of seconds (between seconds_min and seconds_max), before
    executing the function.

    Sometimes this is handy for when scraping jobs get blocked due to too many
    requests in a short period of time.
    """

    def decorator_random_wait(func):
        @functools.wraps(func)
        def wrapper_random_wait(*args, **kwargs):
            seconds_sleep = np.round(
                np.random.uniform(low=seconds_min, high=seconds_max), 3
            )
            if args[0].logger:
                args[0].logger.debug(f"waiting for {seconds_sleep} seconds")
            time.sleep(seconds_sleep)
            return func(*args, **kwargs)

        return wrapper_random_wait

    if _func is None:
        return decorator_random_wait
    else:
        return decorator_random_wait(_func)


def validateUrl(url):
    # Regex to check for a valid URL
    reg_exp = (
        "((http|https)://)(www.)?"
        + "[a-zA-Z0-9@:%._\\+~#?&//=]"
        + "{2,256}\\.[a-z]"
        + "{2,6}\\b([-a-zA-Z0-9@:%"
        + "._\\+~#?&//=]*)"
    )

    # Compile the ReGex
    compiled = re.compile(reg_exp)

    # return false if empty string
    if url == None:
        return False

    # return True if there is a match
    if re.search(compiled, url):
        return True
    else:
        return False
    
    
def mouse_move(driver, max_mouse_moves = 10):
    """performs mouse move, for help with bot mitigation, partially ported from OpenWPM """
    
    # bot mitigation: move the mouse randomly around a number of times
    window_size = driver.get_window_size()
    num_moves = 0
    num_fails = 0
    while num_moves < max_mouse_moves + 1 and num_fails < max_mouse_moves:
        try:
            if num_moves == 0:  # move to the center of the screen
                x = int(round(window_size["height"] / 2))
                y = int(round(window_size["width"] / 2))
            else:  # move a random amount in some direction
                move_max = random.randint(0, 500)
                x = random.randint(-move_max, move_max)
                y = random.randint(-move_max, move_max)
            action = ActionChains(webdriver)
            action.move_by_offset(x, y)
            action.perform()
            num_moves += 1
        except MoveTargetOutOfBoundsException:
            num_fails += 1
            pass
