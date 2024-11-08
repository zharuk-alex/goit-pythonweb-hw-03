from datetime import datetime


def format_timestamp(value, format="%Y-%m-%d %H:%M:%S"):
    dt_object = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
    return dt_object.strftime(format)
