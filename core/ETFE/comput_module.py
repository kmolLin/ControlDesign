#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np


def sysid_invfreqs(g, w, Nb, Na, wf, iter, tor):

    nk = 0.0
    Nb = Nb + 1
    nm = max(Na + 1, Nb + nk)
    inda = np.linspace(Na - 1, 0, num=Na, dtype=np.int16)
    indb = np.linspace(Nb - 2, 0, num=Na, dtype=np.int16)
    indg = np.linspace(Na, 0, num=Na + 1, dtype=np.int16)
    maxiter = iter
    w_f = np.sqrt(wf)
    OM = np.ones(len(w), dtype=np.complex)

    for kom in range(1, 14):
        OM = np.r_['0,2', OM, (w * 1j) ** kom]

    # print(OM[inda, :].shape)
    # print(np.transpose(np.tile(g, (Na, 1))).shape)

    # a = np.transpose(OM[inda, :])
    # print("@" * 10)
    # b = np.transpose(np.tile(g, (Na, 1)))
    Dva = np.transpose(OM[inda, :]) * np.transpose(np.tile(g, (Na, 1)))
    Dvb = np.transpose(-(OM[indb, :]))
    # TODO : need to check value and cloume
    D = np.column_stack((Dva, Dvb)) * np.transpose(np.tile(w_f, (Na + Nb - 1, 1)))
    R = np.dot(D.conj().T, D)
    Vd = np.dot(D.conj().T, ((-g * np.transpose(OM[Na, :])) * w_f))
    R = R.real
    Vd = Vd.real

    th = np.linalg.solve(R, Vd)
    print(len(th))
    return

    a = th[1: Na].transpose()
    # a = np.vstack()
    b = np.vstack((np.zeros(1, nk), np.transpose(th[Na+1: Na+Nb])))
    v = np.roots(a)
    vind = np.where(v.real > 0)
    v[vind] = -v[vind]
    a = np.poly(v)






if __name__ == '__main__':

    pass
