""" Converts a list of news into pdf or html

Functions:
    get_cached_content_paths(cache_path): Given the cache directory of a feed, returns paths to article, images and
                                          links files
    get_conversion_data(item): Extracts the news feed info given it's dictionary
    convert_pdf(news_tuples_list, input_path): Converts a list of news into pdf format
    convert_html(news_tuples_list, input_path): Converts a list of news into HTML format

"""

try:
    import json
    import logging
    import os
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
except ImportError as error:
    raise SystemExit(f"Error: There was a problem with import of the module/package: {error.name}.")


def get_cached_content_paths(cache_path):
    """ Given the cache directory of a feed, returns paths to article, images and links files

    Args:
        cache_path: cache directory of a single feed

    Returns:
        article_path (str): path to the text file containing the article
        images_paths (list): a list of paths in string referring to the images downloaded from the news article
        links_path (str): path to the text file containing the links extracted from the feed's news article

    """
    article_path = None
    links_path = None
    images_paths = []
    items = os.listdir(cache_path)
    for item in items:
        # item is a tuple, with first element being the date and the second
        # element being the feed's dictionary
        if item.endswith("images"):
            for image in os.listdir(os.path.abspath(os.path.join(cache_path,  item))):
                images_paths.append(os.path.join(cache_path, 'images', image))
        elif item == "links.txt":
            links_path = os.path.abspath(os.path.join(cache_path, item))
        else:
            article_path = os.path.abspath(os.path.join(cache_path, item))
    return article_path, images_paths, links_path


def get_conversion_data(item):
    """ Extracts the news feed info given it's dictionary

    Args:
        item (dict): dictionary of cached feed content

    Returns:
        title (str): the title of feed's news
        date (str): the published date of the news
        article: new's article
        images_paths (list): downloaded images path list
        links_list (list): list of links in the article

    """
    news = item[1]
    # cache directory of the feed
    directory = news.get("cache_directory")
    article_path, images_paths, links_path = get_cached_content_paths(directory)
    with open(article_path, encoding="utf-8") as f:
        lines = f.read()
    # news article extracted
    article = lines
    with open(links_path, 'r') as f:
        links_list = json.loads(f.read())
    title = news.get("title")
    date = news.get("date")
    return title, date, article, images_paths, links_list


def convert_pdf(news_tuples_list, input_path):
    """ Converts a list of news into pdf format

    Args:
        news_tuples_list: list of feed info in a tuple structure
        input_path: the path in which the converted pdf should be stored

    Returns:
        None

    """
    doc = SimpleDocTemplate(input_path, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    news_id = 0
    Story = []
    for item in news_tuples_list:
        title, date, article, images_paths, links_list = get_conversion_data(item)
        logging.info("feed's content retrieved for conversion")
        news_id += 1

        # Structuring the pdf file
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        ptext = '<b>News Number:  </b>: %s' % news_id
        Story.append(Spacer(1, 12))
        Story.append(Paragraph(ptext, styles["Normal"]))
        ptext = '<b>Title</b>: %s' % title
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        ptext = '<b>Date</b>: %s' % date
        Story.append(Paragraph(ptext, styles["Normal"]))
        Story.append(Spacer(1, 12))
        ptext = '<b>Article</b>: %s' % article
        Story.append(Paragraph(ptext, styles["Justify"]))
        Story.append(Spacer(1, 12))

        for pic in images_paths:
            im = Image(pic, 2 * inch, 2 * inch)
            Story.append(im)
        Story.append(Spacer(1, 12))
        Story.append(Spacer(1, 12))
        for link in links_list:
            ptext = '<a href = %s >Link</a>' % link
            Story.append(Paragraph(ptext, styles["Normal"]))

    doc.build(Story)


def convert_html(news_tuples_list, input_path):
    """ Converts a list of news into HTML format

    Args:
        news_tuples_list: list of feed info in a tuple structure
        input_path: the path in which the converted HTML should be stored

    Returns:
        None

    """

    news_id = 0
    body = ""
    for item in news_tuples_list:
        news_id += 1
        title, date, article, images_paths, links_list = get_conversion_data(item)
        logging.info("feed's content retrieved for conversion")
        # structuring the html file
        text = "<h2>News Number {News_id}</h2><p><b>Title: </b>{Title}<br><b>Date: </b>{Date}<br><b>Article: " \
               "</b>{Article}<br></p>"
        text = text.format(News_id=news_id, Title=title, Date=date, Article=article)
        for image_path in images_paths:
            text = text + '<img src = {Image_Path} width="200" height="250" style="vertical-align:' \
                          'middle;margin:0px 5px">'.format(Image_Path=image_path)
        n = 0
        for link in links_list:
            n += 1
            text = text + "<p><a href={Link}>link number {N}</a></p>".format(Link=link, N=n)
        body = body + text
    text = '''<html><body>{Text}</body></html>'''.format(Text=body)

    if not input_path.endswith(".html"):
        logging.error("Input path is not ending with .html")
        raise SystemExit('ERROR: Path extension must be .html')

    # creating the file
    try:
        file = open(input_path, "w",  encoding="utf-8")
        file.write(text)
        file.close()

    except FileNotFoundError:
        logging.error("Provided path is not correct.")
        raise SystemExit('Path is not correct. Please Input a correct Path.')
