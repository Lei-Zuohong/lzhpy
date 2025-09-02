# -*- coding: UTF-8 -*-
# Public package
import numpy
import scipy
# Private package
# Internal package


def significance(value=[],
                 num_parameter=1,
                 method='chisq'):
    # method
    if (method == 'chisq'):
        factor = 1
    elif (method == 'likelihood'):
        factor = 2.
    else:
        raise ValueError('Error: Wrong significance method!')
    # value
    try:
        length = len(value)
        if (length == 2):
            delta = abs(value[1] - value[0])
        else:
            print('Error: Wrong significance value input!')
    except BaseException:
        delta = value
    # calculate
    output = 1 - scipy.special.gammainc(num_parameter / 2, factor * delta / 2)
    output = abs(scipy.stats.norm.ppf(0.5 * output))
    return output


class edouble:
    def __init__(self, *args):
        if (len(args) == 1):
            self.value = args[0]
            if (self.value < 0):
                self.error = 0
            elif (self.value < 1):
                self.error = 1
            else:
                self.error = numpy.sqrt(self.value)
        elif (len(args) == 2):
            self.value = args[0]
            self.error = args[1]

    def __add__(self, other):
        if isinstance(other, edouble):
            return edouble(self.value + other.value, numpy.sqrt(self.error**2 + other.error**2))
        else:
            return edouble(self.value + other, self.error)

    def __sub__(self, other):
        if isinstance(other, edouble):
            return edouble(self.value - other.value, numpy.sqrt(self.error**2 + other.error**2))
        else:
            return edouble(self.value - other, self.error)

    def __mul__(self, other):
        if isinstance(other, edouble):
            return edouble(self.value * other.value, numpy.sqrt((self.error * other.value)**2 + (other.error * self.value)**2))
        else:
            return edouble(self.value * other, self.error * other)

    def __truediv__(self, other):
        if isinstance(other, edouble):
            return edouble(self.value / other.value, numpy.sqrt((self.error / other.value)**2 + (self.value / other.value**2 * other.error)**2))
        else:
            return edouble(self.value / other, self.error / other)

    def __str__(self):
        return str(self.value) + ' +/- ' + str(self.error)

    def significance(self):
        return self.value / self.error
