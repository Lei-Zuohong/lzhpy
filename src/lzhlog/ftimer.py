# -*- coding: UTF-8 -*-
# Public package
import time
import pandas
import inspect
# Private package
# Internal package

################################################################################
# 批注
buffer = pandas.DataFrame(columns=['Module', 'Function', 'Time']).set_index(['Module', 'Function'])['Time']
################################################################################


def dec(func):
    def wrapper(*args, **argv):
        start = time.time()
        result = func(*args, **argv)
        end = time.time()
        module = inspect.getmodule(func).__name__
        function = func.__qualname__
        if ((module, function) not in buffer):
            buffer[(module, function)] = end - start
        else:
            buffer[(module, function)] += end - start
        return result
    return wrapper


def __buffer_to_df(sort=False):
    output = pandas.DataFrame({'time(s)': buffer,
                               'percent(%)': buffer / buffer.sum() * 100})
    if (sort):
        output = output.sort_values(by='time(s)', ascending=False)
    else:
        output = output.sort_index()
    return output


def report(logger=None, sort=False):
    output = __buffer_to_df(sort=sort)
    if (logger is not None):
        for line in output.__str__().split('\n'):
            logger.info(line)
    else:
        print(output)


def to_csv(filename):
    output = __buffer_to_df()
    output.to_csv(filename)
    return output


def to_pickle(filename):
    output = __buffer_to_df()
    output.to_pickle(filename)
    return output
