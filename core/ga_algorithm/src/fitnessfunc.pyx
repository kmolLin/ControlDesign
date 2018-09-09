# fitness fuc

from verify cimport Verification
from scipy.interpolate import interp1d
from scipy.signal import step
import numpy as np
cimport numpy as np
from dialogBlock import DialogBlock


cdef class Fitne(Verification):
    
    cdef object pidblock, block, 
    cdef double beta
    cdef np.ndarray upper, lower
    
    def __cinit__(self, block:object, beta:double, limitup:list, limitlow:list):
        # kp/(1,1,2+kp)
        self.block = block
        self.beta = beta
        self.upper = np.array(limitup)
        self.lower = np.array(limitlow)
        
    def __call__(self, np.ndarray v):
        return self.run(v)
        
    cdef int get_nParm(self):
        return 3
    
    cdef np.ndarray get_upper(self):
        return self.upper
    
    cdef np.ndarray get_lower(self):
        return self.lower
    
    cdef double run(self, np.ndarray v):
        cdef double overshoot, value, ts, ess, tr, wk
        cdef np.ndarray T, yout
        cdef object pidblock
        cdef int i
        
        tr = 0
        pidblock = (self.block * DialogBlock([v[0], v[1], v[2]], [1, 0])).cloop()
        T , yout = step((pidblock.num, pidblock.den))
        overshoot = max(yout)
        for i, value in enumerate(yout):
            if value == 1:
                tr = T[i]
                break
            elif value > 1:
                tr = T[i]-((T[i]-T[i-1])/ (value-yout[i-1]))*(value-1)
                break
        ts = T[-1]
        ess = yout[-1]
        wk = (1-np.exp(self.beta))*(overshoot+ess)+ np.exp(-1*self.beta)*(ts-tr)
        return (wk)
    
    cpdef object get_result(self, np.ndarray v):
        return v
        
        
        
