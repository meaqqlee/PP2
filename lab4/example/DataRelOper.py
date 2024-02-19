from datetime import datetime, timedelta

def subtract_five_days():
    return datetime.now() - timedelta(days=5)

def print_dates():
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    print(f"Yesterday: {yesterday.strftime('%Y-%m-%d')}")
    print(f"Today: {today.strftime('%Y-%m-%d')}")
    print(f"Tomorrow: {tomorrow.strftime('%Y-%m-%d')}")

def drop_microseconds():
    return datetime.now().replace(microsecond=0)

def date_difference_in_seconds(date1, date2):
    return abs((date2 - date1).total_seconds())

if __name__ == "__main__":
    print(f"Five days ago: {subtract_five_days()}")
    print_dates()
    print(f"Current time without microseconds: {drop_microseconds()}")
    print(f"Difference in seconds: {date_difference_in_seconds(datetime(2024, 2, 15), datetime(2024, 2, 18))}")
