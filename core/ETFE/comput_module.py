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
    OM = np.ones(len(w), dtype=np.complex128)
    omega = np.array([np.pi / 10 * i for i in range(1, 20002)])

    for kom in range(1, 14):
        OM = np.r_['0,2', OM, (omega * 1j) ** kom]

    Dva = (OM[inda, :]).T * (g.reshape((20001, 1)) * np.ones((1, 13)))
    Dvb = np.transpose(-(OM[indb, :]))
    # TODO : need to check value and cloume
    D = np.column_stack((Dva, Dvb)) * w_f.reshape((20001, 1)) * np.ones((1, Na + Nb - 1))
    R = np.dot(D.conj().T, D)
    Vd = np.dot(D.conj().T, ((-g * np.transpose(OM[Na, :])) * w_f))
    R = R.real
    Vd = Vd.real
    th = np.linalg.solve(R, Vd)
    a = th[0: Na].T
    a = np.insert(a, 0, [1])
    b = np.transpose(th[Na: Na+Nb])

    v = np.roots(a)
    vind = np.where(v.real > 0)
    v[vind] = -v[vind]
    a = np.poly(v)
    # The initial estimate:
    GC = (b.reshape((1, 13)) @ OM[indb, :]) / (a.reshape(1, 14) @ OM[indg, :]).T
    e = (GC - g) * w_f
    Vcap = e.conj().transpose() * e
    t = np.hstack((a[1: Na+1], b[int(nk): int(nk+Nb)])).T
    error = np.zeros((1))
    print(Vcap)
    # error[0] = Vcap



if __name__ == '__main__':

    pass
