# -*- coding: UTF-8 -*-
# Public package
import copy
import numpy
import pandas
# Private package
# Internal package
from .tools import *


class Parameter():
    '模型参数'

    def __init__(self,
                 *args: list[pandas.Series],
                 name: str = '',
                 value: float = 0,
                 error: float = 1,
                 left: float = None,
                 right: float = None,
                 vary: bool = True):
        '''
        模型参数
            - args: 可以选择直接输入一个pandas.Series
            - name: 名字
            - value: 数值
            - error: 误差
            - left: 左边界
            - right: 右边界
            - vary: 是否为变量
        '''
        if (len(args) == 0):
            self.df = pandas.Series({'name': name,
                                     'value': value,
                                     'error': error,
                                     'left': left,
                                     'right': right,
                                     'vary': vary})
        elif (isinstance(args[0], pandas.core.series.Series)):
            self.df = args[0]

    def __str__(self):
        return self.df.__str__()

    def __repr__(self):
        return self.df.__repr__()

    def copy(self):
        return copy.deepcopy(self)

    def gen_rand_norm(self, num: int) -> numpy.ndarray:
        '返回该变量的正态分布样本'
        if (self.df['vary']):
            output = gen_rand_norm(num, self.df['value'], self.df['error'])
        else:
            output = numpy.full(num, self.df['value'])
        return output

    def gen_rand_uniform(self, num: int) -> numpy.ndarray:
        '返回该变量的均匀分布样本'
        if (self.df['vary']):
            output = gen_rand_uniform(num, self.df['left'], self.df['right'])
        else:
            output = numpy.full(num, self.df['value'])
        return output


class Parameters():
    '模型参数集合'

    def __init__(self,
                 *args):
        '''
        模型参数集合：
            - args -> None: 初始化空集合
            - args -> numpy.ndarray: 通过参数样本初始化，输入格式为numpy(paras, samples)
            - args -> pandas.DataFrame: 通过参数样本初始化，输入格式为dataframe(samples * paras)
        '''
        if (len(args) == 0):
            self.df = pandas.DataFrame(columns=['name', 'value', 'error', 'left', 'right', 'vary'])
        elif (isinstance(args[0], numpy.ndarray)):
            self.__init_ndarray(args[0])
        elif (isinstance(args[0], pandas.core.frame.DataFrame)):
            self.__init_dataframe(args[0])
        else:
            raise TypeError(f'Wrong type of args: {type(args[0])}')

    def __init_ndarray(self, datain: numpy.ndarray):
        self.df = pandas.DataFrame(columns=['name', 'value', 'error', 'left', 'right', 'vary'])
        for ip in range(datain.shape[0]):
            self.add_para(Parameter(name='p%d' % (ip),
                                    value=datain[ip].mean(),
                                    error=datain[ip].std(),
                                    left=datain[ip].min(),
                                    right=datain[ip].max(),
                                    vary=True))
        self.set_correlation(numpy.corrcoef(datain))

    def __init_dataframe(self, datain: pandas.DataFrame):
        self.df = pandas.DataFrame(columns=['name', 'value', 'error', 'left', 'right', 'vary'])
        for column in datain.columns:
            self.add_para(Parameter(name=column,
                                    value=datain[column].mean(),
                                    error=datain[column].std(),
                                    left=datain[column].min(),
                                    right=datain[column].max(),
                                    vary=True))
        self.set_correlation(numpy.corrcoef(datain.to_numpy().T))

    def __str__(self):
        return self.df.__str__()

    def __repr__(self):
        return self.df.__repr__()

    def copy(self):
        return copy.deepcopy(self)

    def __getitem__(self, key: str):
        return self.df.loc[self.df['name'] == key, :].squeeze()

    def add_para(self, para: Parameter):
        '增加参数'
        self.df.loc[self.df.shape[0]] = para.df

    def add_paras(self, paras: 'Parameters'):
        '增加参数集合'
        self.df = pandas.concat([self.df, paras.df], ignore_index=True).reset_index(drop=True)

    def vary_num(self):
        '变量数目'
        return self.df['vary'].sum()

    def vary_names(self):
        '变量名字'
        return self.df[self.df['vary']]['name'].to_list()

    def set_correlation(self, cor):
        '''
        设定相关系数矩阵
        '''
        if (numpy.unique([self.vary_num(),
                          cor.shape[0],
                          cor.shape[1]]).shape[0] != 1):
            msg = f'''
            Error correlation dimension:
                - vary parameters: {self.vary_num()}
                - correlation: {cor.shape[0]} * {cor.shape[1]}
            '''
            raise ValueError(msg)
        if (isinstance(cor, pandas.core.frame.DataFrame)):
            self.cor = cor.copy()
            self.cor.reindex(index=self.vary_names(), columns=self.vary_names())
        elif (isinstance(cor, numpy.ndarray)):
            self.cor = pandas.DataFrame(cor, columns=self.vary_names(), index=self.vary_names())
        else:
            raise TypeError(f'Wrong type of correlation {type(cor)}')

    def set_covariance(self, cov):
        '''
        设定协方差矩阵
        '''
        if (numpy.unique([self.vary_num(),
                          cov.shape[0],
                          cov.shape[1]]).shape[0] != 1):
            msg = f'''
            Error covariance dimension:
                - vary parameters: {self.vary_num()}
                - correlation: {cov.shape[0]} * {cov.shape[1]}
            '''
            raise ValueError(msg)
        if (isinstance(cov, pandas.core.frame.DataFrame)):
            self.cor = cov
            self.cor.reindex(index=self.vary_names(), columns=self.vary_names())
        elif (isinstance(cov, numpy.ndarray)):
            self.cor = pandas.DataFrame(cov, columns=self.vary_names(), index=self.vary_names())
        else:
            raise TypeError(f'Wrong type of covariance {type(cov)}')
        # 转换数值
        temp_df = self.df.set_index(['name'], drop=True)
        for pi in self.cor.index:
            for pj in self.cor.columns:
                self.cor.loc[pi, pj] = self.cor.loc[pi, pj] / temp_df.loc[pi, 'error'] / temp_df.loc[pj, 'error']

    def gen_rand_norm(self, num: int) -> pandas.DataFrame:
        '''
        返回所有参数的正态分布样本
        '''
        output = pandas.DataFrame({column: Parameter(self.df.loc[self.df['name'] == column].iloc[0]).gen_rand_norm(num) for column in self.df['name']})
        return output

    def gen_rand_uniform(self, num: int) -> pandas.DataFrame:
        '''
        返回所有参数的均匀分布样本
        '''
        output = pandas.DataFrame({column: Parameter(self.df.loc[self.df['name'] == column].iloc[0]).gen_rand_uniform(num) for column in self.df['name']})
        return output

    def gen_rand_norm_cor(self, num: int) -> pandas.DataFrame:
        '''
        返回所有参数的正态分布样本，考虑相关性
        '''
        if (not hasattr(self, 'cor')):
            raise ValueError('The correlation matrix is not set.')
        output = gen_rand_norm_cor(num,
                                   self.df[self.df['vary']]['value'].to_numpy(),
                                   self.df[self.df['vary']]['error'].to_numpy(),
                                   self.cor.to_numpy())
        output = pandas.DataFrame(output.T, columns=self.vary_names())
        return output
