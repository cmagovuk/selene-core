Selene
======

A framework for efficient, consistent and maintainable object-oriented webscraping. Wraps and combines both Selenium Webdriver and BeautifulSoup.

Principles
~~~~~~~~~~

1. Websites are best represented using an Object-Oriented Programming approach.
2. All websites are made out of pages.
3. All pages can be represented as Page objects
4. The base of all Page objects can ultimately derive from inheriting a general Page object.   
5. All webpages are made out of elements.
6. All elements can be represented as Element objects
7. The base of all Element objects can ultimately derive from inheriting a general Element object.

Features
~~~~~~~~

* General Page and Element objects.
* Selenium-based Page and Element objects with methods that wrap Selenium Webdriver.
* Soup-based Page and Element objects with methods that wrap BeautifulSoup.
  
How to use it
~~~~~~~~~~~~~

Selene is a framework. It provides base Classes that can be used to create website-specific ``Page`` and ``Element`` objects by sub-classing the base Classes. Please refer to the `documentation <websites/websites.html>`_ for an example of how this is done.

Installation
~~~~~~~~~~~~

To install from scratch

* Install Chrome and chromedriver: ``bash env-setup.sh``

* Install: ``pip install .``