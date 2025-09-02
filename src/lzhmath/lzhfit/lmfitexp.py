# -*- coding: UTF-8 -*-
# Public package
import lmfit
import numpy
import pandas
# Private package
# Internal package
from . import lzhpara


def Parameter_to_lmfit(para: lzhpara.Parameter) -> lmfit.Parameter:
    p = lmfit.Parameter(para.df['name'])
    p.set(value=para.df['value'],
          vary=para.df['vary'],
          min=para.df['limitl'],
          max=para.df['limitr'])
    return p


def Parameters_to_lmfit(paras: lzhpara.Parameters) -> lmfit.Parameters:
    ps = lmfit.Parameters()
    for ip in range(paras.df.shape[0]):
        ps.add(Parameter_to_lmfit(lzhpara.Parameter(paras.df.iloc[ip])))
    return ps


def lmfit_to_Parameter(p: lmfit.Parameter) -> lzhpara.Parameter:
    output = lzhpara.Parameter(name=p.name,
                               value=p.value,
                               error=p.stderr,
                               limitl=p.min,
                               limitr=p.max,
                               vary=p.vary)
    return output


def lmfit_to_Parameters(ps: lmfit.Parameters) -> lzhpara.Parameters:
    output = lzhpara.Parameters()
    for name in ps:
        output.add_para(lmfit_to_Parameter(ps[name]))
    has_cor = False
    temp_names = output.vary_names()
    temp_cor = pandas.DataFrame(numpy.zeros((len(temp_names), len(temp_names))),
                                columns=temp_names,
                                index=temp_names)
    for temp_name1 in temp_names:
        if (hasattr(ps[temp_name1], 'correl')):
            for temp_name2 in temp_names:
                if (temp_name1 == temp_name2):
                    temp_cor.loc[temp_name1, temp_name2] = 1.0
                elif (temp_name2 in ps[temp_name1].correl):
                    temp_cor.loc[temp_name1, temp_name2] = ps[temp_name1].correl[temp_name2]
                    has_cor = True
    if (has_cor):
        output.set_correlation(temp_cor)
    return output
