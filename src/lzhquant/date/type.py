# -*- coding: UTF-8 -*-
# Public package
import datetime
# Private package
# Internal package


################################################################################
# 日期格式转换函数
# i: int
# s: string
# d: datetime.date
################################################################################


def dateitos(date: int) -> str:
    return '%08d' % (date)


def datestoi(date: str) -> int:
    return int(date)


def datestod(date: str) -> datetime.date:
    return datetime.datetime.strptime(date, '%Y%m%d').date()


def datedtos(date: datetime.date) -> str:
    return date.strftime('%Y%m%d')


def dateitod(date: int) -> datetime.date:
    return datestod(dateitos(date))


def datedtoi(date: datetime.date) -> int:
    return datestoi(datedtos(date))


def datetod(date) -> datetime.date:
    if (isinstance(date, datetime.datetime)):
        return date.date()
    elif (isinstance(date, datetime.date)):
        return date
    elif (isinstance(date, str)):
        return datestod(date)
    elif (isinstance(date, int)):
        return dateitod(date)


def datetos(date) -> str:
    if (isinstance(date, datetime.datetime)):
        return datedtos(date.date())
    elif (isinstance(date, datetime.date)):
        return datedtos(date)
    elif (isinstance(date, str)):
        return date
    elif (isinstance(date, int)):
        return dateitos(date)


def datetoi(date) -> int:
    if (isinstance(date, datetime.datetime)):
        return datedtoi(date.date())
    elif (isinstance(date, datetime.date)):
        return datedtoi(date)
    elif (isinstance(date, str)):
        return datestoi(date)
    elif (isinstance(date, int)):
        return date
