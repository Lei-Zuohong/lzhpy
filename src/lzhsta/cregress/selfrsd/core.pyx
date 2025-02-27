# cython: boundcheck=False, wraparound=False, initializedcheck=False, cdivision=True, nonecheck=False
from libcpp.vector cimport vector
from cython.parallel cimport prange

cdef extern from "core.hpp":
    vector[double] reg_selfrsd(vector[vector[double]] data, int index) nogil

def fit_selfrsd(data, threads):
    cdef:
        int paraN = len(data)
        int dataN = len(data[0])
        vector[vector[double]] output

    output.resize(paraN)
    for i in range(paraN):
        output[i].resize(paraN+1)
    
    cdef:
        int index
        vector[vector[double]] data_c = data
        int threads_c = threads

    for index in prange(paraN, nogil=True, schedule='static', num_threads=threads_c):
        fit_selfrsd_c(data_c,
                      index,
                      output[index])

    return output

cdef int fit_selfrsd_c(vector[vector[double]] data, int index, vector[double] &output) nogil:
    cdef:
        vector[double] result
    
    result = reg_selfrsd(data, index)
    for i in range(result.size()):
        output[i] = result[i]

    return 1
