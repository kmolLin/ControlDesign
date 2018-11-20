# cython etfe

import numpy as np
from numpy cimport (
    ndarray,
    float64_t,
    complex128_t,
)
from libc.math cimport ceil, sqrt, pi, cos, atan2, hypot, sin
from numpy.fft import fft

# TODO : check mag plot value

cpdef tuple ETFE(list input, double Ts, int N, list output):
    """
    input = []
    Ts = time
    N = Number
    output = float
    :return
    tfreq: (Hz)
    tmag: (DB)
    tphase: (Deg)
    """
    cdef int M = 150
    cdef int index = 1
    cdef int Ncap = len(input)

    cdef ndarray[complex128_t, ndim=1] yd = np.zeros(N, dtype=np.complex128)
    cdef ndarray[complex128_t, ndim=1] ud = np.zeros(N, dtype=np.complex128)
    cdef ndarray[complex128_t, ndim=1] U = np.array(input, dtype=np.complex128)
    cdef ndarray[complex128_t, ndim=1] Y = np.array(output, dtype=np.complex128)

    cdef int i, start, end
    if Ncap < N:
        start = int(N - Ncap - index)
        end = N
        i = start
        while i < end:
            U[i] = 0j
            Y[i] = 0j
            i = i + 1
    else:
        Ncap = N

    cdef int nfft = 2 * <int>ceil(Ncap / N) * N
    cdef int L = nfft

    U.resize(nfft, refcheck=False)
    Y.resize(nfft, refcheck=False)

    M = 1 if M < 0 else M
    M /= 2
    M1 = int((L / M))# 109
    cdef int sc = int(L / (2 * N))# sc = 1

    # U : input signal
    # Y : output signal
    Y = fft(Y)
    U = fft(U)

    start = int(L - M1 + 2 - index)
    end = int(L - index)
    cdef int cnt = 0

    # YYsize
    cdef ndarray[complex128_t, ndim=1] YY = np.zeros(end - start + 1, dtype=np.complex128)
    cdef ndarray[complex128_t, ndim=1] UU = np.zeros(end - start + 1, dtype=np.complex128)

    for i in range(start, end):
        YY[cnt] = Y[i]
        UU[cnt] = U[i]
        cnt += 1
    YY = np.append(YY, Y)
    UU = np.append(UU, U)

    cdef double real, imag
    # YY =  YY * UU
    for i in range(len(YY)):
        real = YY[i].real * UU[i].real + YY[i].imag * UU[i].imag
        imag = YY[i].imag * UU[i].real - YY[i].real * UU[i].imag
        YY[i] = complex(real, imag)

    # UU = hypot(UU) + 0j
    cdef double tmp
    for i in range(len(UU)):
        tmp = hypot(UU[i].real, UU[i].imag)
        real = tmp * tmp
        imag = 0.0
        UU[i] = complex(real, imag)

    # Hamaing Window
    cdef ndarray[float64_t, ndim=1] ha, a
    cdef double ha_norm
    if M1 > 1:

        ha = np.zeros(M1 + 1, dtype=np.float64)
        for i in range(int(M1) + 1):
            ha[i] = (0.54 - 0.46 * cos(2 * pi * i / M1))

        ha_norm = Norm(ha)

        for i in range(int(M1) + 1):
            ha[i] /= (ha_norm * ha_norm)

        a = np.zeros(1, dtype=np.float64)
        a[0] = 1

        YY = Filter(ha, a, YY)
        UU = Filter(ha, a, UU)

    start = int(M1 + (M1 / 2) + sc - index)
    end = int(M1 + (M1 / 2) + L / 2 - index)
    cnt = 0
    for i in range(start, end, sc):
        yd[cnt].real += YY[i].real
        yd[cnt].imag += YY[i].imag
        cnt = cnt + 1

    cnt = 0
    end = int(M1 + (M1 / 2) + L / 2)
    for i in range(start, end, sc):
        ud[cnt].real += UU[i].real
        ud[cnt].imag += UU[i].imag
        cnt = cnt + 1

    # results of frequency, magnitude, and phase.
    cdef double frq_res = pi / (N * Ts)
    cdef list tfreq = []
    cdef list tfreq_h = []
    cdef list real_value = []
    cdef list imag_value = []
    cdef list tmag = []
    cdef list tphase = []
    cdef double tmp_clear = 0.

    for i in range(N):
        tfreq.append((i + 1) * frq_res)
        tfreq_h.append(tfreq[i] / (2 * pi))
        den = (ud[i].real * ud[i].real + ud[i].imag * ud[i].imag)
        real_value.append((yd[i].real * ud[i].real + yd[i].imag * ud[i].imag) / den)
        imag_value.append((yd[i].imag * ud[i].real - yd[i].real * ud[i].imag) / den)
        tmag.append(hypot(real_value[i], imag_value[i]))
        tphase.append(atan2(imag_value[i], real_value[i]))

    return tfreq, tfreq_h, tmag, tphase, imag_value, real_value

