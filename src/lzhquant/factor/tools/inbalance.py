# -*- coding: UTF-8 -*-
# Public package
# Private package
# Internal package

def inbalance_equal(value1, value2):
    return ((value1 - value2) / (value1 + value2)).significance()


def inbalance_square(num1, den1, num2, den2):
    return (num1 / den1 - num2 / den2).significance()
