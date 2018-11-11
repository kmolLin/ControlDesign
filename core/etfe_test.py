# etfe test

import numpy as np
from typing import List
from math import ceil, sqrt, pi, cos, atan2, degrees
from numpy.fft import fft


def ETFE(input: List[float], Ts: float, N: int, output:List[float]):
    """
    input = []
    Ts = time
    N = Number
    output = float
    """
    M = 150
    #output = np.zeros(N)
    index = 1

    yd = np.zeros(N, dtype=complex)
    ud = np.zeros(N, dtype=complex)

    Ncap = len(input)

    U = np.array(input, dtype=float)
    Y = np.array(output, dtype=float)
    a = np.array([])

    if Ncap < N:
        start = int(N - Ncap - index)
        end = N
        i = start
        while i < end:
            U[i] = 0.
            Y[i] = 0.
            i = i + 1
    else:
        Ncap = N


    nfft = 2 * ceil(Ncap / N) * N
    L = nfft

    U.resize(nfft)
    Y.resize(nfft)

    if M < 0:
        M = 1
    else:
        M = M

    M /= 2
    M1 = int((L / M))# 109
    sc = int(L / (2 * N)) # sc = 1

    Y = fft(Y)
    U = fft(U)

    start = int(L - M1 + 2 - index)
    end = int(L - index)

    # YYsize
    YY = np.array([], dtype=complex)
    YY.resize((end - start + 1))

    UU = np.array([], dtype=complex)
    UU.resize((end - start + 1))
    cnt = 0

    i = start
    while i < end:
        YY[cnt] = Y[i]
        UU[cnt] = U[i]
        cnt = cnt + 1
        i = i + 1

    YY = np.append(YY, Y)
    UU = np.append(UU, U)

    for i in range(len(YY)):
        real = YY[i].real * UU[i].real + YY[i].imag * UU[i].imag
        imag = YY[i].imag * UU[i].real - YY[i].real * UU[i].imag
        YY[i] = complex(real, imag)

    for i in range(len(UU)):
        real = pow(sqrt(pow(UU[i].real, 2) + pow(UU[i].imag, 2)), 2)
        imag = 0.0
        UU[i] = complex(real, imag)

    # Hamaing Window
    if M1 > 1:

        ha = np.array([], dtype=float)
        ha.resize((M1 + 1))
        # TODO : May M1 need to + 1
        for i in range(int(M1) + 1):
            ha[i] = (0.54 - 0.46 * cos(2 * pi * i / M1))

        ha_norm = Norm(ha)

        for i in range(int(M1) + 1):
            ha[i] /= pow(ha_norm, 2)

        a.resize(1)
        a[0] = 1

        YY = Filter(ha, a, YY)
        UU = Filter(ha, a, UU)

    start = int(M1 + (M1 / 2) + sc - index)
    end = int(M1 + (M1 / 2) + L / 2 - index)
    cnt = 0

    i = start
    while i < end:
        yd[cnt] += YY[i]
        cnt = cnt + 1
        i += sc

    cnt = 0
    start = int(M1 + (M1 / 2) + sc - index)
    end = int(M1 + (M1 / 2) + L / 2)
    i = start
    while i < end:
        ud[cnt] += UU[i]
        cnt = cnt + 1
        i += sc

    # results of frequency, magnitude, and phase.
    frq_res = pi / (N * Ts)
    tfreq = []
    tfreq_h = []
    real, imag = np.array([], dtype=complex), np.array([], dtype=complex)
    real.resize(N)
    imag.resize(N)
    tmag = []
    tphase = []

    for i in range(N):
        tfreq.append((i + 1) * frq_res)
        tfreq_h.append(tfreq[i] / (2 * pi))
        real = (yd[i].real * ud[i].real + yd[i].imag * ud[i].imag) / \
                  (pow(ud[i].real, 2) + pow(ud[i].imag, 2))
        imag = (yd[i].imag * ud[i].real - yd[i].real * ud[i].imag) / \
                  (pow(ud[i].real, 2) + pow(ud[i].imag, 2))
        tmag.append(degrees(float(sqrt(pow(real, 2) + pow(imag, 2)))))
        tphase.append(float(atan2(imag, real)))

    #print(tmag)
    #print(tfreq, tfreq_h, real, imag, tmag, tphase)


    import matplotlib.pyplot as plt
    plt.figure("Mag")
    plt.semilogx(tfreq_h, tmag)
    plt.figure("Phase")
    plt.semilogx(tfreq_h, tphase)
    plt.show()



def Filter(b, a, x):
    """
    :param b: filiter
    :param a: a[]
    :param x: data
    :return:
    """

    alen = len(a)
    blen = len(b)
    index = len(x)
    xx = np.zeros(blen, dtype=complex)
    yy = np.zeros(alen, dtype=complex)
    y = np.array([], dtype=complex)
    tmp = np.array([], dtype=complex)

    #print(alen, blen, index)
    xx.resize(blen)
    yy.resize(alen)
    y.resize(index)
    ca = a
    cb = b
    tmp = x

    i = 1
    while i < alen:
        ca[i] /= ca[0]
        i = i + 1
    i = 0
    while i < index:
        yy[0] = 0
        xx[0] = tmp[i]
        j = 0
        real_value = 0
        imag_value = 0
        while j < blen:
            real_value += cb[j] * xx[j].real
            imag_value += cb[j] * xx[j].imag
            j = j + 1
        y[i] = complex(real_value, imag_value)
        j = 1
        while j < alen:
            real_value -= ca[j] * yy[j].real
            imag_value -= ca[j] * yy[j].imag
            j = j + 1
        y[i] = complex(real_value, imag_value)
        j = blen - 1
        while j > 0:
            xx[j] = xx[j - 1]
            j = j - 1

        j = alen - 1
        while j > 0:
            yy[i] = yy[j - 1]
            j = j - 1

        i = i + 1

    return y

def Norm(x):
    sum = 0.
    tmp = x

    for i in range(len(tmp)):
        sum += pow(tmp[i], 2)

    return sqrt(sum)


if __name__ == '__main__':
    file = open("testcode.txt", "r")
    lines = file.readlines()
    time = []
    input = []
    output = []
    for line in lines:
        time.append(float(line.split(' ')[0]))
        input.append(float(line.split(' ')[1]))
        output.append(float(line.split(' ')[2]))
    n = 16384
    ETFE(input, 0.0005, n, output)
