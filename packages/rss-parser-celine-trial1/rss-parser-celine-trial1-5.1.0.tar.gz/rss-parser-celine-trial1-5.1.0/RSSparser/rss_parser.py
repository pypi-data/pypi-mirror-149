""" Handles the reading arguments of CLI utility and program flow. """


# as sometimes there are problems with python environment variables, if module is not found
# because sys.path is not looking at the right place, we catch that exception and set the sys.path as
# as the directory of the project
for i in range(2):
    try:
        import argparse
        import logging
        from RSSparser.cache_news import show_cache_by_date, clear_cache
        from RSSparser.RSSItems import RSSItems
        from RSSparser.convert_format import convert_html, convert_pdf
        from RSSparser import __version__, set_verbose, colorize
    except ModuleNotFoundError as error:
        if i == 1:
            raise SystemExit(f"ERROR: Program halting as module {error.name} is not found/Does not exist.")
        import os
        import sys
        sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    # this section might be redundant
    except ImportError as error:
        raise SystemExit(f"Error: There was a problem with import of the module/package: {error.name}.")

    else:
        break


def main():
    parser = argparse.ArgumentParser(description="Pure Python command-line RSS reader.")
    parser.add_argument("--version", action="store_true", help="Print version info")
    parser.add_argument("--json", action="store_true", help="Print result as JSON in stdout")
    parser.add_argument("--verbose", action="store_true", help="Outputs verbose status messages")
    parser.add_argument("--limit", help="Limit news topics if this parameter provided", type=int)
    parser.add_argument("source", nargs='?', help="RSS URL")
    parser.add_argument("--date", help="Show cached news published after date")
    # parser.add_argument("--clear", action="store_true", help="Clears cache.")
    parser.add_argument("--to-html", help="Converts and stores in HTML at the user-provided path.")
    parser.add_argument("--to-pdf", help="Converts and stores in PDF at the user-provided path.")
    parser.add_argument("--colorize", action="store_true", help="Colorize the CLI output.")
    args = parser.parse_args()

    # set the verbose globally in the __init__.py file
    set_verbose(args.verbose)

    # # additional feature
    # if args.clear:
    #     clear_cache()

    if args.colorize is True:
        colorize()

    # if the version flag is set, print the version and exit the program
    if args.version:
        print(f"version: {__version__}")
        logging.info("Version printed, exiting the program.")
        # if the version flag is set, the only required performance of
        # the app is to show the version and exit, hence:
        exit()

    if args.source is not None:
        if args.date is None:
            # given only RSS URL and probably other options without specified date
            # printing RSS feed and caching them and converting if the options are set
            rss = RSSItems(args.source, args.json, args.limit)
            rss.print_feed()
            if args.to_html is not None:
                convert_html(rss.cache_list, args.to_pdf)
            if args.to_pdf is not None:
                convert_pdf(rss.cache_list, args.to_pdf)
        else:
            # given RSS URL and date
            # print and/or convert cached news feed based on json and limit options
            show_cache_by_date(args.date, args.json, args.limit, args.to_html, args.to_pdf, args.source)

    else:
        # missing RSS URL
        if args.date is not None:
            # showing cached data in specified date, based on limit and json and html/pdf options
            show_cache_by_date(args.date, args.json, args.limit, args.to_html, args.to_pdf, args.source)
        else:
            if args.date is None:
                # if neither date nor RSS URL is provided, the program exits with an error.
                raise SystemExit("Error: Either RSS URL or date for cached news must be input. Please enter either.")


if __name__ == "__main__":
    main()
