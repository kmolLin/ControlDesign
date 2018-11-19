# -*- coding: utf-8 -*-

from etfe import ETFE, sys_frq_rep
from time import time
from bodeplot_module import bode_plot
from scipy.optimize import curve_fit
from numpy import inf
import numpy as np


def func(x, a, b, c, d, e, f, g, h, i, j):
    return (g * x ** 3 + h * x ** 2 + i * x ** 1 + j) /\
           (a * x ** 5 + b * x ** 4 + c * x ** 3 + d * x ** 2 + e * x ** 1 + f)


if __name__ == '__main__':
    file = open("test.txt", "r")
    lines = file.readlines()
    timex = []
    input = []
    output = []
    for line in lines:
        timex.append(float(line.split(' ')[0]))
        input.append(float(line.split(' ')[1]))
        output.append(float(line.split(' ')[2]))
    file.close()
    n = 1024. * 16
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

    graw = np.zeros(len(r), dtype=complex)
    graw.imag = np.array(i)
    graw.real = np.array(r)

    # test = bode_plot(tfreq_h, [mag], [pha], True)
