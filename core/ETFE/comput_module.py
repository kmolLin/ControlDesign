#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np


def sysid_invfreqs(g: np.ndarray, w: np.ndarray, Nb: int,
                    Na: int, wf: np.ndarray, iter: int, tor: float):

    nk = 0.0
    Nb = Nb + 1
    nm = max(Na + 1, Nb + nk)
    inda = np.linspace(Na - 1, 0, num=Na, dtype=np.int16)
    indb = np.linspace(Nb - 1, 0, num=Nb, dtype=np.int16)
    indg = np.linspace(Na, 0, num=Na + 1, dtype=np.int16)
    maxiter = iter
    length_data = len(g)
    w_f = np.sqrt(wf)
    OM = np.ones(len(w), dtype=np.complex128)
    # omega = np.array([np.pi / 10 * i for i in range(1, 20002)])
    tol = 0.000000001
    # TODO need to check omega value
    for kom in range(1, nm):
        OM = np.r_['0,2', OM, (w * 1j) ** kom]
    Dva = (OM[inda, :]).T * (g.reshape((length_data, 1)) * np.ones((1, Na)))
    Dvb = np.transpose(-(OM[indb, :]))
    D = np.column_stack((Dva, Dvb)) * w_f.reshape((length_data, 1)) * np.ones((1, Na + Nb))
    # TODO : A_D = D
    R = np.dot(D.conj().T, D)
    Vd = np.dot(D.conj().T, ((-g * np.transpose(OM[Na, :])) * w_f))
    # TODO : Yd = ((-g * np.transpose(OM[Na, :])) * w_f)
    R = R.real
    Vd = Vd.real
    # TODO : lose complex value
    th = np.linalg.solve(R, Vd)
    a = th[0: Na].T
    a = np.insert(a, 0, [1])
    b = np.transpose(th[Na: Na+Nb])
    v = np.roots(a)
    vind = np.where(v.real > 0)
    v[vind] = -v[vind]
    # TODO: V = Xd
    a = np.poly(v)
    # The initial estimate:
    GC = ((b.reshape((1, len(b))) @ OM[indb, :]) / (a.reshape(1, len(a)) @ OM[indg, :])).T
    e = (GC - g.reshape(length_data, 1)) * w_f.reshape((length_data, 1))
    Vcap = np.dot(e.conj().transpose(), e)
    t = np.hstack((a[1: Na+1], b[int(nk): int(nk+Nb)])).T
    error = np.zeros((1))
    error[0] = Vcap.real
    gndir = 2 * tol + 1
    count = 0
    st = 0.0
    # compute gradient
    D31 = OM[inda, :].T * (-GC / (a.reshape(1, len(a)) @ OM[indg, :]).T * np.ones((1, Na)))
    # TODO : check indb to inda
    D32 = OM[indb, :].T / ((a.reshape(1, len(a)) @ OM[indg, :]).T @ np.ones((1, Nb)))
    D3 = np.hstack((D31, D32)) * (w_f.reshape(length_data, 1) @ np.ones((1, Na + Nb)))
    while np.linalg.norm(gndir) > tol and count < maxiter and st != 1:
        count += 1

        # compute Gauss-Newton search direction
        e = (GC - g.reshape(length_data, 1)) * w_f.reshape((length_data, 1))
        R = D3.conj().T @ D3
        Vd = D3.conj().T @ e
        R = R.real
        Vd = Vd.real
        gndir = np.linalg.solve(R, Vd)
        l1 = 0
        k = 1.0
        V1 = Vcap + 1
        t1 = t

        # search along the gndir-direction
        while V1 > Vcap and l1 < 20:

            if l1 == 19:
                t1 = t
            t1 = t.reshape((Na + Nb, 1)) - k * gndir
            a = t1[0: Na].T
            a = np.insert(a, 0, [1])
            b = np.transpose(t1[Na: Na + Nb])
            v = np.roots(a)
            vind = np.where(v.real > 0)
            v[vind] = -v[vind]
            a = np.poly(v)
            t1[0: Na] = a[1: Na + 1].T.reshape((len(a[1: Na + 1].T), 1))
            GC = ((b @ OM[indb, :]) / (a.reshape(1, len(a)) @ OM[indg, :])).T
            V1 = ((GC - g.reshape(length_data, 1)) *
                  w_f.reshape((length_data, 1))).conj().T @ ((GC - g.reshape(length_data, 1)) *
                    w_f.reshape((length_data, 1)))
            k = k / 2
            l1 += 1
            if l1 == 10:
                gndir = Vd / np.linalg.norm(R) * len(R)
                k = 1
            if l1 == 20:
                st = 1
        t = t1
        Vcap = V1
        error = V1

    return b, a, error


def phase(G):
    Phi = np.arctan2(G.imag, G.real)
    # N = len(Phi)
    # DF = Phi[0: N - 1] - Phi[1: N]
    # # TODO : 3.5 is what ?
    # I = np.where(np.abs(DF) > 3.5)
    # if I != 0:
    #     Phi = Phi * 2 * np.pi * np.sign(DF[])
    return Phi
