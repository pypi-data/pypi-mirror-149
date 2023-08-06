import datetime

import pandas as pd

from meixmetric.exc.mx_exc import BizException

ALL_DATE_PERIOD = ['month', 'quarter', 'year', 'week', 'm1', 'm3', 'm6', 'y1', 'y2', 'y3', 'y5', 'total']


def calc_date(date: datetime.datetime, period: str, bdate: datetime.datetime) -> datetime.datetime:
    if period == 'month':
        # 本月
        return datetime.datetime(date.year, date.month, 1) - pd.DateOffset(days=1)
    if period == 'quarter':
        # 本季
        return datetime.datetime(date.year, date.month - (date.month - 1) % 3, 1) - pd.DateOffset(days=1)
    if period == 'year':
        # 本年
        return datetime.datetime(date.year, 1, 1) - pd.DateOffset(days=1)
    if period == 'week':
        return date - pd.DateOffset(days=7)
    if period == 'm1':
        return date - pd.DateOffset(months=1)
    if period == 'm3':
        return date - pd.DateOffset(months=3)
    if period == 'm6':
        return date - pd.DateOffset(months=6)
    if period == 'y1':
        return date - pd.DateOffset(years=1)
    if period == 'y2':
        return date - pd.DateOffset(years=2)
    if period == 'y3':
        return date - pd.DateOffset(years=3)
    if period == 'y5':
        return date - pd.DateOffset(years=5)
    if period == 'total':
        return bdate
    else:
        raise BizException("period错误")
