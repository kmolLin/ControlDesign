# test GA 

from fitnessfunc import Fitne
from rga import Genetic
from dialogBlock import DialogBlock
from etfe import ETFE, sys_frq_rep
from scipy.signal import lti, bode
import numpy as np
from bodeplot_module import bode_plot
from scipy import signal as sg
import matplotlib.pyplot as plt

#block = DialogBlock([1], [1, 1, 2], )
upper = [100.0, 100.0]
lower = [-100.0, -100.0]


def calcc2d(e, num, den, sampletime):
    u = []
    for k, e_k in enumerate(e):
        sum1 = 0
        for i, num_i in enumerate(num):
            if k - i < 0:
                continue
            else:
                sum1 += num[i] * e[k - i]
        sum2 = 0
        for io in range(1, len(den)):
            if k == 0:
                sum2 += 0
                continue
            if k - io < 0:
                sum2 += 0
            else:
                sum2 += den[io] * u[k - io]
        u.append(sum1 - sum2)
    t = np.arange(0, sampletime * (len(e)), sampletime)
    return t, u


def test_algorithm_rga(data_time_step, u_input_data, y_output_data):
    """Real-coded genetic algorithm."""
    fun1 = Genetic(Fitne(data_time_step, u_input_data, y_output_data, upper, lower), {
        'maxGen': 100, 'report': 10,
        # Genetic
        'nPop': 100,
        'pCross': 0.95,
        'pMute': 0.05,
        'pWin': 0.95,
        'bDelta': 5.,
    })
    a, b = fun1.run()
    return a, b


if __name__ == "__main__":
    # file = open("../ETFE/testcode.txt", "r")
    # lines = file.readlines()
    # timex = []
    # input = []
    # output = []
    # for line in lines:
    #     timex.append(float(line.split(' ')[0]))
    #     input.append(float(line.split(' ')[1]))
    #     output.append(float(line.split(' ')[2]))
    # # TODO : N = 8 * 1024 ???
    # n = 1024. * 16
    # # t_freq_h: units (Hz)
    # # t_mag: units (DB)
    # # t_phase: units (Deg)
    # tfreq, tfreq_h, tmag_sys, tphase, imag_value, real_value = \
    #     ETFE(input, 0.0005, n, output)
    # mag, pha = sys_frq_rep(0.01, real_value, imag_value, tfreq,
    #                        tmag_sys, tphase)

    # print(tfreq_h[:10])
    # print(len(tfreq_h))
    # print(len(mag))
    num = [10]
    den = [1, 10]
    tf = sg.TransferFunction(num, den)
    t, yout = sg.step(tf)
    a = np.ones(len(t))
    a, b = test_algorithm_rga(len(t), a, yout)
    print(a)
    #
    # dd, d1, d3d = sg.cont2discrete((num, den), 0.002, method="bilinear")
    # t, u = calcc2d(a.tolist(), dd[0], d1, d3d)
    # print(type(yout))
    # plt.plot(t, u, 'r')
    # plt.plot(t, u, 'g')
    # plt.show()

    # a, b = test_algorithm_rga(tfreq_h, mag)
    # print(a)
    # system = lti([a[0], a[1], a[2]], [a[3], a[4], a[5], a[6], a[7]])
    # w, mag, phase = bode(system, w=np.array(tfreq_h))
    # bode_plot(w, mag, phase, True)
    # fig, ax = plt.subplots()
    # ax.plot(T, yout)
    # plt.show()

