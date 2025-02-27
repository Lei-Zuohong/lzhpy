接口：
fit_selfrsd(data, threads)

功能：
data 维度为 paraN * sampleN
计算每一个 para 对其它所有 para 的回归结果
返回结果为 paraN * (paraN + 1) 的矩阵，自己本身位置为截距，最后一列为r