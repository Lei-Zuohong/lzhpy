接口：
fit_storersd(datay, datax, threads)

功能：
datay 维度为 parayN * sampleN
datax 维度为 paraxN * sampleN
计算每一个 paray 对所有 parax 的回归结果
返回结果为 parayN * (paraxN + 2) 的矩阵，倒数第二列为截距，倒数第一列为r