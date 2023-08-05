import logging
import os

__version__ = "4.1.0"
color_mood = False
cached_news_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cached_news'))


# globally set the verbose/logging config based on the input from the user
def set_verbose(verbose):
    if verbose:
        # setting the lowest priority level to Info, showing all logs with info level and higher
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
        logging.info("Verbose is set to On")
    else:
        # by setting critical + 1, even the highest priority leveled messages are not printed
        logging_level = logging.CRITICAL + 1
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging_level)


# setting the color_mood to True if the user has set the colorize option
def colorize():
    global color_mood
    color_mood = True
