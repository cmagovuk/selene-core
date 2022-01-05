from selene.core.crawler import Crawler
from selene.core.selenium.tasks import task_screenshot_to_notebook


class CrawlerSelene(Crawler):
    """
    A crawler class to assist any workflow which requires selenium webdriver.
    
    Inherits selene.core.crawler.Crawler
    """

    def screenshot_to_notebook(self, driver, debug=None):
        """
        Display a thumbnail-sized screenshot to a Jupyter notebook,
        only if the crawler is in debug mode.
        
        Parameters
        ----------
            driver : selenium.webdriver
                the initialised webdriver instance
            debug : bool
                whether or not the craler is in debug mode
        """
        if debug is None:
            debug = self.debug
        if debug:
            task_screenshot_to_notebook(driver, width=600, height=400, logger=None)
