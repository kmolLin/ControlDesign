#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from numpy import real
# TODO: need to check question why can't import
from core.ga_algorithm import test_algorithm_rga


def leastsquare_system(g: np.ndarray, w: np.ndarray, Nb: int,
                       Na: int, wf: np.ndarray, max_iter: int,
                       tor: float, method: int):
    """
    g is a complex data in frequency domain :param g:
    w is frequency time :param w:
    Nb is num order :param Nb:
    Na is den order :param Na:
    wf is weight of g (important data need to * K):param wf:
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
    ori_A = np.column_stack((Dva, Dvb)) * w_f.reshape((length_data, 1)) * np.ones((1, Na + Nb))
    ori_Y = ((-g * np.transpose(OM[Na, :])) * w_f)
    ori_X = np.linalg.solve(real(ori_A.conj().T @ ori_A),  real(ori_A.conj().T @ ori_Y))

    # process the a, b parameter
    a = ori_X[0: Na].T
    a = np.insert(a, 0, [1])
    b = np.transpose(ori_X[Na: Na + Nb])
    v = np.roots(a)
    vind = np.where(v.real > 0)
    v[vind] = -v[vind]
    a = np.poly(v)

    # calc the b, a transfer function frequency response
    GC = ((b.reshape((1, len(b))) @ OM[indb, :]) / (a.reshape(1, len(a)) @ OM[indg, :])).T
    e = (GC - g.reshape(length_data, 1)) * w_f.reshape((length_data, 1))
    # calc (GC - e)^2 have error
    Vcap = np.dot(e.conj().transpose(), e)
    error = real(Vcap)
    Matrix_X_ori = np.hstack((a[1: Na + 1], b[int(nk): int(nk + Nb)])).T
    disturbance = 2 * tol + 1
    count = 0
    st = 0.0

    # check the algorithm (default is Gauss-Newton)
    if method == 1:
        para_v, his_v = test_algorithm_rga(1000, a, b, g, OM, indb, indg, w_f)
        a, b = np.split(para_v, [13])
        a = np.insert(a, 0, [1])
        GC = ((b.reshape((1, len(b))) @ OM[indb, :]) / (a.reshape(1, len(a)) @ OM[indg, :])).T
        e = (GC - g.reshape(length_data, 1)) * w_f.reshape((length_data, 1))
        # calc (GC - e)^2 have error
        Vcap = np.dot(e.conj().transpose(), e)
        error = real(Vcap)
    elif method == 2:
        while np.linalg.norm(disturbance) > tol and count < max_iter and st != 1:
            count += 1
            # compute gradiant
            # calc jacobain matrix
            Jacobain_tmp_A = OM[inda, :].T * (-GC / (a.reshape(1, len(a)) @ OM[indg, :]).T * np.ones((1, Na)))
            Jacobain_tmp_B = OM[indb, :].T / ((a.reshape(1, len(a)) @ OM[indg, :]).T @ np.ones((1, Nb)))
            Jacobain_X = np.hstack((Jacobain_tmp_A, Jacobain_tmp_B)) * (w_f.reshape(length_data, 1) @ np.ones((1, Na + Nb)))

            # compute Gauss-Newton search direction
            e = (GC - g.reshape(length_data, 1)) * w_f.reshape((length_data, 1))
            R = real(Jacobain_X.conj().T @ Jacobain_X)
            Vd = real(Jacobain_X.conj().T @ e)
            gndir = np.linalg.solve(R, Vd)
            l1 = 0
            k = 1.0
            V1 = Vcap + 1
            matrix_X = Matrix_X_ori

            # search along the gndir-direction
            # do with gauss newton method
            while V1 > Vcap and l1 < 20:
                if l1 == 19:
                    t1 = Matrix_X_ori
                matrix_X = Matrix_X_ori.reshape((Na + Nb, 1)) - k * gndir
                a = np.insert(matrix_X[0: Na].T, 0, [1])
                b = np.transpose(matrix_X[Na: Na + Nb])
                v = np.roots(a)
                vind = np.where(v.real > 0)
                v[vind] = -v[vind]
                a = np.poly(v)
                matrix_X[0: Na] = a[1: Na + 1].T.reshape((len(a[1: Na + 1].T), 1))
                GC = ((b @ OM[indb, :]) / (a.reshape(1, len(a)) @ OM[indg, :])).T
                V1 = ((GC - g.reshape(length_data, 1)) * w_f.reshape((length_data, 1))).conj().T \
                        @ ((GC - g.reshape(length_data, 1)) * w_f.reshape((length_data, 1)))
                k = k / 2
                l1 += 1
                if l1 == 10:
                    gndir = Vd / np.linalg.norm(R) * len(R)
                    k = 1
                if l1 == 20:
                    st = 1
            Matrix_X_ori = matrix_X
            Vcap = V1
            error = V1
    elif method == 3:
        b, a, error
    return b, a, error


