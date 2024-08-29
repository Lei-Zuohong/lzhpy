# -*- coding: UTF-8 -*-
# Public package
import copy
import numpy
import pandas
import scipy.stats
import scipy.linalg
import scipy.special
# Private package
# Internal package

################################################################################
# 批注
################################################################################


def gen_rand_norm(num, mean, error):
    '''Generate random numbers with normal distribution.

    Args:
        num (int): number of random numbers.
        mean (float): mean of normal distribution.
        error (float): standard deviation of normal distribution.

    Returns:
        output (numpy.ndarray): random numbers.
    '''
    output = scipy.stats.norm.rvs(mean, error, size=(num))
    return output


def gen_rand_uniform(num, left, right):
    '''Generate random numbers with uniform distribution.

    Args:
        num (int): number of random numbers.
        left (float): left boundary of uniform distribution.
        right (float): right boundary of uniform distribution.

    Returns:
        output (numpy.ndarray): random numbers.
    '''
    output = scipy.stats.uniform.rvs(left, right - left, size=(num))
    return output


def gen_rand_norm_cov(num, means, errors, cov):
    '''Generate random numbers with normal distribution and covariance.

    Args:
        num (int): number of random numbers.
        means (numpy.ndarray): means of normal distribution.
        errors (numpy.ndarray): standard deviations of normal distribution.
        cov (numpy.ndarray): covariance matrix of normal distribution.

    Returns:
        output (numpy.ndarray): random numbers.
    '''
    # 判断数组长度
    if (numpy.unique([means.shape[0], errors.shape[0], cov.shape[0], cov.shape[1]]).shape[0] > 1):
        strerr = 'Error from hmath.hstatis.generate_random_gaussian_cov():\n'
        strerr += 'Error length of input matrix!\n'
        strerr += 'Length of means: ' + str(means.shape[0]) + '\n'
        strerr += 'Length of errors: ' + str(errors.shape[0]) + '\n'
        strerr += 'Length of covs: ' + str(cov.shape[0]) + ', ' + str(cov.shape[1]) + '\n'
        raise ValueError(strerr)
    length = means.shape[0]
    # 产生标准高斯分布
    output = numpy.array([gen_rand_norm(num, 0.0, 1.0) for i in range(length)])
    # 转换标准高斯分布
    eigen_value, eigen_vector = scipy.linalg.eigh(cov)
    correction = numpy.dot(eigen_vector, numpy.diag(numpy.sqrt(eigen_value)))
    output = numpy.dot(correction, output)
    # 平移分布
    for i in range(length):
        output[i] += means[i]
    return output


def gen_rand_norm_cor(num, means, errors, cor):
    '''Generate random numbers with normal distribution and correlation.

    Args:
        num (int): number of random numbers.
        means (numpy.ndarray): means of normal distribution.
        errors (numpy.ndarray): standard deviations of normal distribution.
        cor (numpy.ndarray): correlation matrix of normal distribution.

    Returns:
        output (numpy.ndarray): random numbers.
    '''
    # 判断数组长度
    if (numpy.unique([means.shape[0], errors.shape[0], cor.shape[0], cor.shape[1]]).shape[0] > 1):
        strerr = 'Error from hmath.hstatis.generate_random_gaussian_cor():\n'
        strerr += 'Error length of input matrix!\n'
        strerr += 'Length of means: ' + str(means.shape[0]) + '\n'
        strerr += 'Length of errors: ' + str(errors.shape[0]) + '\n'
        strerr += 'Length of cors: ' + str(cor.shape[0]) + ', ' + str(cor.shape[1]) + '\n'
        raise ValueError(strerr)
    length = means.shape[0]
    # 得到covariance
    cov = cor.copy()
    for i in range(length):
        for j in range(length):
            cov[i][j] *= errors[i] * errors[j]
    # 调用covariance
    output = gen_rand_norm_cov(num, means, errors, cov)
    return output


