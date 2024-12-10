# -*- coding: UTF-8 -*-
# Public package
import numpy
import lmfit
import pandas
# Private package
# Internal package


def residual(ps, y, x):
    values = ps.valuesdict()
    output = y.copy()
    for i in range(x.shape[0]):
        output -= values['beta%d' % (i)] * x[i]
    return output


def residual_weight(ps, y, x, w):
    values = ps.valuesdict()
    output = y.copy()
    for i in range(x.shape[0]):
        output -= values['beta%d' % (i)] * x[i]
    output *= w
    return output


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


class Linear():
    def __init__(self, y, x, w=None):
        self.y = to_ndarray(y)
        self.x = to_ndarray(x)
        if (w is None):
            self.w = numpy.ones(self.y.shape[0])
        else:
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
        index &= ~numpy.isnan(self.w)
        index &= ~numpy.isinf(self.w)
        index &= self.w != 0
        # 重构数据
        self.y = self.y[index]
        self.x = self.x[index]
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
                raise ValueError('method not support')

    def __fit_simple(self):
        self.mean_x = numpy.sum(self.x * self.w) / numpy.sum(self.w)
        self.mean_y = numpy.sum(self.y * self.w) / numpy.sum(self.w)
        self.epsilon_x = self.x - self.mean_x
        self.epsilon_y = self.y - self.mean_y
        self.beta = (self.epsilon_y * self.epsilon_x * self.w).sum() / (self.epsilon_x**2 * self.w).sum()
        self.alpha = self.mean_y - self.mean_x * self.beta
        self.r = ((self.epsilon_y * self.epsilon_x * self.w).sum()) / numpy.sqrt((self.epsilon_x**2 * self.w).sum()) / numpy.sqrt((self.epsilon_y**2 * self.w).sum())

    def __fit_linear(self):
        self.__fit_simple()
        self.yp = self.x * self.beta + self.alpha
        self.epsilon_yp = self.yp - numpy.sum(self.yp * self.w) / numpy.sum(self.w)
        self.epsilon = self.y - self.yp
        self.sse = numpy.sum((self.epsilon)**2 * self.w)
        self.ssr = numpy.sum((self.epsilon_yp)**2 * self.w)
        self.sst = numpy.sum((self.epsilon_y)**2 * self.w)
        self.beta_e = numpy.sqrt(((self.epsilon**2 * self.w).sum()) / ((self.epsilon_x**2 * self.w).sum()) / (len(self.x) - 2))
        self.alpha_e = self.beta_e * numpy.sqrt(numpy.sum(self.x**2 * self.w) / len(self.x))
        if (self.beta_e == 0):
            self.beta_t = numpy.inf
        else:
            self.beta_t = self.beta / self.beta_e
        self.alpha_t = self.alpha / self.alpha_e
        self.r2 = self.ssr / self.sst
        self.r = numpy.sqrt(self.r2)

    def __fit_polyfit(self):
        para, cova = numpy.polyfit(self.x, self.y, 1, w=self.w, cov=True)
        self.beta = para[0]
        self.alpha = para[1]
        self.beta_e = numpy.sqrt(cova[0][0])
        self.alpha_e = numpy.sqrt(cova[1][1])
        self.beta_t = self.beta / self.beta_e
        self.alpha_t = self.alpha / self.alpha_e


