""" Handles the time and date related operations

Functions:
    date_print_format(date): converts the date string into a particular format
    time_in_range(selected_date, news_time): Checks if the feeds date is the day user has specified
    date_object(date): Given a date in string format, returns a datetime object for date operations

"""

try:
    from datetime import datetime, timedelta
    import dateutil.parser
except ImportError as error:
    raise SystemExit(f"Error: There was a problem with import of the module/package: {error.name}.")


def date_print_format(date):
    """ converts the date string into a particular format

    example timestamp in such format:
    Thu, 21 Apr 2022 09:25:02 +0000

    Args:
        date (str): URL of the news page

    Returns:
        date (str): formatted date
    """

    date_format = "%a, %d %b %Y %H:%M:%S %z"
    # RSS files dates are in iso format, to parse them:
    date = dateutil.parser.isoparse(date)
    date = date.strftime(date_format)
    return date


def time_in_range(selected_date, news_time):
    """ Checks if the feeds date is the day user has specified

    Args:
        selected_date (str): specified date by the user
        news_time (str): feeds date to be tested to be in the same day of the selected date

    Returns:
        (Boolean): whether the selected date is the specified date or not

    """
    selected_date = date_object(selected_date)
    news_date = dateutil.parser.parse(news_time).replace(tzinfo=None)
    delta = timedelta(hours=23, minutes=59, seconds=59, microseconds=999999)
    end_date = selected_date + delta
    if selected_date <= news_date <= end_date:
        return True
    else:
        return False


def date_object(date):
    """Given a date in string format, returns a datetime object for date operations

    Args:
        date (str): date in string format

    Returns:
        datetime.strptime(date, "%Y%m%d")(datetime): date object of the given string
    """

    # convert the string into a date object
    return datetime.strptime(date, "%Y%m%d")
