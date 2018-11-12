# fitness fuc

from verify cimport Verification
from scipy.interpolate import interp1d
from scipy.signal import bode, lti
import numpy as np
cimport numpy as np
from numpy cimport float64_t, ndarray


cdef class Fitne(Verification):

    cdef ndarray data_mag, freqdata, lower, upper
    cdef int data_len
    
    def __cinit__(self, freq_data:list, data_of_mag:np.ndarray, limitup:list, limitlow:list):
        # kp/(1,1,2+kp)
        # self.block = block
        self.data_mag = data_of_mag
        self.upper = np.array(limitup)
        self.lower = np.array(limitlow)
        self.freqdata = np.array(freq_data)
        self.data_len = len(self.freqdata)
        
    def __call__(self, ndarray[float64_t, ndim=1] v):
        return self.run(v)
        
    cdef int get_nParm(self):
        return 8
    
    cdef ndarray[float64_t, ndim=1] get_upper(self):
        return self.upper
    
    cdef ndarray[float64_t, ndim=1] get_lower(self):
        return self.lower
    
    cdef double run(self, np.ndarray v):

        if v[0] == 0 or v[3] == 0:
            return 999999999
        system = lti([v[0], v[1], v[2]], [v[3], v[4], v[5], v[6], v[7]])
        w, mag, phase = bode(system, w=self.freqdata, n=self.data_len)
        return sum(np.hypot(self.data_mag, mag))
    
    cpdef object get_result(self, ndarray[float64_t, ndim=1] v):
        return v
        
        
        