class MultiLinear():
    def __init__(self, y, x, w=None, stable=False):
        self.y = to_ndarray(y)
        self.x = to_ndarray(x)
        if (w is None):
            self.w = numpy.ones(self.y.shape[0])
        else:
            self.w = to_ndarray(w)
        self.method = 'linear'
        self.force_neutral = False
        self.drop_nan = True
        self.drop_inf = True
        self.drop_zero = False
        if (stable):
            self.inv = inverse_matrix
        else:
            self.inv = numpy.linalg.inv

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
        index &= ~numpy.isnan(self.w)
        index &= ~numpy.isinf(self.w)
        index &= self.w != 0
        self.y = self.y[index]
        self.x = self.x[:, index]
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
                raise ValueError('method not support')

    def __fit_linear(self):
        y = self.y.copy()
        if (self.force_neutral):
            x = self.x.copy().T
        else:
            x = numpy.concatenate((self.x, [numpy.ones(self.x.shape[1])]), axis=0).copy().T
        w = numpy.diag(self.w)
        # 计算斜率
        temp_inv = self.inv(numpy.dot(numpy.dot(x.T, w), x))
        beta_ = numpy.dot(temp_inv, numpy.dot(numpy.dot(x.T, w), y))
        if (self.force_neutral):
            self.beta = beta_
            self.alpha = 0.0
        else:
            self.beta = beta_[:-1]
            self.alpha = beta_[-1]
        # 计算统计参数
        self.yp = numpy.dot(self.x.T, self.beta) + self.alpha
        self.epsilon_yp = self.yp - numpy.sum(self.yp * self.w) / numpy.sum(self.w)
        self.epsilon_y = self.y - numpy.sum(self.y * self.w) / numpy.sum(self.w)
        self.epsilon = self.y - self.yp
        self.sse = numpy.sum((self.epsilon)**2 * self.w)
        self.ssr = numpy.sum((self.epsilon_yp)**2 * self.w)
        self.sst = numpy.sum((self.epsilon_y)**2 * self.w)
        self.mse = numpy.sum((self.epsilon)**2 * self.w) / numpy.sum(self.w)
        temp = self.mse * temp_inv * x.shape[0] / (x.shape[0] - x.shape[1])
        temp[numpy.where(temp < 0)] = 0.0
        e_ = numpy.diagonal(numpy.sqrt(temp))
        t_ = beta_ / e_
        if (self.force_neutral):
            self.beta_e = e_
            self.alpha_e = 0.0
            self.beta_t = t_
            self.alpha_t = 0.0
        else:
            self.beta_e = e_[0:-1]
            self.alpha_e = e_[-1]
            self.beta_t = t_[0:-1]
            self.alpha_t = t_[-1]
        self.r2 = self.ssr / self.sst
        self.r = numpy.sqrt(self.r2)

    def __fit_lmfit(self):
        y = self.y.copy()
        x = numpy.concatenate((self.x, [numpy.ones(self.x.shape[1])]), axis=0).copy()
        w = self.w.copy()
        ps = lmfit.Parameters()
        for i in range(x.shape[0]):
            if (hasattr(self, 'hint')):
                ps.add(name='beta%d' % (i), value=self.hint[i][0], min=self.hint[i][1], max=self.hint[i][2])
            else:
                ps.add(name='beta%d' % (i), value=0.0, min=-10000, max=10000)
        result = lmfit.minimize(residual_weight, params=ps, method='leastsq', args=(y, x, w))
        # lmfit.printfuncs.report_fit(result.params, min_correl=0.5)
        beta_ = []
        betae_ = []
        for i in range(x.shape[0]):
            beta_.append(result.params['beta%d' % (i)].value)
            if (None is not result.params['beta%d' % (i)].stderr):
                betae_.append(result.params['beta%d' % (i)].stderr)
            else:
                betae_.append(result.params['beta%d' % (i)].value)
        beta_ = numpy.array(beta_)
        betae_ = numpy.array(betae_)
        t_ = beta_ / betae_
        self.beta = beta_[0:-1]
        self.alpha = beta_[-1]
        self.beta_e = betae_[0:-1]
        self.alpha_e = betae_[-1]
        self.beta_t = t_[0:-1]
        self.alpha_t = t_[-1]
        self.yp = numpy.dot(self.x.T, self.beta) + self.alpha
        self.epsilon_yp = self.yp - numpy.sum(self.yp * self.w) / numpy.sum(self.w)
        self.epsilon_y = self.y - numpy.sum(self.y * self.w) / numpy.sum(self.w)
        self.epsilon = self.y - self.yp
        self.sse = numpy.sum((self.epsilon)**2 * self.w)
        self.ssr = numpy.sum((self.epsilon_yp)**2 * self.w)
        self.sst = numpy.sum((self.epsilon_y)**2 * self.w)
        self.mse = numpy.sum((self.epsilon)**2 * self.w) / numpy.sum(self.w)
        self.r2 = self.ssr / self.sst
        self.r = numpy.sqrt(self.r2)
