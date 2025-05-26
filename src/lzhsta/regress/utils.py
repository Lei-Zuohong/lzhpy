# -*- coding: UTF-8 -*-
# Public package
import numpy
import pandas
# Private package
# Internal package


def to_ndarray(data):
    if (isinstance(data, list)):
        return numpy.array(data)
    elif (isinstance(data, numpy.ndarray)):
        return data.copy()
    elif (isinstance(data, pandas.Series)):
        return data.to_numpy()
    elif (isinstance(data, pandas.DataFrame)):
        return data.to_numpy().T
    else:
        raise ValueError('data type not support')


def inverse_matrix(data):
    size = data.shape[0]
    array1 = data.copy()
    array2 = numpy.diag(numpy.ones(size))
    for i in range(size):
        if (array1[i][i] == 0):
            for j in range(i + 1, size):
                if (array1[j][i] != 0):
                    array1[[i, j]] = array1[[j, i]]
                    array2[[i, j]] = array2[[j, i]]
                    break
        if (array1[i][i] == 0):
            array1[i][i] = 1e-8
        array2[i] /= array1[i][i]
        array1[i] /= array1[i][i]
        for j in range(size):
            if (j != i):
                array2[j] -= array2[i] * array1[j][i]
                array1[j] -= array1[i] * array1[j][i]
    return array2
