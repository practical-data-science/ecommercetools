import pandas as pd
from pandas.tseries.offsets import BDay
from pandas.tseries.holiday import (
    AbstractHolidayCalendar, Holiday, DateOffset, SU, MO, TU, WE, TH, FR, SA, next_monday,
    nearest_workday, sunday_to_monday, EasterMonday, GoodFriday, Easter
)


class UKEcommerceTradingCalendar(AbstractHolidayCalendar):
    rules = [

        # Pay days (based on fourth Friday of the month)
        Holiday('January Pay Day', month=1, day=31, offset=BDay(-1)),
        Holiday('February Pay Day', month=2, day=28, offset=BDay(-1)),
        Holiday('March Pay Day', month=3, day=31, offset=BDay(-1)),
        Holiday('April Pay Day', month=4, day=30, offset=BDay(-1)),
        Holiday('May Pay Day', month=5, day=31, offset=BDay(-1)),
        Holiday('June Pay Day', month=6, day=30, offset=BDay(-1)),
        Holiday('July Pay Day', month=7, day=31, offset=BDay(-1)),
        Holiday('August Pay Day', month=8, day=31, offset=BDay(-1)),
        Holiday('September Pay Day', month=9, day=30, offset=BDay(-1)),
        Holiday('October Pay Day', month=10, day=31, offset=BDay(-1)),
        Holiday('November Pay Day', month=11, day=30, offset=BDay(-1)),
        Holiday('December Pay Day', month=12, day=31, offset=BDay(-1)),

        # Seasonal trading events
        Holiday('January sale', month=1, day=1),
        Holiday('Valentine\'s Day [last order date]', month=2, day=14, offset=BDay(-2)),
        Holiday('Valentine\'s Day', month=2, day=14),
        Holiday('Mother\'s Day [last order date]', month=5, day=1, offset=BDay(-2)),
        Holiday('Mother\'s Day', month=5, day=1, offset=pd.DateOffset(weekday=SU(2))),
        Holiday('Father\'s Day [last order date]', month=6, day=1, offset=BDay(-2)),
        Holiday('Father\'s Day', month=6, day=1, offset=pd.DateOffset(weekday=SU(3))),
        Holiday("Black Friday [sale starts]", month=11, day=1, offset=[pd.DateOffset(weekday=SA(4)), BDay(-5)]),
        Holiday('Black Friday', month=11, day=1, offset=pd.DateOffset(weekday=FR(4))),
        Holiday("Cyber Monday", month=11, day=1, offset=[pd.DateOffset(weekday=SA(4)), pd.DateOffset(2)]),
        Holiday('Christmas Day [last order date]', month=12, day=25, offset=BDay(-2)),
        Holiday('Boxing Day sale', month=12, day=26),
    ]


def _get_dates(start_date, days=365):
    """Get all dates from a start date to a given end date X days ahead.

    Args:
        start_date (YYYY-MM-DD): Start date, i.e. 2021-01-01
        days (optional, int): 365

    Returns:
        Dataframe of dates X days ahead of start date
    """

    period = pd.date_range(start_date, periods=days, freq='D')
    df = pd.DataFrame({'date': period})
    return df


def get_trading_events(start_date, days=365):
    """Calculate and return all trading events from the UK ecommerce trading calendar.

    Args:
        start_date (YYYY-MM-DD): Start date, i.e. 2021-01-01
        days (optional, int): 365

    Returns:
        Dataframe of the name and date of each ecommerce trading event.
    """

    dates = _get_dates(start_date, days)

    calendar = UKEcommerceTradingCalendar()
    start = dates.date.min()
    end = dates.date.max()

    events = calendar.holidays(start=start, end=end, return_name=True)
    events = events.reset_index(name='event').rename(columns={'index': 'date'})

    return events


def get_trading_calendar(start_date, days=365):
    """Return a full ecommerce trading calendar for the specified period.

    Args:
        start_date (YYYY-MM-DD): Start date, i.e. 2021-01-01
        days (optional, int): 365

    Returns:
        Pandas dataframe containing full calendar of ecommerce trading events.
    """

    dates = _get_dates(start_date, days)
    events = get_trading_events(start_date, days)

    calendar = dates.merge(events, on='date', how='left').fillna('')
    return calendar
