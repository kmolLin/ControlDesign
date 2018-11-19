#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np


def sysid_invfreqs(g, w, Nb, Na, wf, iter, tor):

    nk = 0.0
    Nb = Nb + 0 + 1
    nm = max(Na + 1, Nb + nk)
    inda = np.linspace(Na - 1, 0, num=Na, dtype=np.int16)
    indb = np.linspace(Nb - 2, 0, num=Nb, dtype=np.int16)
    indg = np.linspace(Na + 1, 0, num=Na + 1, dtype=np.int16)
    maxiter = iter
    w_f = np.sqrt(wf)
    OM = np.ones(len(w), dtype=np.complex)

    for kom in range(1, nm - 1):
        OM = np.r_['0,2', OM, (w * 1j) ** kom]


    Dva = np.dot(np.transpose(OM[inda, :]), (np.tile(g, (Na, 1))))
    Dvb = np.transpose(-(OM[indb, :]))
    # TODO : need to check value
    print(Dva.shape)
    print(Dvb.shape)
    # print(-(OM[indb, :]))

    D = np.dot(np.vstack((Dva, Dvb)), (np.tile(w_f, (Na + Nb, 1))))
    R = D * D
    Vd = D * ((-g * OM[Na+1, :]).transpose() * w_f)
    R = R.real
    Vd = Vd.real
    th = Vd / R

    a = th[1: Na].transpose()
    # a = np.vstack()
    b = np.vstack((np.zeros(1, nk), np.transpose(th[Na+1: Na+Nb])))
    v = np.roots(a)
    vind = np.where(v.real > 0)
    v[vind] = -v[vind]
    a = np.poly(v)






if __name__ == '__main__':

    pass
