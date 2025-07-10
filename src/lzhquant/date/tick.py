# -*- coding: UTF-8 -*-
# Public package
# Private package
# Internal package
from .type import *


def get_stock_tick_times(date):
    dt = datetod(date)
    times = [datetime.datetime.combine(dt, datetime.time(9, 30))]
    while (times[-1] < datetime.datetime.combine(dt, datetime.time(11, 30))):
        times.append(times[-1] + datetime.timedelta(seconds=3))
    times.append(datetime.datetime.combine(dt, datetime.time(13)))
    while (times[-1] < datetime.datetime.combine(dt, datetime.time(15))):
        times.append(times[-1] + datetime.timedelta(seconds=3))
    return times
