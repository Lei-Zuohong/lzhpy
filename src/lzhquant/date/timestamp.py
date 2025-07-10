# -*- coding: UTF-8 -*-
# Public package
import pytz
import pandas
import datetime
# Private package
# Internal package


def etimestamp_to_datetime(timestamp: int, multiple=int(1e9)) -> datetime.datetime:
    '转换时间戳为datetime, 常用于L1行情'
    # 1. 转换为 UTC datetime（带时区）
    seconds = timestamp // multiple
    nanoseconds = timestamp % multiple
    dt_utc = datetime.datetime.fromtimestamp(seconds, pytz.UTC)
    dt_utc = dt_utc.replace(microsecond=nanoseconds // 1000)
    # 2. 转换为北京时间（UTC+8），再移除时区信息
    dt_beijing = dt_utc.astimezone(pytz.timezone("Asia/Shanghai"))
    dt_beijing_naive = dt_beijing.replace(tzinfo=None)  # 移除时区信息
    return dt_beijing_naive


def datetime_to_etimestamp(dtm: datetime.datetime, multiple=(1e9)) -> int:
    '转换datetime为时间戳, 常用于L1行情'
    # 1. 将 naive 时间标记为北京时间（Asia/Shanghai）
    tz_shanghai = pytz.timezone("Asia/Shanghai")
    dt_beijing = tz_shanghai.localize(dtm)
    # 2. 转换为 UTC 时间
    dt_utc = dt_beijing.astimezone(pytz.UTC)
    # 3. 计算 Unix 时间戳（秒 + 纳秒）
    timestamp_seconds = dt_utc.timestamp()  # 浮点数（含小数秒）
    timestamp_nanoseconds = int(timestamp_seconds * multiple)  # 转换为纳秒
    return timestamp_nanoseconds


def timeclock_to_datetime(intday: int, inttime: int) -> datetime.datetime:
    '转换时钟数字为datetime，用于L2行情'
    return datetime.datetime(intday // 10000,
                             intday % 10000 // 100,
                             intday % 100,
                             inttime // 10000000000000,
                             inttime % 10000000000000 // 100000000000,
                             inttime % 100000000000 // 1000000000)


def dftimeclock_to_datetime(df: pandas.DataFrame, nday: str, ntime: str) -> pandas.Series:
    '转换dataframe时钟数字为datetime，用于L2行情'
    return df[[nday, ntime]].apply(lambda x: timeclock_to_datetime(x.loc[nday], x.loc[ntime]), axis=1)
