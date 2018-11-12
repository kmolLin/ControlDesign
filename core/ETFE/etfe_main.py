# -*- coding: utf-8 -*-

from etfe import ETFE, sys_frq_rep
from time import time
from bodeplot_module import bode_plot

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
    # TODO : N = 8 * 1024 ???
    n = 1024. * 16
    t0 = time()
    # t_freq_h: units (Hz)
    # t_mag: units (DB)
    # t_phase: units (Deg)
    tfreq, tfreq_h, tmag_sys, tphase, imag_value, real_value = \
        ETFE(input, 0.0005, n, output)
    #print(time() - t0)
    print(tmag_sys[0])
    mag, pha = sys_frq_rep(0.01, real_value, imag_value, tfreq,
                                    tmag_sys, tphase)

    test = bode_plot(tfreq_h, mag, pha, True)
