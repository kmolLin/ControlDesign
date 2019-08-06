# -*- coding: utf-8 -*-
# cython: language_level=3
# fitness fuc

from .Adesign.verify cimport Verification
import numpy as np
cimport numpy as np
from numpy cimport float64_t, ndarray


cdef list calcc2d(
    ndarray[float64_t, ndim=1] e,
    ndarray[float64_t, ndim=1] num,
    ndarray[float64_t, ndim=1] den,
    long double sampletime
):
    cdef list u = []
    cdef int k, i, io
    cdef long double sum1, sum2
    for k, e_k in enumerate(e):
        sum1 = 0

        for i, num_i in enumerate(num):
            if k - i < 0:
                continue
            else:
                sum1 += num[i] * e[k - i]
        sum2 = 0
        for io in range(1, len(den)):
            if k == 0:
                sum2 += 0
                continue
            if k - io < 0:
                sum2 += 0
            else:
                sum2 += den[io] * u[k - io]
        u.append(sum1 - sum2)
    return u


cdef class Fitne(Verification):

    cdef ndarray  u_input_data, lower, upper,\
        y_output_data, timess, allparameter, orignal_g, \
        OM, indb, indg, w_f
    cdef int data_len, tmp_a_len, blen
    cdef int data_time_step, lendata
    
    def __cinit__(self,
        int data_time_step,
        ndarray[float64_t, ndim=1] tmp_a,
        ndarray[float64_t, ndim=1] b,
        ndarray[complex, ndim=1] orignal_g,
        limitup,
        limitlow,
        OM,
        indb,
        indg,
        w_f,
    ):
        # kp/(1,1,2+kp)
        # self.block = block
        self.data_time_step = data_time_step
        self.upper = np.array(limitup)
        self.lower = np.array(limitlow)
        self.tmp_a_len = len(tmp_a)
        self.blen = len(b)
        self.allparameter = np.append(tmp_a, b)
        self.orignal_g = orignal_g
        self.OM = OM
        self.indb = indb
        self.indg = indg
        self.w_f = w_f
        self.lendata = len(orignal_g)

        self.timess = np.linspace(0, 10, 10001)
        # self.data_len = len(self.freqdata)


    cdef int get_nParm(self):
        return len(self.allparameter)
    
    cdef ndarray[float64_t, ndim=1] get_upper(self):
        return self.upper
    
    cdef ndarray[float64_t, ndim=1] get_lower(self):
        return self.lower
    
    cdef double fitness(self, np.ndarray v):
        cdef np.ndarray dd, d1, a, b
        cdef long double d3d, tt
        cdef long complex gc

        a, b = np.split(v, [self.tmp_a_len])
        a = np.insert(a, 0, [1])
        GC = ((b.reshape((1, len(b))) @ self.OM[self.indb, :]) /
              (a.reshape(1, len(a)) @ self.OM[self.indg, :])).T
        e = (GC - self.orignal_g.reshape(self.lendata, 1)) * self.w_f.reshape((self.lendata, 1))
        Vcap = np.dot(e.conj().transpose(), e)
        return np.real(Vcap)

    cpdef object result(self, ndarray[float64_t, ndim=1] v):
        return v
