接口：
fit_cross(codes, x, y, oid, jobN)

功能：
codes 为整数列表，股票代码
x 为 codeN * sampleN 的自变量矩阵
y 为 codeN * sampleN 的因变量矩阵
oid 为 计算的参数列表
    oid: 0   =>   out: r
    oid: 1   =>   out: alpha
    oid: 2   =>   out: beta
    oid: 11  =>   out: alpha_e
    oid: 12  =>   out: alpha_t
    oid: 21  =>   out: beta_e
    oid: 22  =>   out: beta_t
计算每一个 y 对每一个 x 进行一元线性回归的对应参数
返回所有配对结果的字典{codex, codey, output}
------------------------------------------------------------
接口：
fit_across(codexs, codeys, x, y, oid, jobN)

功能：
codexs 为整数列表，自变量股票代码
codeys 为整数列表，自变量股票代码
x 为 codeN * sampleN 的自变量矩阵
y 为 codeN * sampleN 的因变量矩阵
oid 为 计算的参数列表
计算每一个 y 对每一个 x 进行一元线性回归的对应参数
返回所有配对结果的字典{codex, codey, output}
------------------------------------------------------------
接口：
fit_path(codes, x, y, oid, jobN)

功能：
codes 为整数列表，股票代码
x 为 codeN * paraN * sampleN 的自变量矩阵
y 为 codeN * sampleN 的因变量矩阵
oid 为 计算的参数列表
    oid: 2   =>   out: beta
    oid: 21  =>   out: beta_e
    oid: 22  =>   out: beta_t
计算每一个股票，通过所有para x 到 y 进行多远线性回归的对应参数
返回所有结果的字典{code, [output]}