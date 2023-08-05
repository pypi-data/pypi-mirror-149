""" Prepare the data of the news to be printed as the RSS feeds

This modules fetches the XML content of the URL provided by the user,
parses it into XML tree elements, extracts some data from
this tree

Functions:
    get_encoding(soup): Checks the encoding of the html file of the news page
    get_content(news_link): Extracts the content summary of the news page
    extract_XML(URL): Given the RSS url, fetches the XML content
    parse_XML(): Parses the XML file
    get_soup(news_link): Extracts the content summary of the news page
    print_RSS_title(root): Prints the title of the RSS file before the feed

"""

try:
    import xml.etree.ElementTree as ET
    import requests
    import json
    import logging
    from bs4 import BeautifulSoup
    import re
    from datetime import datetime
    import os
except ImportError as error:
    raise SystemExit(f"Error: There was a problem with import of the module/package: {error.name}.")


def get_encoding(soup):
    """ Checks the encoding of the html file of the news page

    Args:
        soup (BeautifulSoup object): html parsed object with BeautifulSoup
                                     function of bs4 library

    Returns:
        encode (str): the encoding extracted from the html
    """
    # getting the encoding from the soup object (html parsed object)
    logging.info("Getting the encoding of the HTML webpage of the news.")
    if soup and soup.meta:
        encode = soup.meta.get('charset')
        if encode is None:
            encode = soup.meta.get('content-type')
            if encode is None:
                content = soup.meta.get('content')
                match = re.search('charset=(.*)', content)
                if match:
                    encode = match.group(1)
                else:
                    raise ValueError('unable to find encoding')
    else:
        logging.error("Encoding was not found.")
        raise ValueError('unable to find encoding')
    return encode


def get_content(news_link):
    """ Extracts the content summary of the news page

    Args:
        news_link (str): URL of the news page

    Returns:
        content.attrs.get("content") (str): the summary of the content
                                            of the news page
    """

    try:
        logging.info("Getting the content of the news feed.")
        page = requests.get(news_link)
        text = page.content
        # parsing the content of the webpage into
        # html string
        soup = BeautifulSoup(text, "html.parser")
        # parsing the content of the webpage, this time with the
        # recognized encoding
        soup = BeautifulSoup(text, "html.parser", from_encoding=get_encoding(soup))
        content = soup.find("meta", attrs={"name": "description"})
        logging.info("Content extracted successfully.")
        return content.attrs.get("content")

    except ValueError:
        # if the get_encoding function is unable to provide
        # correct encoding, continue with the defaults of
        # BeautifulSoup function
        logging.warning("The encoding might not be correct!")
        page = requests.get(news_link)
        text = page.content
        soup = BeautifulSoup(text, "html.parser")
        content = soup.find("meta", attrs={"name": "description"})
        return content.attrs.get("content")


def parse_XML():
    """Parses the xml file

    Reads the rss.xml file and parses it into XML elements in tree structure

    Returns:
        root: root node of the XML tree
        items: feed nodes of the XML tree
    """

    # Parses the XML into element tree
    # and extracts the root of the tree
    try:
        xml = os.path.abspath(os.path.join(os.path.dirname(__file__), 'rss.xml'))
        tree = ET.parse(xml)
    except ET.ParseError:
        logging.error("Parsing was unsuccessful.")
        raise SystemExit("Error: RSS XML is not in correct structure.")
    else:
        logging.info("RSS file Parsed successfully!")

    root = tree.getroot()

    # creating a list of all items(titles) in the RSS file
    # in the RSS file, the titles are wrapped in elements
    # with the tag: item
    try:
        items = root.find("channel").findall("item")
    except AttributeError:
        logging.debug("Couldn't find channel tag!")
        logging.error("RSS info is not in proper shape!")
        raise SystemExit("Error: Please insert the RSS URL again.")
    return root, items


def get_soup(news_link):
    """ Extracts the content summary of the news page

    Args:
        news_link (str): URL of the news page

    Returns:
        content.attrs.get("content") (str): the summary of the content
                                            of the news page
    """

    try:
        page = requests.get(news_link)
        text = page.content
        # parsing the content of the webpage into
        # html string
        soup = BeautifulSoup(text, "html.parser")
        # parsing the content of the webpage, this time with the
        # recognized encoding
        soup = BeautifulSoup(text, "html.parser", from_encoding=get_encoding(soup))
        soup.prettify()
        return soup

    except ValueError:
        # if the get_encoding function is unable to provide
        # correct encoding, continue with the defaults of
        # BeautifulSoup function
        page = requests.get(news_link)
        text = page.content
        soup = BeautifulSoup(text, "html.parser")
        return soup


def print_rss_title(root):
    """Prints the title of the RSS file before the feed

    Args:
        root: root of the parsed XML tree

    Returns:
        None
    """

    try:
        feed = root.find("channel").find("title").text
        print(feed)
    except AttributeError:
        logging.debug("Couldn't find channel tag!")
        logging.error("RSS  info is not in proper shape!")
        raise SystemExit("Error: Please insert the RSS URL again.")
