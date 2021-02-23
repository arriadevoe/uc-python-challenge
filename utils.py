import datetime


def parse_date_time(dt):
    return datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S%z")