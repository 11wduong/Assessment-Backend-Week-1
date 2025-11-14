"""Functions for working with dates."""

from datetime import datetime, date


def convert_to_datetime(date_val: str) -> datetime:
    """Converts string date values to datetime objects."""
    return datetime.strptime(date_val, "%d.%m.%Y")


def get_days_between(first: datetime, last: datetime) -> int:
    """Gets the difference between two dates."""
    return (last - first)


def get_day_of_week_on(date_val: datetime) -> str:
    pass


def get_current_age(birthdate: date) -> int:
    pass
