""" Contains the class RSSItem"""

try:
    import logging
    import os
    from RSSparser.fetch_data import extract_XML, extract_article
    from RSSparser.prepare_data import parse_XML, get_content
    from RSSparser.RSSFeed import RSSFeed
    from RSSparser.print_news import print_json_format, print_regular_format
    from RSSparser.cache_news import cache_news as cache
    from RSSparser import cached_news_directory
except ImportError as error:
    raise SystemExit(f"Error: There was a problem with import of the module/package: {error.name}.")


class RSSItems:
    """ Given a RSS URL, this class handles the parsing and managing the feeds extraction

    Instance variables:
        title (str): the title of the RSS feeds
        URL (str): the RSS URL string provided by the user
        json (boolean): the option for printing the feeds
        root (XML element): The root of the XML tree after being parsed
        items (XML element): the xml elements containing the news items
        cache_list (list): for each RSS page, the structured RSS feed items
                           info in list to be cached
        length (int): number of RSS feeds item extracted from the XML
        limit (int): number of feeds to be printed
        rss_items (list): a list of RSSFeed objects, corresponding to RSS news feeds items
        json_dictionary (dict): news feed in the json format

    Instance methods:
        parse_xml(self): Reads the rss.xml file and parses it
        set_rss_elements(self): creating an RSSFeed object for each XML news item
        feeds_number(self, limit): Determines number of feeds to be printed
        create_cache_directory(self): Creates a directory to store cache directories of RSS items in it
        create_json_dictionary(self): Creates the json format dictionary
        print_feed(self): Prints the feed in normal or json format
        def create_cache_list(self): For the current RSS items, creates a cache_list to be cached or converted
        def cache_news(self): caches the news provided in the cache_list

    """

    def __init__(self, rss_url, json, limit):
        self.title = None
        self.URL = rss_url
        self.json = json
        self.root = None
        self.items = None
        self.cache_list = []
        self.media_namespace = extract_XML(rss_url)
        self.length = None
        self.parse_xml()
        self.limit = self.feeds_number(limit)
        self.rss_items = []
        self.json_dictionary = {}
        self.create_cache_directory()
        self.set_rss_elements()
        self.create_json_dictionary()
        self.create_cache_list()
        self.cache_news()

    def parse_xml(self):
        """ Reads the rss.xml file and parses it

        After parsing the XMl file, sets the items and root instance variables
        also sets the length of the items

        Returns:
            None

        """
        self.root, self.items = parse_XML()
        self.length = len(self.items)

    def set_rss_elements(self):
        """ creating an RSSFeed object for each XML news item

        Returns:
            None

        """
        element_iterator = iter(self.items)
        # creating an RSSFeed object for each XML news item
        for count in range(self.limit):
            element = next(element_iterator)
            self.rss_items.append(RSSFeed(element, self.URL, self.media_namespace))

    def feeds_number(self, limit):
        """ Determines number of feeds to be printed

        Based on the limit input by the user, this number is calculated

        Args:
            args.limit (int): the number limit input by the user

        Returns:
            limit: number of feeds to be printed
        """
        # limit variable: if the user does not provide a value for it
        # or the value is larger than feeds size then user gets all available news feeds
        if limit is None:
            limit = self.length
        else:
            limit = min(self.length, limit)
        return limit

    @staticmethod
    def create_cache_directory():
        """ Creates a directory to store cache directories of RSS items in it

        Returns:
            None

        """

        # check to see if the directory already does not exist
        if not os.path.isdir(cached_news_directory):
            os.makedirs(cached_news_directory)
            # initiating the cache folder id 0 for the feeds' cache folders
            cache_id = "0"
            # storing the counting number in a text file for program's next runs
            cache_id_path = os.path.abspath(os.path.join(cached_news_directory, "cache_id.txt"))
            with open(cache_id_path, 'w') as file:
                file.write(cache_id)

    def create_json_dictionary(self):
        """ Creates the json format dictionary

        Returns:
            None

        """
        news_id = 0
        for items in self.rss_items:
            news_id += 1
            news_key = "News Number: " + str(news_id)
            self.json_dictionary[news_key] = items.dictionary

    def print_feed(self):
        """ Prints the feed in normal or json format

        Returns:
            None

        """
        if self.json:
            print_json_format(self.json_dictionary)
        else:
            for item in self.rss_items:
                print_regular_format(item.dictionary)

    def create_cache_list(self):
        """ For the current RSS items, creates a cache_list to be cached or converted

        Returns:
            None

        """
        for item in self.rss_items:
            self.cache_list.append(item.cache_tuple)

    def cache_news(self):
        """ caches the news provided in the cache_list

        Returns:
            None

        """
        cache(self.cache_list)
