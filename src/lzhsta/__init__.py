# -*- coding: UTF-8 -*-
# Public package
import scipy
# Private package
# Internal package

################################################################################
# 批注
################################################################################


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
