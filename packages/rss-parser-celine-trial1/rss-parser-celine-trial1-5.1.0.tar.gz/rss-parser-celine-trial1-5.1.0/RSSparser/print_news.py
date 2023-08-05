""" Handles the printing of the feeds

Functions:
    wrap_text(text): makes sure the line lengths are no more than 120 for the input
    print_json_format(dictionary): Prints the content of the feeds dictionary in json format
    print_regular_format(dic_temp): Prints the content of the feeds dictionary in regular format

"""

try:
    import logging
    import textwrap
    from RSSparser import color_mood
except ImportError as error:
    raise SystemExit(f"Error: There was a problem with import of the module/package: {error.name}.")

# if user has input colorize option, print the output with colored format
if color_mood:
    from rich import print


def wrap_text(text):
    """ makes sure the line lengths are no more than 120 for the input

    Args:
        text (str): text to be formatted in the lines of length 120

    Returns:
        (str): formatted text
    """
    return '\n'.join(textwrap.wrap(text, 100))


def print_json_format(dictionary):
    """ Prints the content of the feeds dictionary in json format

    Args:
    dictionary: a dictionary of RSS items including title, date, news content...

    Returns:
    None
    """

    # Approach number 1
    # manually printing the feeds dictionary in json format
    logging.info("Printing the feed in json\n")
    print("{")
    i = 0
    for item in dictionary.keys():
        i += 1
        print(f'\n\t"{item}": {{')
        for item_item in dictionary[item].keys():
            if item_item == "title":
                title = '\n\t\t          '.join(textwrap.wrap(dictionary[item].get(item_item), 80))
                print(f'\t\t"{item_item}": "{title}"')
            elif item_item == "date":
                print(f'\t\t"{item_item}": "{dictionary[item].get(item_item)}"')
            elif item_item == "link":
                link = '\n\t\t        '.join(textwrap.wrap(dictionary[item].get(item_item), 80))
                print(f'\t\t"{item_item}": "{link}"')
            elif item_item == "content":
                content = '\n\t\t           '.join(textwrap.wrap(dictionary[item].get(item_item), 80))
                print(f'\t\t"{item_item}": "{content}"')
            elif item_item == "image_link":
                img_link = '\n\t\t              '.join(textwrap.wrap(dictionary[item].get(item_item), 80))
                print(f'\t\t"{item_item}": "{img_link}"')

        if i != len(dictionary):
            print("\t},")
        else:
            print("\t}")
    print("}")

    # Approach number 2

    # out_file = open("test2.json", "w")
    # json.dump(json_dit, out_file, indent=4)
    # out_file.close()

    # myfile = open("test2.json")
    # txt = myfile.read()
    # print(txt)
    # myfile.close()

    # import os
    # os.remove("test2.json")


run_once = 0


def print_regular_format(dictionary):
    """ Prints the content of the feeds dictionary in regular format

    Args:
        dictionary (dict): a dictionary of RSS items including title, date, news content...

    Returns:
            None
    """
    global run_once
    if run_once == 0:
        logging.info("Printing the RSS feed")
        run_once += 1

    print("------------------------------------------------------------------------------------")
    print(f"Title: {wrap_text(dictionary.get('title'))}")
    print(f"Date: {wrap_text(dictionary.get('date'))}")
    print(f"Link: {wrap_text(dictionary.get('link'))}\n")
    if dictionary.get('image_link') is not None:
        print(f"[image: {wrap_text(dictionary.get('title'))}][2]\n{wrap_text(dictionary.get('content'))}[1]\n\n")
    else:
        print(f"{wrap_text(dictionary.get('content'))}[1]\n\n")
    print(f"[1]: {wrap_text(dictionary.get('link'))} (link)")

    if dictionary.get('image_link') is not None:
        print(f"[2]: {wrap_text(dictionary.get('image_link'))} (image)\n\n")