class Parameter():
    '''Parameter'''

    def __init__(self, *args, name='', value=0, error=1, limitl=None, limitr=None, vary=True):
        '''Parameter

        Args:
            name (str): name of parameter.
            value (float): value of parameter.
            error (float): error of parameter.
            limitl (float): left boundary of parameter.
            limitr (float): right boundary of parameter.
            vary (bool): whether the parameter varies.
        '''
        if (len(args) == 0):
            self.df = pandas.Series({'name': name,
                                     'value': value,
                                     'error': error,
                                     'limitl': limitl,
                                     'limitr': limitr,
                                     'vary': vary})
        elif (isinstance(args[0], pandas.core.series.Series)):
            self.df = args[0]
        else:
            raise ValueError('Error from hmath.hstatis.Parameter():\n')

    def __repr__(self):
        return self.df.__repr__()

    def copy(self):
        return copy.deepcopy(self)

    def gen_rand_norm(self, num):
        '''Generate random numbers with normal distribution.

        Args:
            num (int): number of random numbers.

        Returns:
            output (numpy.ndarray): random numbers.
        '''
        if (self.df['vary']):
            output = gen_rand_norm(num, self.df['value'], self.df['error'])
        else:
            output = numpy.full(num, self.df['value'])
        return output

    def gen_rand_uniform(self, num):
        '''Generate random numbers with uniform distribution.

        Args:
            num (int): number of random numbers.

        Returns:
            output (numpy.ndarray): random numbers.
        '''
        if (self.df['vary']):
            output = gen_rand_uniform(num, self.df['limitl'], self.df['limitr'])
        else:
            output = numpy.full(num, self.df['value'])
        return output


