# -*- coding: utf-8 -*-

from etfe import ETFE, sys_frq_rep
from time import time
from comput_module import sysid_invfreqs, phase
from bodeplot_module import bode_plot
from scipy.optimize import curve_fit
import matplotlib.patches as mpatches
from scipy import signal
from numpy import inf
import matplotlib.pyplot as plt
import numpy as np


def func(x, a, b, c, d, e, f, g, h, i, j):
    return (g * x ** 3 + h * x ** 2 + i * x ** 1 + j) /\
           (a * x ** 5 + b * x ** 4 + c * x ** 3 + d * x ** 2 + e * x ** 1 + f)


def calc_bode_plot(tfreq_h, H):
    mag_t = []
    pha_t = []
    for i in range(len(tfreq_h)):
        mag_t.append(20 * np.log10(np.linalg.norm(H[i])))
        pha_t.append(np.rad2deg(phase(H[i])))
    return mag_t, pha_t


if __name__ == '__main__':
    file = open("testcode.txt", "r")
    lines = file.readlines()
    timex = []
    input = []
    output = []
    for line in lines:
        timex.append(float(line.split(' ')[0]))
        input.append(float(line.split(' ')[1]))
        output.append(float(line.split(' ')[2]))
    file.close()
    # n = 1024. * 16
    n = 20001
    t0 = time()
    # t_freq_h: units (Hz)
    # t_mag: units (DB)
    # t_phase: units (Deg)
    tfreq, tfreq_h, tmag_sys, tphase, imag_value, real_value = \
        ETFE(input, 0.0005, n, output)

    mag, pha, r, i = sys_frq_rep(0.01, real_value, imag_value, tfreq, tmag_sys, tphase)

    complex_number = np.zeros(len(imag_value), dtype=complex)
    complex_number.imag = np.array(imag_value)
    complex_number.real = np.array(real_value)

    graw = np.ones(20001, dtype=complex)
    graw.imag = np.array(i)
    graw.real = np.array(r)

    # print(len(tfreq_h))
    wt = []
    for i in range(20001):
        # wt.append(1.0)
        if i <= 2000:
            wt.append(10.0)
        elif 2000 < i <= 16000:
            wt.append(20.0)
        else:
            wt.append(10.0)

    omega = np.array([np.pi / 10 * i for i in range(1, 20002)])
    tfreq_h = omega
    wwt = np.array(tfreq_h, dtype=np.complex)

    # error_tmp = []
    # block_tmp = []
    # for i in range(13, 2, -1):
    #     num, den, error = sysid_invfreqs(graw, wwt, i - 1, i, np.array(wt), 30, 0.0000000001)
    #     sys = signal.TransferFunction(num, den)
    #     W, H = signal.freqresp(sys, w=tfreq_h)
    #     # print(error.real)
    #     error_tmp.append(error.real.tolist()[0][0])
    #     block_tmp.append(i)
    #
    # red_patch = mpatches.Patch(color='blue', label='The error of fitting')
    # plt.stem(block_tmp, error_tmp, '-.')
    # plt.legend(handles=[red_patch])
    # plt.show()
    # num, den, error = sysid_invfreqs(graw, wwt, 12, 13, np.array(wt), 30, 0.0000000001)
    num, den, error = sysid_invfreqs(graw, wwt, 3, 5, np.array(wt), 30, 0.0000000001)
    sys = signal.TransferFunction(num, den)
    with open("../ga_algorithm/Output.txt", 'r') as text_file:
        a = []
        for line in text_file:
            a.append(float(line.rstrip()))

    # a = np.array(tmp[0].split(" ,"))
    # print(a)
    # bb = [float(i) for i in a]
    # a = bb

    nunm = [a[5], a[6], a[7], a[8]]
    dend = [1, a[0], a[1], a[2], a[3], a[4]]

    sys2 = signal.TransferFunction(nunm, dend)

    # nunm = [a[7], a[8], a[9], a[10], a[11], a[12]]
    # dend = [1, a[0], a[1], a[2], a[3], a[4], a[5], a[6]]
    #
    # sys2 = signal.TransferFunction(nunm, dend)

    W, H = signal.freqresp(sys, w=tfreq_h)
    ww, HH = signal.freqresp(sys2, w=tfreq_h)

    mag_t, pha_t = calc_bode_plot(tfreq_h, H)
    mag_tt, pha_tt = calc_bode_plot(tfreq_h, HH)

    # mag_t = []
    # pha_t = []
    # for i in range(len(tfreq_h)):
    #     mag_t.append(20 * np.log10(np.linalg.norm(H[i])))
    #     pha_t.append(np.rad2deg(phase(H[i])))
    print(time() - t0)
    tfreq_h = tfreq_h / (np.pi * 2)
    # w, mag1, phase1 = signal.bode(sys, w=tfreq_h)
    test = bode_plot(tfreq_h, [mag, mag_t, mag_tt], [pha, pha_t, pha_tt], True)
    # test = bode_plot(tfreq_h, [mag_tt, mag_t], [pha_tt, pha_t], True)
