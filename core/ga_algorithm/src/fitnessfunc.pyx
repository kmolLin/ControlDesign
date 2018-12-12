# fitness fuc

from verify cimport Verification
from scipy.interpolate import interp1d
from scipy.signal import bode, lti
import numpy as np
cimport numpy as np
from scipy.signal import step, TransferFunction, cont2discrete
from numpy cimport float64_t, ndarray


cdef class Fitne(Verification):

    cdef ndarray , u_input_data, lower, upper, y_output_data
    cdef int data_len
    cdef int data_time_step
    
    def __cinit__(self, data_time_step:int, u_input_data:np.ndarray, y_output_data:np.ndarray,
                  limitup:list, limitlow:list):
        # kp/(1,1,2+kp)
        # self.block = block
        self.data_time_step = data_time_step
        self.upper = np.array(limitup)
        self.lower = np.array(limitlow)
        self.u_input_data = np.array(u_input_data)
        # self.data_len = len(self.freqdata)
        self.y_output_data = y_output_data
        
    def __call__(self, ndarray[float64_t, ndim=1] v):
        return self.run(v)


    cdef list calcc2d(self, e:np.ndarray, num:np.ndarray, den:np.ndarray ,sampletime:float):
        cdef list u = []
        cdef int k, i, io
        cdef double sum1, sum2
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

    cdef int get_nParm(self):
        return 2
    
    cdef ndarray[float64_t, ndim=1] get_upper(self):
        return self.upper
    
    cdef ndarray[float64_t, ndim=1] get_lower(self):
        return self.lower
    
    cdef double run(self, np.ndarray v):
        cdef np.ndarray dd, d1, a
        cdef float d3d
        cdef list u = []
        u = []

        if v[0] == 0:
            return 999999999
        # num =
        # den =
        # tf = TransferFunction([v[0]], [1, v[1]])
        # t, yout = step(tf)
        a = np.ones(self.data_time_step)

        dd, d1, d3d = cont2discrete(([v[0]], [1, v[1]]), 0.01, method="bilinear")
        u = self.calcc2d(a, dd[0], d1, d3d)

        return sum(np.sqrt(np.square(np.array(u) - self.y_output_data)))
    
    cpdef object get_result(self, ndarray[float64_t, ndim=1] v):
        return v
        
        
        