class Parameters():
    '''Parameters'''

    def __init__(self, *args):
        '''Parameters

        Args:
            args (empty): empty.
            args (numpy.ndarray): using numpy.ndarray (Npara * Nsample) to initialize.
            args (pandas.core.frame.DataFrame): using DataFrame (Npara * Nsample) to initialize.
        '''
        if (len(args) == 0):
            self.df = pandas.DataFrame(columns=['name', 'value', 'error', 'limitl', 'limitr', 'vary'])
        elif (isinstance(args[0], numpy.ndarray)):
            self.__init_ndarray(args[0])
        elif (isinstance(args[0], pandas.core.frame.DataFrame)):
            self.__init_dataframe(args[0])

    def __init_ndarray(self, datain):
        self.df = pandas.DataFrame(columns=['name', 'value', 'error', 'limitl', 'limitr', 'vary'])
        for ip in range(datain.shape[0]):
            self.add_para(Parameter(name='p%d' % (ip),
                                    value=datain[ip].mean(),
                                    error=datain[ip].std(),
                                    limitl=datain[ip].min(),
                                    limitr=datain[ip].max(),
                                    vary=True))
        self.set_correlation(numpy.corrcoef(datain))

    def __init_dataframe(self, datain):
        self.df = pandas.DataFrame(columns=['name', 'value', 'error', 'limitl', 'limitr', 'vary'])
        for column in datain.columns:
            self.add_para(Parameter(name=column,
                                    value=datain[column].mean(),
                                    error=datain[column].std(),
                                    limitl=datain[column].min(),
                                    limitr=datain[column].max(),
                                    vary=True))
        self.set_correlation(numpy.corrcoef(datain.to_numpy().T))

    def __repr__(self):
        return self.df.__repr__()

    def __getitem__(self, key):
        return self.df[self.df['name']==key]['value'].iloc[0]

    def copy(self):
        return copy.deepcopy(self)

    def add_para(self, para):
        '''Add parameter

        Args:
            para (Parameter): parameter.
        '''
        self.df.loc[self.df.shape[0]] = para.df

    def add_paras(self, paras):
        '''Add parameters

        Args:
            paras (Parameters): parameters.
        '''
        self.df = pandas.concat([self.df, paras.df], ignore_index=True)

    def vary_num(self):
        'Number of varying parameters.'
        return self.df['vary'].sum()

    def vary_names(self):
        'Names of varying parameters.'
        return self.df[self.df['vary']]['name'].to_list()

    def set_correlation(self, cor):
        '''Set correlation matrix

        Args:
            cor (numpy.ndarray): correlation matrix.
        '''
        if (numpy.unique([self.vary_num(),
                          cor.shape[0],
                          cor.shape[1]]).shape[0] != 1):
            strerr = 'Error from hmath.hstatis.Parameters.set_correlation():\n'
            strerr += 'Dimension of vary parameters: ' + str(self.vary_num()) + '\n'
            strerr += 'Dimension of correlation input: ' + str(cor.shape[0]) + ' * ' + str(cor.shape[1]) + '\n'
            raise ValueError(strerr)
        if (isinstance(cor, pandas.core.frame.DataFrame)):
            self.cor = cor
            self.cor.reindex(index=self.vary_names(), columns=self.vary_names())
        elif (isinstance(cor, numpy.ndarray)):
            self.cor = pandas.DataFrame(cor, columns=self.vary_names(), index=self.vary_names())

    def set_covariance(self, cov):
        '''Set covariance matrix

        Args:
            cov (numpy.ndarray): covariance matrix.
        '''
        if (numpy.unique([self.vary_num(),
                          cov.shape[0],
                          cov.shape[1]]).shape[0] != 1):
            strerr = 'Error from hmath.hstatis.Parameters.set_covariance():\n'
            strerr += 'Dimension of vary parameters: ' + str(self.vary_num()) + '\n'
            strerr += 'Dimension of covariance input: ' + str(cov.shape[0]) + ' * ' + str(cov.shape[1]) + '\n'
            raise ValueError(strerr)
        if (isinstance(cov, pandas.core.frame.DataFrame)):
            self.cor = cov
            self.cor.reindex(index=self.vary_names(), columns=self.vary_names())
        elif (isinstance(cov, numpy.ndarray)):
            self.cor = pandas.DataFrame(cov, columns=self.vary_names(), index=self.vary_names())
        temp_df = self.df.set_index(['name'], drop=True)
        for pi in self.cor.index:
            for pj in self.cor.columns:
                self.cor.loc[pi, pj] = self.cor.loc[pi, pj] / temp_df.loc[pi, 'error'] / temp_df.loc[pj, 'error']

    def gen_rand_norm(self, num):
        '''Generate random numbers with normal distribution.

        Args:
            num (int): number of random numbers.

        Returns:
            output (pandas.core.frame.DataFrame): random numbers (Npara * Nsample).
        '''
        output = pandas.DataFrame({column: Parameter(self.df.loc[self.df['name'] == column].iloc[0]).gen_rand_norm(num) for column in self.df['name']})
        return output

    def gen_rand_uniform(self, num):
        '''Generate random numbers with uniform distribution.

        Args:
            num (int): number of random numbers.

        Returns:
            output (pandas.core.frame.DataFrame): random numbers (Npara * Nsample).
        '''
        output = pandas.DataFrame({column: Parameter(self.df.loc[self.df['name'] == column].iloc[0]).gen_rand_uniform(num) for column in self.df['name']})
        return output

    def gen_rand_norm_cor(self, num):
        '''Generate random numbers with normal distribution and correlation.

        Args:
            num (int): number of random numbers.

        Returns:
            output (pandas.core.frame.DataFrame): random numbers (Npara * Nsample).
        '''
        if (not hasattr(self, 'cor')):
            raise ValueError('The correlation matrix is not set.')
        output = gen_rand_norm_cor(num,
                                   self.df[self.df['vary']]['value'].to_numpy(),
                                   self.df[self.df['vary']]['error'].to_numpy(),
                                   self.cor.to_numpy())
        output = pandas.DataFrame(output.T, columns=self.vary_names())
        return output
