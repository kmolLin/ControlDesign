#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from numpy import real

def leastsquare_system(g: np.ndarray, w: np.ndarray, Nb: int,
                    Na: int, wf: np.ndarray, iter: int, tor: float):
    """
    g is a complex data in frequency domain :param g:
    w is frequency time :param w:
    Nb is num order :param Nb:
    Na is den order :param Na:
    wf is ??? :param wf:
    iterations :param iter:
    a smaller number:param tor:
    (num, den, error):return:
    """
    nk = 0.0
    Nb = Nb + 1
    nm = max(Na + 1, int(Nb + nk))
    inda = np.linspace(Na - 1, 0, num=Na, dtype=np.int16)
    indb = np.linspace(Nb - 1, 0, num=Nb, dtype=np.int16)
    indg = np.linspace(Na, 0, num=Na + 1, dtype=np.int16)
    length_data = len(g)
    w_f = np.sqrt(wf)
    OM = np.ones(len(w), dtype=np.complex128)
    tol = 0.000000001

    # Y = AX
    # bulid init the A matrix
    for kom in range(1, nm):
        OM = np.r_['0,2', OM, (w * 1j) ** kom]

    Dva = (OM[inda, :]).T * (g.reshape((length_data, 1)) * np.ones((1, Na)))
    Dvb = np.transpose(-(OM[indb, :]))
    # TODO: ask the w_f using where ?
    ori_A = np.column_stack((Dva, Dvb)) * w_f.reshape((length_data, 1)) * np.ones((1, Na + Nb))

    ori_Y = ((-g * np.transpose(OM[Na, :])) * w_f)
    ori_X = np.linalg.solve(real(ori_A.T @ ori_A),  real(ori_A.T @ ori_Y))

    # process the a, b parameter
    a = ori_X[0: Na].T
    a = np.insert(a, 0, [1])
    b = np.transpose(ori_X[Na: Na + Nb])
    v = np.roots(a)
    vind = np.where(v.real > 0)
    v[vind] = -v[vind]
    a = np.poly(v)

    # calc the b,a transfer function frequency response
    GC = ((b.reshape((1, len(b))) @ OM[indb, :]) / (a.reshape(1, len(a)) @ OM[indg, :])).T
    e = (GC - g.reshape(length_data, 1)) * w_f.reshape((length_data, 1))
    # calc (GC - e)^2 have error
    Vcap = np.dot(e.conj().transpose(), e)
    print(b)
    print(a)
    print(Vcap)
    exit()

