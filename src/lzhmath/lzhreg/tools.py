# -*- coding: UTF-8 -*-
# Public package
import numpy
import pandas
from dataclasses import dataclass
# Private package
# Internal package


@dataclass
class FitResult:
    beta: float | numpy.ndarray = None
    beta_e: float | numpy.ndarray = None
    beta_t: float | numpy.ndarray = None
    alpha: float = None
    alpha_e: float = None
    alpha_t: float = None
    r: float = None
    r2: float = None
    eps_yp: numpy.ndarray = None
    eps: numpy.ndarray = None
    sse: float = None
    ssr: float = None
    sst: float = None


def to_ndarray(data: list | numpy.ndarray | pandas.Series | pandas.DataFrame) -> numpy.ndarray:
    '将任何类型一维数据转换为numpy'
    if (isinstance(data, list)):
        return numpy.array(data)
    elif (isinstance(data, numpy.ndarray)):
        return data.copy()
    elif (isinstance(data, pandas.Series)):
        return data.to_numpy()
    elif (isinstance(data, pandas.DataFrame)):
        return data.to_numpy().T
    else:
        raise ValueError(f'Wrong type of data: {type(data)}')


def inverse_matrix(data: numpy.ndarray) -> numpy.ndarray:
    '矩阵求逆，允许处理0值'
    if (data.shape[0] != data.shape[1]):
        msg = f'''
        Wrong input matrix shape:
            - shape[0]: {data.shape[0]}
            - shape[1]: {data.shape[1]}
        '''
        raise ValueError(msg)
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
