# -*- coding: utf-8 -*-

from etfe import ETFE
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
    n = 1024. * 8
    t0 = time()
    # t_freq_h: units (Hz)
    # t_mag: units (DB)
    # t_phase: units (Deg)
    t_freq_h, t_mag, t_phase = ETFE(input, 0.0005, n, output)
    print(time() - t0)
    bode_plot(t_freq_h, t_mag, t_phase)
