from selene.core.logger import get_logger
from selene.core.selenium.tasks import task_screenshot_to_notebook


class Crawler:
    """
    A parent crawler class to assist any worflow.
    """

    def __init__(self, id_crawler="Crawler", debug=True):
        """
        Initialise Crawler.

        Parameters
        ----------
            id_crawler : str
                an ID to show up in the logging message
            debug : bool
                whether to start the crawler in debug mode
        """
        self.id = "Crawler"
        self.debug = debug
        # Get logger
        if debug:
            self.logger = get_logger(level="DEBUG")
        else:
            self.logger = get_logger(level="INFO")

    def log(self, message, level="DEBUG"):
        """
        Output a log message, with the appropriate loglevel (default=DEBUG).

        Parameters
        ----------
            message : str
                the message to log
            level : str
                the loglevel of the message
        """
        if self.logger is None:
            return
        message = f"{self.id}: {message}"
        if level == "DEBUG":
            self.logger.debug(message)
        elif level == "INFO":
            self.logger.info(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "EXCEPTION":
            self.logger.exception(message)

    def screenshot_to_notebook(self, driver, debug=None):
        """
        Display a thumbnail-sized screenshot to a Jupyter notebook,
        only if the crawler is in debug mode.

        Parameters
        ----------
            driver : selenium.webdriver
                a selenium webdriver instance
            debug : bool
                whether or not the craler is in debug mode
        """
        if debug is None:
            debug = self.debug
        if debug:
            task_screenshot_to_notebook(driver, width=600, height=400, logger=None)
