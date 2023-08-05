import datetime
from typing import Union


def date_to_datestring(day: Union[str, datetime.date]) -> str:
    """Convert a date to a %y%m%d formatted string.

    Parameters
    ----------
    day : Union[str, datetime.date]
        The date to convert. If day is a string, it should be
        formatted '%Y-%m-%d'

    Returns
    -------
    datestring : str
        The date formatted %y%m%d. For example November 9, 2020 would
        be formatted 201109.
    """
    if isinstance(day, str):
        date_time_obj = datetime.datetime.strptime(day, '%Y-%m-%d')
        date_string = date_time_obj.strftime('%y%m%d')
    else:
        date_string = day.strftime('%y%m%d')
    return date_string
