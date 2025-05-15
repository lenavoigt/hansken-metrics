from datetime import datetime, timedelta


def get_year_month_day_str(datetime_obj: datetime) -> str:
    """
    Convert a datetime object to a string of the format YYYY-MM-DD
    :param datetime_obj: datetime object
    :return: string in the format 'YYYY-MM-DD'
    """
    return datetime_obj.strftime('%Y-%m-%d')


def get_time_delta_days(delta: timedelta) -> float:
    """
    Convert a timedelta object to a float representing the total number of days.
    :param delta: timedelta object
    :return: float number of days
    """
    return delta.total_seconds() / 86400
