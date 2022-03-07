import os
import sys
import logging


def get_logger(
    name="log",
    level="INFO",
    to_console=True,
    to_file=False,
    overwrite=False,
    dirpath="/notebooks/selene_logger",
    filename="log.log",
):
    """
    Initialise a logger instance to print, either to file or to a notebook.

    Parameters
    ----------
        name : str
            the name of the logger
        level : str
            the loglevel of the log. Can be DEBUG, INFO, WARNING or EXCEPTION (default INFO)
        to_console : bool
            whether or not to print the log to console/notebook
        to_file : bool
            whether or not to print the log to a file
        overwrite : bool
            whether or not to overwrite an existing file
        dirpath : str
            the path to a directory to save the log (if to_file is True)
        filename : str
            the path to a file to save the log (if to_file is True)

    Returns
    ----------
        logger : logging.Logger
            the logger instance
    """
    # Get logger
    logger = logging.getLogger(name)
    logger.handlers = []
    # Set the loglevel and format
    logger.setLevel(level)
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    if to_console:
        # Add the stream handler to print to console/notebook
        stream_handler = logging.StreamHandler(stream=sys.stderr)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    if to_file:
        # Create the directory
        if not os.path.exists(dirpath):
            print("Directory not found; creating: {}".format(dirpath))
            os.makedirs(dirpath)
        filepath = "{}/{}".format(dirpath, filename)
        print("Saving log to {}".format(filepath))
        # Create the file
        if os.path.exists(filepath) and overwrite:
            print("File exists; overwriting: {}".format(filepath))
            file_handler = logging.FileHandler(filepath, mode="w")
        elif os.path.exists(dirpath):
            print("File exists; appending: {}".format(filepath))
            file_handler = logging.FileHandler(filepath, mode="a")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    logger.info("Logger started")
    return logger
