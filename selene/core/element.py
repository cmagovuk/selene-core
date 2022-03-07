class Element:
    """
    A parent Element class. Both ElementSelene and ElementSoup inherit this class.
    """

    def __init__(self, element, logger):
        """
        Initialise Element.

        Parameters
        ----------
            element :
                this could be a BeautifulSoup WebElement or a Selenium Webdriver WebElement.
            logger : logging.Logger
                a logger instance (see core.logger.py)
        """
        self.element = element
        self.logger = logger

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
        message = f"{message}"
        if level == "DEBUG":
            self.logger.debug(message)
        elif level == "INFO":
            self.logger.info(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "EXCEPTION":
            self.logger.exception(message)
