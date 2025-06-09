import datetime

def exists_datetime_format(df: str) -> bool:
    """
    Checks if the string matches a datetime format.
    """
    try:
        datetime.datetime.strptime(df, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False