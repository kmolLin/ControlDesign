# -*- coding: utf-8 -*-

from etfe import ETFE, sys_frq_rep
from time import time
from comput_module import sysid_invfreqs, phase
from bodeplot_module import bode_plot
from leastsquare import leastsquare_system
from scipy import signal
from notchfilter import notch_filter
import numpy as np



def calc_bode_plot(tfreq_h, H):
    mag_t = []
    pha_t = []
    for i in range(len(tfreq_h)):
        mag_t.append(20 * np.log10(np.linalg.norm(H[i])))
        pha_t.append(np.rad2deg(phase(H[i])))
    return mag_t, pha_t


def just_fft(sample_time, input, output):
    input_tmp = np.fft.fft(input)
    output_tmp = np.fft.fft(output)


if __name__ == '__main__':
    file = open("chirpOut_Y_R_M.txt", "r")
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

    weight = []
    for i in range(20001):
        # wt.append(1.0)
        if i <= 2000:
            weight.append(10.0)
        elif 2000 < i <= 16000:
            weight.append(20.0)
        else:
            weight.append(10.0)

    # omega = np.array([np.pi / 10 * i for i in range(1, 20002)])
    # tfreq_h = omega
    wwt = np.array(tfreq, dtype=np.complex)

    num, den, error = leastsquare_system(graw, wwt, 12, 13, np.array(weight), 30, 0.0000000001)
    # num, den, error = sysid_invfreqs(graw, wwt, 13, 13, np.array(weight), 30, 0.0000000001)
    print(len(num[0]))
    print(len(den))

    sys = signal.TransferFunction(num, den)
    W, H = signal.freqresp(sys, w=tfreq)
    # ww, HH = signal.freqresp(sys2, w=tfreq)
    mag_t, pha_t = calc_bode_plot(tfreq, H)

    g_with_notch, grawNotch_mag, grawNotch_phase, freq = notch_filter(mag_t, pha_t, np.array(tfreq), num, den)
    print(time() - t0)
    tfreq = wwt / (np.pi * 2)

    # tuning second
    num1, den1, error1 = leastsquare_system(g_with_notch[0:freq], wwt[0:freq], 0, 1, np.array(weight)[0:freq], 50, 1e-10)
    sys1 = signal.TransferFunction(num1, den1)
    W1, H1 = signal.freqresp(sys1, w=wwt)
    print(num1, den1)
    mag_t_1, pha_t_1 = calc_bode_plot(wwt, H1)
    name = ["Original", "Gauss Newton", "Gauss with auto Notch", "First-order system"]
    test = bode_plot(wwt, [mag, mag_t, grawNotch_mag, mag_t_1], [pha, pha_t, grawNotch_phase, pha_t_1], name, True)
