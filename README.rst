Selene - the CMA DaTA unit's webscraping package
================================================

A framework for more efficient, consistent and maintainable object-oriented webscraping. Wraps and combines both Selenium Webdriver and BeautifulSoup.

Principles
~~~~~~~~

1. Websites are best represented using an Object-Oriented Programming approach.
2. All websites are made out of pages.
3. All pages can be represented as Page objects
4. The base of all Page objects can ultimately derive from inheriting a general Page object.   
5. All webpages are made out of elements.
6. All elements can be represented as Element objects
7. The base of all Element objects can ultimately derive from inheriting a general Element object.

Features
~~~~~~~~

1. `selene.core`:
  * General Page and Element objects
  * Selenium-based Page and Element objects with functions to wrap Selenium Webdriver.
  * Soup-based Page and Element objects with functions to wrap BeautifulSoup.
  
Installation
~~~~~~~~

To install from scratch:

1. Install Chrome and chromedriver:

``bash env-setup.sh``

2. Install:

``pip install .``