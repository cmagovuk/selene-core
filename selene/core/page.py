from .utils import *


class Page:
    """
    A parent Page class. Both PageSelene and PageSoup inherit this class.
    """

    def __init__(self, url, logger, id_page=0):
        """
        Initialise Page.

        Parameters
        ----------
            url : str
                any webpage has a url
            logger : logging.Logger
                a logger instance (see core.logger.py)
            id_page : str
                an ID to show up in the logging message
        """
        self.url = url
        self.logger = logger
        self.domain = get_domain(url)
        self.id = f"WORKER-{id_page:02}"

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
