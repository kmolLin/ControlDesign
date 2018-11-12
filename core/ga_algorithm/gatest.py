# test GA 

from fitnessfunc import Fitne
from rga import Genetic
from dialogBlock import DialogBlock
from etfe import ETFE, sys_frq_rep
from scipy.signal import lti, bode
import numpy as np
from bodeplot_module import bode_plot
import matplotlib.pyplot as plt

#block = DialogBlock([1], [1, 1, 2], )
upper = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
lower = [-1000.0, -1000.0, -1000.0, -1000.0, -1000.0, -1000.0, -1000.0, -1000.0]


def test_algorithm_rga(tfreq_h, mag):
    """Real-coded genetic algorithm."""
    fun1 = Genetic(Fitne(tfreq_h, mag, upper, lower), {
        'maxGen': 500, 'report': 10,
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
    file = open("../ETFE/testcode.txt", "r")
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
    # t_freq_h: units (Hz)
    # t_mag: units (DB)
    # t_phase: units (Deg)
    tfreq, tfreq_h, tmag_sys, tphase, imag_value, real_value = \
        ETFE(input, 0.0005, n, output)
    mag, pha = sys_frq_rep(0.01, real_value, imag_value, tfreq,
                           tmag_sys, tphase)

    # print(tfreq_h[:10])
    # print(len(tfreq_h))
    # print(len(mag))

    a, b = test_algorithm_rga(tfreq_h, mag)
    print(a)
    system = lti([a[0], a[1], a[2]], [a[3], a[4], a[5], a[6], a[7]])
    w, mag, phase = bode(system, w=np.array(tfreq_h))
    bode_plot(w, mag, phase, True)
    # fig, ax = plt.subplots()
    # ax.plot(T, yout)
    # plt.show()

