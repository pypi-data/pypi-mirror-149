""" Caches the news and retrieves the cached news

This modules implements functions to cache the previously
seen feeds, and retrieve them when user enters the date
argument

Functions:
    get_encoding(soup): Checks the encoding of the html file of
                        the news page

    cache_news(news_list): saves the news list in a file
    retrieve_cache(): reads the file that contents the cached news
    find_item(selected_date, json, limit): based on the given date,
                selects the news that are published after the date
                and picks the number of news specified by the limit
                argument (if the argument is not present, all cached
                news) also prints the feed if it is in the regular format
    clear_cache(): deletes the file of the cached news
    show_cache_by_date(selected_date, json, limit): prints
                the selected number of cached news feed with
                calling find_item function

"""

try:
    import pickle
    from RSSparser.date_time import date_object, time_in_range
    from datetime import datetime
    from RSSparser.print_news import print_json_format, print_regular_format
    import logging
    import os
    import shutil
    import dateutil.parser
    from RSSparser.convert_format import convert_html, convert_pdf
    from RSSparser import cached_news_directory
except ImportError as error:
    raise SystemExit(f"Error: There was a problem with import of the module/package: {error.name}.")


def cache_news(cache_list):
    # create cached_news.pkl file to store the caching info in it
    cache = os.path.join(cached_news_directory, "cached_news.pkl")
    # checks to make sure the cache file already exist, and if does, the new data to be
    # cached is appended the older file
    if os.path.isfile(cache):
        a_file = open(cache, "rb")
        saved_news = pickle.load(a_file)
        cache_list = [*cache_list, *saved_news]
        cache_file = open(cache, "wb")
        logging.info("Appending the feeds cache to existing cached news")
        pickle.dump(cache_list, cache_file)
        cache_file.close()
    else:
        # if the cache info file does not exist, create a new file for caching the info
        logging.info("Creating a new cache info file.")
        a_file = open(cache, "wb")
        pickle.dump(cache_list, a_file)
        a_file.close()


def retrieve_cache():
    """ retrieves the cached news in a file

    Returns:
        pickle.load(a_file) (list): the loaded list of feeds info

    """
    logging.info("retrieving cache")
    cache = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cached_news', "cached_news.pkl"))
    try:
        a_file = open(cache, "rb")
        logging.info("Retrieving the cache.")
        return pickle.load(a_file)
    except FileNotFoundError:
        logging.error("There is no cached news feed!")
        raise SystemExit()


def find_item(selected_date, limit, input_rss_url):
    """ Selects the news after the specified date

    This function selects the news from the retrieved list that satisfy
    the date condition, and if the selected mode is not json, then prints it
    in the regular format

    Args:
        selected_date (str): the input date the user wants to see news feeds from
        limit: number of cached news specified by the user to be shown
        input_rss_url (str): the RSS URL input by the user

    Returns:
        selected_news (dict): a dictionary of cached news created based on the number limit
                              and date
        news_list (list): a list of cached news created based on the number limit
                              and date

    """
    news_id = 0
    # the news items from the cached news is stored in the selected news
    # dictionary after picked by the specified date by the user
    logging.info("Finding news.")
    selected_news = {}
    cached_news = retrieve_cache()

    # setting the number of cached news to be printed based on the limit input
    if limit is None:
        limit = len(cached_news)
    else:
        limit = min(limit, len(cached_news))

    news_list = []
    for item in cached_news:
        news_date = item[0]
        # checking to see if the news publish date is the specified date
        if time_in_range(selected_date, news_date):
            if input_rss_url is not None:
                rss_source = item[1].get("rss_source")
                # if user has specified a URL source, checking to see if the feed is from that source
                if rss_source == input_rss_url:
                    news_id += 1
                    selected_news["News Number " + str(news_id)] = item[1]
                    news_list.append(item)
                    if len(news_list) == limit:
                        break
            else:
                news_id += 1
                selected_news["News Number " + str(news_id)] = item[1]
                news_list.append(item)
                if len(news_list) == limit:
                    break
    # selected news is for json format printing
    # news_list is for normal format printing
    return selected_news, news_list


def clear_cache():
    """ deletes the cache file

    Returns:
        None
    """
    try:
        shutil.rmtree(cached_news_directory)
        logging.info("cache cleared!")
    except NotADirectoryError:
        logging.error("No cached news exist!")
        raise SystemExit()


def show_cache_by_date(selected_date, json, limit, html, pdf, input_rss_url):
    """ prints the cached news based on the number limit and date

    with the specified printing format and number of news and selected date
    prints the cached news feed

    Args:
        selected_date(str): date chosen by user for the news to be shown after that
        json (boolean): printing mode specified by the user
        limit (int): number of cached news specified by the user to be shown
        html (str): the path in which the html file should be stored
        pdf (str): the path in which the pdf file should be stored
        input_rss_url (str): the RSS URL input by the user

    Returns:
        None
    """
    selected_news, cached_news_by_date = find_item(selected_date, limit, input_rss_url)
    if len(cached_news_by_date) == 0:
        raise SystemExit("There is no news feed in the specified date!")

    if json:
        print_json_format(selected_news)
        if html is not None:
            logging.info("Converting the cached news into HTML.")
            convert_html(cached_news_by_date, html)

        if pdf is not None:
            logging.info("Converting the cached news into PDF.")
            convert_pdf(cached_news_by_date, pdf)
    else:
        for item in cached_news_by_date:
            print_regular_format(item[1])
        if html is not None:
            logging.info("Converting the cached news into HTML.")
            convert_html(cached_news_by_date, html)

        if pdf is not None:
            logging.info("Converting the cached news into PDF.")
            convert_pdf(cached_news_by_date, pdf)
