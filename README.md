# Selene
A framework for more efficient, consistent and maintainable webscraping. Wraps and combines both Selenium Webdriver and BeautifulSoup.

## Motivation
We have gathered data from websites (i.e. webscraping) in multiple projects, applying multiple methodologies and never building upon what we have done previously. Selene introduces a methodology which can be used as the basis for new webscraping projects, and can be easily maintained and improved over time.

## Principles
1. Websites are best represented using an Object-Oriented Programming approach.
2. All websites are made out of pages.
  1. All pages can be represented as Page objects
  2. The base of all Page objects can ultimately derive from inheriting a general Page object.   
3. All webpages are made out of elements.
  1. All elements can be represented as Element objects
  2. The base of all Element objects can ultimately derive from inheriting a general Element object.

For concrete examples of how this works, please check out how specific websites have been broken down into Page objects in `selene.websites`, and how they are used in `vignettes.websites`.

## Features
1. `selene.core`:
  * General Page and Element objects
  * Selenium-based Page and Element objects with functions to wrap Selenium Webdriver.
  * Soup-based Page and Element objects with functions to wrap BeautifulSoup.
2. `vignettes`:
  * Vignettes for getting started
  
## Requirements
- selenium
- beautifulsoup4
- lxml

## Installation
To install from scratch:
1. Load conda environment:
```
conda activate py39
```
2. Install Chrome and chromedriver:
```
bash env-setup.sh
```
3. Install:
```
pip install .
```
