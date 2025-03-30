from datetime import datetime, timedelta


def get_timestamp_5_mins_before(timestamp: datetime):
    return (timestamp - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
