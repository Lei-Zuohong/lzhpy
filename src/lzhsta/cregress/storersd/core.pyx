# cython: boundcheck=False, wraparound=False, initializedcheck=False, cdivision=True, nonecheck=False
from libcpp.vector cimport vector
from cython.parallel cimport prange

cdef extern from "core.hpp":
    vector[double] reg_storersd(vector[double] datay, vector[vector[double]] datax) nogil

def fit_storersd(datay, datax, threads):
    cdef:
        int paraxN = len(datax)
        int parayN = len(datay)
        vector[vector[double]] output
    
    output.resize(parayN)
    for i in range(parayN):
        output[i].resize(paraxN+2)
    
    cdef:
        int index
        vector[vector[double]] datax_c = datax
        vector[vector[double]] datay_c = datay
        int threads_c = threads

    for index in prange(parayN, nogil=True, schedule='static', num_threads=threads_c):
        fit_storersd_c(datay_c[index],
                       datax_c,
                       output[index])

    return output

cdef int fit_storersd_c(vector[double] datay, vector[vector[double]] datax, vector[double] &output) nogil:
    cdef:
        vector[double] result
    
    result = reg_storersd(datay, datax)
    for i in range(result.size()):
        output[i] = result[i]

    return 1