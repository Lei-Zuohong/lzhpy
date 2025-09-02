# -*- coding: UTF-8 -*-
# Public package
import numpy
# Private package
# Internal package
from .tools import *
from . import od_simple
from . import od_linear
from . import od_polyfit
from . import td_linear
from . import td_lmfit


class Linear():
    def __init__(self,
                 y: list | numpy.ndarray | pandas.Series,
                 x: list | numpy.ndarray | pandas.Series,
                 w: list | numpy.ndarray | pandas.Series = None):
        self.y = to_ndarray(y)
        self.x = to_ndarray(x)
        if (w is not None):
            self.w = to_ndarray(w)
        self.method = 'linear'
        self.drop_nan = True  # 是否删除nan
        self.drop_inf = True  # 是否删除inf
        self.drop_zero = False  # 是否删除0

    def clean(self):
        # 筛选有效数据
        index = numpy.ones(self.y.shape[0], dtype=bool)
        if (self.drop_nan):
            for array in [self.y, self.x]:
                index &= ~numpy.isnan(array)
        if (self.drop_inf):
            for array in [self.y, self.x]:
                index &= ~numpy.isinf(array)
        if (self.drop_zero):
            for array in [self.y, self.x]:
                index &= array != 0
        if (hasattr(self, 'w')):
            index &= ~numpy.isnan(self.w)
            index &= ~numpy.isinf(self.w)
            index &= self.w != 0
        # 重构数据
        self.y = self.y[index]
        self.x = self.x[index]
        if (hasattr(self, 'w')):
            self.w = self.w[index]
        # 返回结果
        if (self.y.shape[0] > 2):
            return True
        else:
            return False

    def fit(self):
        match(self.method):
            case('simple'):
                self.__fit_simple()
            case('linear'):
                self.__fit_linear()
            case('polyfit'):
                self.__fit_polyfit()
            case _:
                raise ValueError(f'Wrong method: {self.method}')

    def __fit_simple(self):
        if (hasattr(self, 'w')):
            self.result = od_simple.fitw(self.x, self.y, self.w)
        else:
            self.result = od_simple.fit(self.x, self.y)

    def __fit_linear(self):
        if (hasattr(self, 'w')):
            self.result = od_linear.fitw(self.x, self.y, self.w)
        else:
            self.result = od_linear.fit(self.x, self.y)

    def __fit_polyfit(self):
        if (hasattr(self, 'w')):
            self.result = od_polyfit.fitw(self.x, self.y, self.w)
        else:
            self.result = od_polyfit.fit(self.x, self.y)


class MultiLinear():
    def __init__(self,
                 y: list | numpy.ndarray | pandas.Series,
                 x: list | numpy.ndarray | pandas.DataFrame,
                 w: list | numpy.ndarray | pandas.Series = None,
                 stable: bool = False):
        self.y = to_ndarray(y)
        self.x = to_ndarray(x)
        if (w is not None):
            self.w = to_ndarray(w)
        self.method = 'linear'
        self.force_neutral = False
        self.drop_nan = True
        self.drop_inf = True
        self.drop_zero = False
        self.stable = stable

    def clean(self):
        index = numpy.ones(self.y.shape[0], dtype=bool)
        if (self.drop_nan):
            for array in numpy.concatenate(([self.y], self.x), axis=0):
                index &= ~numpy.isnan(array)
        if (self.drop_inf):
            for array in numpy.concatenate(([self.y], self.x), axis=0):
                index &= ~numpy.isinf(array)
        if (self.drop_zero):
            for array in numpy.concatenate(([self.y], self.x), axis=0):
                index &= array != 0
        if (hasattr(self, 'w')):
            index &= ~numpy.isnan(self.w)
            index &= ~numpy.isinf(self.w)
            index &= self.w != 0
        self.y = self.y[index]
        self.x = self.x[:, index]
        if (hasattr(self, 'w')):
            self.w = self.w[index]
        if (self.y.shape[0] > self.x.shape[0]):
            return True
        else:
            return False

    def fit(self):
        match(self.method):
            case('linear'):
                self.__fit_linear()
            case('lmfit'):
                self.__fit_lmfit()
            case _:
                raise ValueError(f'Wrong method: {self.method}')

    def __fit_linear(self):
        # 是否添加截距
        if (self.force_neutral):
            ix = self.x
        else:
            ix = numpy.concatenate((self.x, [numpy.ones(self.x.shape[1])]), axis=0)
        # 拟合
        if (hasattr(self, 'w')):
            self.result = td_linear.fitw(ix, self.y, self.w, stable=self.stable)
        else:
            self.result = td_linear.fit(ix, self.y, stable=self.stable)
        # 处理截距
        if (self.force_neutral):
            self.result.alpha = 0.0
            self.result.alpha_e = 0.0
            self.result.alpha_t = 0.0
        else:
            self.result.alpha = self.result.beta[-1]
            self.result.alpha_e = self.result.beta_e[-1]
            self.result.alpha_t = self.result.beta_t[-1]
            self.result.beta = self.result. beta[:-1]
            self.result.beta_e = self.result.beta_e[:-1]
            self.result.beta_t = self.result.beta_t[:-1]

    def __fit_lmfit(self):
        # 是否添加截距
        if (self.force_neutral):
            ix = self.x
        else:
            ix = numpy.concatenate((self.x, [numpy.ones(self.x.shape[1])]), axis=0)
        # 拟合
        if (hasattr(self, 'w')):
            self.result = td_lmfit.fitw(ix, self.y, self.w)
        else:
            self.result = td_lmfit.fit(ix, self.y)
        # 处理截距
        if (self.force_neutral):
            self.result.alpha = 0.0
            self.result.alpha_e = 0.0
            self.result.alpha_t = 0.0
        else:
            self.result.alpha = self.result.beta[-1]
            self.result.alpha_e = self.result.beta_e[-1]
            self.result.alpha_t = self.result.beta_t[-1]
            self.result.beta = self.result. beta[:-1]
            self.result.beta_e = self.result.beta_e[:-1]
            self.result.beta_t = self.result.beta_t[:-1]
