Selene - the CMA DaTA unit's webscraping package
================================================

A framework for more efficient, consistent and maintainable object-oriented webscraping. Wraps and combines both Selenium Webdriver and BeautifulSoup.

**Motivation**

The CMA DaTA unit had gathered data from websites (i.e. webscraping) in multiple projects, applying multiple methodologies and never building upon what we have done previously. Selene introduces a methodology which can be used as the basis for new webscraping projects, and can be easily maintained and improved over time.

**Principles**

1. Websites are best represented using an Object-Oriented Programming approach.
2. All websites are made out of pages.
3. All pages can be represented as Page objects
4. The base of all Page objects can ultimately derive from inheriting a general Page object.   
5. All webpages are made out of elements.
6. All elements can be represented as Element objects
7. The base of all Element objects can ultimately derive from inheriting a general Element object.

**Features**

1. `selene.core`:
  * General Page and Element objects
  * Selenium-based Page and Element objects with functions to wrap Selenium Webdriver.
  * Soup-based Page and Element objects with functions to wrap BeautifulSoup.
  
**Requirements**

* selenium
* beautifulsoup4
* lxml
* ipython
* numpy
* requests

**Installation**

To install from scratch:

1. Install Chrome and chromedriver:

``bash env-setup.sh``

2. Install:

``pip install .``

**Contributing to selene**

The CMA welcomes contributions to selene. If you spot a bug, or think of a potential enhancement to selene - please describe it in an issue using the given template. If you plan on working on the fix / enhancement itself, please assign yourself to the issue and work on a pull request. Otherwise, the DaTA unit will triage the issue and assign some resource to it as appropriate. Any pull requests will need to pass CI (see tox.ini file) and be signed off by an admin.

Notes on pull requests:
* All code must be in black code style. Run ``black -l 90`` on the new files
* Any new functions written will require unit test coverage