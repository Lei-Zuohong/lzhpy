# -*- coding: UTF-8 -*-
# Public package
import numpy
import scipy.stats
import scipy.linalg
# Private package
# Internal package


def gen_rand_norm(num: int,
                  mean: float,
                  std: float) -> numpy.ndarray:
    '''
    返回正态分布样本
        - num: 样本量
        - mean: 平均值
        - std: 标准差
    '''
    return scipy.stats.norm.rvs(mean, std, size=(num))


def gen_rand_uniform(num: int,
                     left: float,
                     right: float) -> numpy.ndarray:
    '''
    返回均匀分布样本
        - num: 样本量
        - left: 左边界
        - right: 右边界
    '''
    return scipy.stats.uniform.rvs(left, right - left, size=(num))


def gen_rand_norm_cov(num: int,
                      means: numpy.ndarray,
                      cov: numpy.ndarray) -> numpy.ndarray:
    '''
    返回根据协方差矩阵生成的多参数样本
        - num: 样本量
        - means: 样本量
        - cov: 协方差矩阵
    '''
    # 检查长度
    length = numpy.unique([means.shape[0], cov.shape[0], cov.shape[1]])
    if (length.shape[0] > 1):
        msg = f'''
        Error length of input matrix:
            - means: {means.shape[0]}
            - cov: {cov.shape[0]} * {cov.shape[1]}
        '''
        raise ValueError(msg)
    length = length[0]
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


def gen_rand_norm_cor(num: int,
                      means: numpy.ndarray,
                      stds: numpy.ndarray,
                      cor: numpy.ndarray) -> numpy.ndarray:
    '''
    返回根据相关系数矩阵生成的多参数样本
        - num: 样本量
        - means: 样本量
        - stds: 标准差
        - cor: 相关系数矩阵
    '''
    # 检查长度
    length = numpy.unique([means.shape[0], stds.shape[0], cor.shape[0], cor.shape[1]])
    if (length.shape[0] > 1):
        msg = f'''
        Error length of input matrix:
            - means: {means.shape[0]}
            - stds: {stds.shape[0]}
            - cor: {cor.shape[0]} * {cor.shape[1]}
        '''
        raise ValueError(msg)
    length = length[0]
    # 获取协方差矩阵
    cov = cor.copy()
    for i in range(length):
        for j in range(length):
            cov[i][j] *= stds[i] * stds[j]
    # 调用cov接口
    return gen_rand_norm_cov(num, means, cov)