cdef ndarray[complex128_t, ndim=1] Filter(
    ndarray[float64_t, ndim=1] b,
    ndarray[float64_t, ndim=1] a,
    ndarray[complex128_t, ndim=1] x
):
    """
    :param b: filiter
    :param a: a[]
    :param x: data
    :return:
    """

    cdef int alen = len(a)
    cdef int blen = len(b)
    cdef int index = len(x)
    cdef ndarray[complex128_t, ndim=1] xx = np.zeros(blen, dtype=np.complex128)
    cdef ndarray[complex128_t, ndim=1] yy = np.zeros(alen, dtype=np.complex128)
    cdef ndarray[complex128_t, ndim=1] y = np.zeros(index, dtype=np.complex128)

    cdef ndarray[float64_t, ndim=1] ca = a
    for i in range(1, alen):
        ca[i] /= ca[0]

    cdef double real_value, imag_value
    cdef int j
    for i in range(0, index):
        yy[0] = 0j
        xx[0] = x[i]

        j = 0
        real_value = 0
        imag_value = 0

        for j in range(0, blen):
            real_value += b[j] * xx[j].real
            imag_value += b[j] * xx[j].imag

        for j in range(1, alen):
            real_value -= ca[j] * yy[j].real
            imag_value -= ca[j] * yy[j].imag

        y[i] = complex(real_value, imag_value)

        j = (blen - 1)
        while j > 0:
            xx[j] = xx[j - 1]
            j -= 1

        j = (alen - 1)
        while j > 0:
            yy[i] = yy[j - 1]
            j -= 1

    return y

cdef inline double Norm(ndarray x):
    return sqrt(sum(i * i for i in x))

cpdef tuple sys_frq_rep(double idkvp, list real_sys, list imag_sys,
                        list freq_r, list mag_sys, list pha_sys):

    cdef ndarray[float64_t, ndim=1] tfreq = np.array(freq_r)
    cdef ndarray[float64_t, ndim=1] mag = np.array(mag_sys)
    cdef ndarray[float64_t, ndim=1] pha = np.array(pha_sys)
    cdef ndarray[float64_t, ndim=1] r_sys = np.array(real_sys)
    cdef ndarray[float64_t, ndim=1] i_sys = np.array(imag_sys)

    cdef int n = len(freq_r)
    cdef ndarray[float64_t, ndim=1] tmag = np.zeros(n)
    cdef ndarray[float64_t, ndim=1] tphase = np.zeros(n)
    cdef ndarray[float64_t, ndim=1] retmag = np.zeros(1)
    cdef ndarray[float64_t, ndim=1] retpha = np.zeros(1)
    cdef ndarray[float64_t, ndim=1] pha_m = np.zeros(1)
    cdef ndarray[float64_t, ndim=1] pha_f = np.zeros(1)
    cdef ndarray[float64_t, ndim=1] mag_m = np.zeros(1)
    cdef ndarray[float64_t, ndim=1] mag_f = np.zeros(1)

    cdef double rad2Hz = 1 / (2 * pi)

    cdef double zr, zi, zmag, zphase, nmag, nr, ni, nphase
    for i in range(n):
        zr = -r_sys[i]
        zi = -i_sys[i]
        zmag = mag[i]
        zphase = atan2(zi, zr)

        nr = idkvp * (1 + r_sys[i])
        ni = idkvp * i_sys[i]
        nmag = hypot(ni, nr)
        nphase = atan2(ni, nr)

        mag[i] = zmag / nmag
        pha[i] = zphase - nphase
        r_sys[i] = mag[i] * cos(pha[i])
        i_sys[i] = mag[i] * sin(pha[i])

        tmag[i] = 20 * np.log10(mag[i])
        tphase[i] = np.degrees(pha[i])

    for i in range(n):
        if tmag[i] == 0 and tfreq[i] < 125.0:
            pha_m[i] = tphase[0]
            pha_f[i] = tfreq[0]
        elif (tmag[i] * retmag[0]) < 0 and tfreq[i] < 125:
            pha_m[0] = tphase[i] + 180
            pha_f[0] = tfreq[i] * rad2Hz

        if tphase[i] == -180 and tfreq[i] < 125 * 2 * pi:
            mag_m[0] = tmag[i]
            mag_f[0] = tfreq[i]

        elif tphase[i] < -180:
                if retpha[0] > -180:
                    if tfreq[i] < 125 * 2 * pi:
                        mag_m[0] = -1 / tmag[i]
                        mag_f[0] = tfreq[i] * rad2Hz

        retmag[0] = tmag[i]
        retpha[0] = abs(tphase[i] + 180)
    return tmag, tphase, r_sys, i_sys



