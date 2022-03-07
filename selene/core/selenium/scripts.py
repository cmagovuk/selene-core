def script_get_scroll_height(driver, element=None):
    """
    Execute JavaScript to get the scroll height of either:
        - the page
        - an element with a scroll bar.

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        element : selenium.webdriver.remote.webelement.WebElement
            the element from which to get the scroll height
            (if None, then the scroll height of the page is found).

    Returns
    ----------
        output : int
            the scroll height in pixels
    """
    if element is None:
        script = "return document.body.scrollHeight;"
        return driver.execute_script(script)
    script = "return arguments[0].scrollHeight;"
    return driver.execute_script(script, element)


def script_get_scroll_position(driver, element=None):
    """
    Execute JavaScript to get the scroll position of either:
        - the page
        - an element with a scroll bar.

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        element : selenium.webdriver.remote.webelement.WebElement
            the element from which to get the scroll position
            (if None, then the scroll position of the page is found).

    Returns
    ----------
        output : int
            the scroll position in pixels
    """
    if element is None:
        script = "return window.pageYOffset;"
        return driver.execute_script(script)
    script = "return arguments[0].scrollTop;"
    return driver.execute_script(script, element)


def script_scroll_to(driver, position, element=None):
    """
    Execute JavaScript to scroll to a position on either:
        - the page
        - an element with a scroll bar.

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        position : int
            the y position (in pxels) to scroll to
        element : selenium.webdriver.remote.webelement.WebElement
            the element from which to get the scroll position
            (if None, then the scroll position of the page is found).

    Returns
    ----------
        output : bool
            True if the operation was successful, False otherwise
    """
    if element is None:
        script = "window.scrollTo(0, arguments[0]); return true;"
        return driver.execute_script(script, position)
    script = "arguments[0].scrollTo(0, arguments[1]); return true;"
    return driver.execute_script(script, element, position)


def script_click_element(driver, element):
    """
    Execute JavaScript to click an element

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        element : selenium.webdriver.remote.webelement.WebElement
            the element from which to get the scroll position
            (if None, then the scroll position of the page is found).

    Returns
    ----------
        output : bool
            True if the operation was successful, False otherwise
    """
    script = "arguments[0].click(); return true;"
    return driver.execute_script(script, element)


def script_get_parent(driver, element):
    """
    Execute JavaScript to get the parent of an element

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        element : selenium.webdriver.remote.webelement.WebElement
            the element from which to get the scroll position
            (if None, then the scroll position of the page is found).

    Returns
    ----------
        output : selenium.webdriver.remote.webelement.WebElement
            the parent WebElement
    """
    script = "return arguments[0].parentElement;"
    return driver.execute_script(script, element)


def script_expand_all_by_class_name(
    driver, identifier, attribute, indicator, clickable=None
):
    """
    WARNING: EXPERIMENTAL

    Execute JavaScript to expand a list of dropdown menus.

    Steps:
        - Find dropdowns by finding all elements with a class name specified with identifier.
        - For each dropdown found:
            - Check if the dropdown is expanded or not. This can be done by:
                - Does the attribute 'class' contain an indicator (e.g. 'expanded')?
                - Does the attribute 'text' contain an indicator (e.g. 'Show More')?
                - Is there an attribute caalled 'exists'?
            -  Find the element to click to expand the dropdown.
               Sometimes the clickable elemnt is not the dropdown itself, but is a button **inside** the dropdown.
            - Click the clickable element.

    Parameters
    ----------
        driver : selenium.webdriver
            a selenium webdriver instance
        identifier :str
            the class name to search for
        attribute : str
            the attribute of the element to check whether it is expanded or not
        indicator : str
            the indicator **within** the attribute, which will indicate whether it is expanded or not
        'clickable' : str
            the class name of the element within the dropdown which you have to click to expand the dropdown

    Returns
    ----------
        output : bool
            True if the operation was successful, False otherwise
    """
    script = """
    let identifier = arguments[0];
    let attribute = arguments[1];
    let indicator = arguments[2];
    let clickable = arguments[3];

    let elements = document.getElementsByClassName(identifier);
    for (element of elements) {
        if (attribute == 'class') {
            if (!element.classList.contains(indicator))
            {
                if (clickable) {
                    element = element.getElementsByClassName(clickable)[0];
                }
                if (element) {
                    element.click();
                }
            }
        }
        else if (attribute == 'text') {
            if (element.textContent.trim() != indicator)
            {
                if (clickable) {
                    element = element.getElementsByClassName(clickable)[0];
                }
                if (element) {
                    element.click();
                }
            }
        }
        else if (attribute == 'exists') {
            if (clickable) {
                element = element.getElementsByClassName(clickable)[0];
            }
            if (element) {
                element.click();
            }
        }
        else {
            if ((!element.hasAttribute(attribute)) || (element.getAttribute(attribute)!=indicator)) {
                if (clickable) {
                    element = element.getElementsByClassName(clickable)[0];
                }
                if (element) {
                    element.click();
                }
            }
        }
    }
    return true;
    """
    return driver.execute_script(script, identifier, attribute, indicator, clickable)
