""" Contains the class RSSFeed """
try:
    import logging
    import os
    import requests
    from RSSparser.fetch_data import extract_article
    from RSSparser.fetch_data import download_images as dl_img
    from RSSparser.prepare_data import get_content, get_soup
    from RSSparser.date_time import date_print_format
    from RSSparser.fetch_data import extract_links as dl_lnk
except ImportError as error:
    raise SystemExit(f"Error: There was a problem with import of the module/package: {error.name}.")


class RSSFeed:
    """
    RSSFeed class correspond to one news feed and handles its data and operations

    RSSFeed class is instantiated when RSS URL is given by the user and after parsing and
    extracting info belonging two each feed item, the info is saved and process in this method.

    Instance variables:
        element (XML element): XML element that has been parsed and passed to the instance
        rss_source (str): The RSS URL from which the news feed is extracted
        title (str): titles of the news feed
        date (str): published date of the feed
        link (str): link of the news feed
        content (str): content of the rss feed
        image_link: (str): if the feed has an image, this is its link
        cache_directory (str): the path in which the cached items are stored for the feed
        dictionary (dict): each news feed is converted to a dictionary, this is the feed dictionary
        cache_tuple (tuple): each news feed info is cached in a tuple structure, first item being
                             the published date, and the second element the feed dictionary.
        soup (BeautifulSoup object): parsed HTML object of the feed news page
        article (string): The article in the feed's news page

    Class Methods:
        set_soup(self.link): fetches hte feed's news page and parses in
        get_feed_fields(self): Extracts the info of the news feed
        create_cache_directory(): Creates a directory for storing the cached content
        create_dict(self): Creates a dictionary for each feed based on its extracted info
        create_cache_tuple(self): Creates a tuple with the published date and the dictionary for each feed
        download_article(self): Given the news link for each feed's news page, downloads its article in a text file.
        download_images(self): Given the news link for each feed's news page, downloads its article's
                               images in a folder.
        download_links(self): Given the news link for each feed's news page, downloads its article's
                              links in a text file.

    """

    def __init__(self, item, rss_source, media_namespace):
        """ RSSFeed class constructor

        Args:
            item (XML element): XML element after it has been parsed and extracted and passed
            rss_source: the RSS URL in which the feed is taken from
        """
        self.element = item
        self.rss_source = rss_source
        self.title = None
        self.date = None
        self.link = None
        self.content = None
        self.image_link = None
        self.media_namespace = media_namespace
        self.cache_directory = self.create_cache_directory()
        self.dictionary = None
        self.cache_tuple = None
        self.get_feed_fields()
        self.soup = self.set_soup()
        self.article = extract_article(self.soup)
        self.create_dict()
        self.create_cache_tuple()
        self.download_article()
        self.download_images()
        self.download_links()

    def set_soup(self):
        """ Parses the HTML structure of the webpage of the feed news

        Returns:
            BeautifulSoup object
        """
        return get_soup(self.link)

    def get_feed_fields(self):
        """ Extracts the info of the news feed

        This method extracts title, date, link, content, image link of the feed
        form the XML element.

        Returns:
            None

        """

        # for each news item, extracting info and save them in a temporary dictionary to add then
        # to the feeds dictionary
        try:
            self.title = self.element.find("title").text
            self.link = self.element.find("link").text
            self.content = get_content(self.link)

            try:
                date = self.element.find("pubDate").text
                self.date = date_print_format(date)
            except ValueError:
                self.date = self.element.find("pubDate").text

            # as far as i've seen, the image URL in RSS XML are paired with a media namespace
            # so this implementation assumes there is no other way for an Image URL for news items in XML file
            try:
                self.image_link = self.element.find('{{{ns}}}content'.format(ns=self.media_namespace)).get("url")
            except AttributeError:
                try:
                    self.image_link = self.element.find('{{{ns}}}thumbnail'.format(ns=self.media_namespace)).get("url")
                except AttributeError:
                    self.image_link = None

        except AttributeError:
            logging.debug("Tag names were not found!")
            logging.error("RSS  info is not in proper shape!")
            raise SystemExit("RSS XML structure is not correct.")
        except requests.exceptions.RequestException:
            logging.error("Fetching was unsuccessful. Content of the feed is not printed for this news.")

    @staticmethod
    def create_cache_directory():
        """ Creates a directory for storing the cached content

        This method creates a directory for each feed item

        Returns:
            the path to the cache directory of the feed
        """

        # Creating a directory for the cached content
        cache_id_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cached_news', 'cache_id.txt'))
        # naming the directories for different feeds in incremental order
        # and storing the folder number to be restored and used for next runs of the program
        with open(cache_id_path, 'r') as file:
            cache_id = file.read()
        cache_id = int(cache_id) + 1
        with open(cache_id_path, 'w') as file:
            file.write(str(cache_id))

        # naming the directories as feed_n: n being the number
        directory_name = "feed_" + str(cache_id)
        directory_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'cached_news', directory_name))
        # checking if there is no directory with the same name, after that creating the directory
        if not os.path.isdir(directory_path):
            os.makedirs(directory_path)
        return os.path.abspath(os.path.join(os.path.dirname(__file__), 'cached_news', directory_name))

    def create_dict(self):
        """ Creates a dictionary for each feed based on its extracted info

        The information of each news feed is stored in this dictionary, as well as the cache directory

        Returns:
            None

        """
        if self.image_link is not None:
            self.dictionary = {"title": self.title,
                               "date": self.date,
                               "link": self.link,
                               "content": self.content,
                               "image_link": self.image_link,
                               "cache_directory": self.cache_directory,
                               "rss_source": self.rss_source}
        else:
            self.dictionary = {"title": self.title,
                               "date": self.date,
                               "link": self.link,
                               "content": self.content,
                               "cache_directory": self.cache_directory,
                               "rss_source": self.rss_source}

    def create_cache_tuple(self):
        """ Creates a tuple with the published date and the dictionary for each feed

        Returns:
            None

        """
        self.cache_tuple = (self.date, self.dictionary)

    def download_article(self):
        """ Given the news link for each feed's news page, downloads its article in a text file.

        Returns:
            None

        """
        article_path = os.path.abspath(os.path.join(self.cache_directory, 'article.txt'))

        if self.article is not None:
            with open(article_path, 'w', encoding="utf-8") as file:
                file.write(self.article)
        else:
            self.article = "Article was not found."

    def download_images(self):
        """ Given the news link for each feed's news page, downloads its article's images in a folder.

        Returns:
            None

        """
        dl_img(self.soup, self.cache_directory)

    def download_links(self):
        """ Given the news link for each feed's news page, downloads its article's links in a text file.

        Returns:
            None

        """
        dl_lnk(self.soup, self.cache_directory)
