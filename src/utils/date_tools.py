import pandas as pd
from datetime import datetime, timedelta

def get_ttm_date_range(current_date: datetime) -> tuple[datetime, datetime]:
    """
    Returns the start and end dates for a Trailing Twelve Months (TTM) window.
    """
    end_date = current_date
    start_date = end_date - timedelta(days=365)
    return start_date, end_date

def ensure_datetime(date_val) -> datetime:
    """
    Safe converter to python datetime.
    """
    return pd.to_datetime(date_val).to_pydatetime()

