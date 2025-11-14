"""Functions for working with dates."""

from datetime import datetime, date


def convert_to_datetime(date_val: str) -> datetime:
    """Converts string date values to datetime objects."""
    try:
        return datetime.strptime(date_val, "%d.%m.%Y")
    except ValueError:
        raise ValueError("Unable to convert value to datetime.")


def get_days_between(first: datetime, last: datetime) -> int:
    """Gets the difference between two dates."""

    if not isinstance(first, datetime) or not isinstance(last, datetime):
        raise TypeError("Datetimes required.")

    difference = (last - first).days

    return difference


def get_day_of_week_on(date_val: datetime) -> str:
    """Returns the day of the week from a datetime object."""
    weekday = ['Monday', 'Tuesday', 'Wednesday',
               'Thursday', 'Friday', 'Saturday', 'Sunday']
    return weekday[date_val.weekday()]


def get_current_age(birthdate: date) -> int:
    """Returns the age from inputted birthdate"""
    today = date.today()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.year))
