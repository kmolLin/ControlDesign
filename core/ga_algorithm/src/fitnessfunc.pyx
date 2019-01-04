# -*- coding: utf-8 -*-
# cython: language_level=3
# fitness fuc

from verify cimport Verification
from scipy.interpolate import interp1d
from scipy.signal import bode, lti
import numpy as np
cimport numpy as np
from scipy.signal import step, TransferFunction, cont2discrete, dlsim
from numpy cimport float64_t, ndarray
from libc.math cimport HUGE_VAL


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

    cdef ndarray , u_input_data, lower, upper, y_output_data, timess
    cdef int data_len
    cdef int data_time_step
    
    def __cinit__(self,
        int data_time_step,
        ndarray[float64_t, ndim=1] u_input_data,
        ndarray[float64_t, ndim=1] y_output_data,
        limitup,
        limitlow
    ):
        # kp/(1,1,2+kp)
        # self.block = block
        self.data_time_step = data_time_step
        self.upper = np.array(limitup)
        self.lower = np.array(limitlow)
        self.u_input_data = np.array(u_input_data)
        self.timess = np.linspace(0, 10, 10001)
        # self.data_len = len(self.freqdata)
        self.y_output_data = y_output_data

    cdef int get_nParm(self):
        return 13
    
    cdef ndarray[float64_t, ndim=1] get_upper(self):
        return self.upper
    
    cdef ndarray[float64_t, ndim=1] get_lower(self):
        return self.lower
    
    cdef double run(self, np.ndarray v):
        cdef np.ndarray dd, d1, a
        cdef long double d3d
        # cdef np.ndarray u
        u = []

        # if v[5] and v[6] and v[7] == 0:
        #     return HUGE_VAL
        # dd, d1, d3d = cont2discrete((
        #     [v[5], v[6], v[7], v[8]],
        # [1, v[0], v[1], v[2], v[3], v[4]]), 0.0005, method="bilinear")

        if v[7] and v[8] and v[9] == 0:
            return HUGE_VAL
        dd, d1, d3d = cont2discrete((
            [v[7], v[8], v[9], v[10], v[11], v[12]],
        [1, v[0], v[1], v[2], v[3], v[4], v[5], v[6]]), 0.0005, method="bilinear")

        u = calcc2d(self.u_input_data, dd[0], d1, d3d)
        if sum(np.square(np.array(u) - self.y_output_data)) == np.nan:
            return HUGE_VAL
        else:
            return sum(np.square(np.array(u) - self.y_output_data))

        # _ ,u = dlsim((dd, d1, d3d), self.u_input_data, t=self.timess)

        # if sum(np.square(np.array(u, dtype=np.double) - self.y_output_data)) == np.inf or np.nan:
        #     return 999999999
        #
        # if sum(np.square(u - self.y_output_data))[0] == np.nan:
        #     return 99999999
        # else:
        #     return sum(np.square(u - self.y_output_data))

    cpdef object get_result(self, ndarray[float64_t, ndim=1] v):
        return v
