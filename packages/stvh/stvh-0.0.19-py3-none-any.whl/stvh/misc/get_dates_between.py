from datetime import date, timedelta


def get_dates_between(start_date: date, end_date: date):
    """Get dates between `start_date` and `end_date` (inclusively).

    Args:
        start_date (date):
        end_date (date):
    """
    current_date = start_date
    timedelta_1days = timedelta(days=1)

    while current_date <= end_date:
        yield current_date

        current_date += timedelta_1days
