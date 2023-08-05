""" Fetches and extracts data from RSS URL and news USLs

Functions:
    extract_XML(url): Given the RSS url, fetches the XML content
    extract_images(soup):  Extracts the path of images in the article of a news page
    download_images(soup, feed_cache_directory): Given the BeautifulSoup object, downloads the images within the
                                                     article of a news page
    extract_links(soup, feed_cache_directory): Given the BeautifulSoup object of a news feed, extracts the links in
                                                   the article of a news page
    extract_article(soup): Given the BeautifulSoup object of a news feed, extracts the article of the feed
    
"""

try:
    import os
    from bs4.element import NavigableString
    import requests
    from bs4 import BeautifulSoup
    import shutil
    import logging
    import json
    import re
    from RSSparser.prepare_data import get_encoding
except ImportError as error:
    raise SystemExit(f"Error: There was a problem with import of the module/package: {error.name}.")


def extract_XML(url):
    """Given the RSS url, fetches the XML content

    The content is then stored in a file names rss.xml

    Args:
        url (str): RSS URL provided by the user

    Returns:
        media_namespace (str): media namespace extracted from XML file
    """
    try:
        logging.info("Requesting the URL webpage")
        response = requests.get(url)
    except requests.exceptions.RequestException:
        logging.error("Fetching was unsuccessful.")
        raise SystemExit("Error: Please insert the correct RSS URL again or Check internet connectivity.")
    else:
        logging.info("Webpage retrieved successfully!")

    # storing the XML content in rss.xml file
    xml = os.path.abspath(os.path.join(os.path.dirname(__file__), 'rss.xml'))
    with open(xml, 'wb') as file:
        file.write(response.content)

    # for the image URL, media namespace is required to be extracted from the XML file
    try:
        media_namespace = re.search('(?<=media=\").*?(?=\")', response.content.decode('utf-8')).group()
    except AttributeError:
        media_namespace = None

    return media_namespace


def extract_images(soup):
    """ Extracts the path of images in the article of a news page

    Given a BeautifulSoup object, extracts the path of the images in the article of a news page.

    Args:
        soup (BeautifulSoup object): HTML page parsed into its elements

    Returns:
        images (list): a list of paths of images in the news article
    """
    images = []
    try:
        for image in soup.find("article").find_all("img"):
            images.append(image.attrs.get("src"))
    except AttributeError:
        images = None
    return images


def download_images(soup, feed_cache_directory):
    """ Given the BeautifulSoup object, downloads the images within the article of a news page

    Args:
        soup (BeautifulSoup object): HTML page parsed into its elements
        feed_cache_directory (str): the path to which the cache content of a feed is stored

    Returns:
        None

    """
    images_url_list = extract_images(soup)
    if images_url_list is not None:
        image_id = 0
        images_dir = os.path.abspath(os.path.join(feed_cache_directory, 'images'))
        # creating a directory in the feed's directory to download the images in
        logging.info("Creating a directory for feed's images.")
        if not os.path.isdir(images_dir):
            os.makedirs(images_dir)
        logging.info("Downloading article's images in images directory for the feed.")
        for url in images_url_list:
            if url is not None and url.startswith("http"):
                r = requests.get(url, stream=True)
                if r.status_code == 200:
                    image_id += 1
                    image_name = "image_" + str(image_id) + ".jpg"
                    with open(os.path.abspath(os.path.join(images_dir, image_name)), 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)


def extract_links(soup, feed_cache_directory):
    """ Given the BeautifulSoup object of a news feed, extracts the links in the article of a news page

    Args:
        soup (BeautifulSoup object): HTML page parsed into its elements
        feed_cache_directory (str): the path to which the cache content of a feed is stored

    Returns:
        None

    """
    links = []
    logging.info("Extracting the links from HTML")
    try:
        for item in soup.find("article").find_all("a"):
            link = item.attrs.get("href")
            if link.startswith("https") or link.startswith("http"):
                links.append(link)
    except AttributeError:
        links = None

    # Creating a text file to store the links in it
    logging.info("Writing the links in a text file in the feed's cache directory.")
    if links is not None:
        with open(os.path.abspath(os.path.join(feed_cache_directory, 'links.txt')), 'w') as f:
            f.write(json.dumps(links))


def extract_article(soup):
    """ Given the BeautifulSoup object of a news feed, extracts the article of the feed

    Args:
        soup (BeautifulSoup object): HTML page parsed into its elements

    Returns:
        article (str): the extracted article of a feed

    """
    article = ""
    string_type = NavigableString
    # string corresponds to a bit of text within a tag. Beautiful Soup uses the NavigableString class to contain
    # these bits of text
    logging.info("Extracting the article from HTML")
    try:
        for paragraph in soup.find("article").find_all("p"):
            if isinstance(paragraph.next_element, string_type):
                article = article + "\n" + paragraph.next_element
    except AttributeError:
        logging.error("Article Not Found")
        article = None

    return article
