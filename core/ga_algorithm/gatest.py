# test GA 

from fitnessfunc import Fitne
from rga import Genetic
import numpy as np
from scipy import signal as sg
import matplotlib.pyplot as plt
from de import Differential
from time import time


#block = DialogBlock([1], [1, 1, 2], )
upper = [100.0, 100.0, 100.0, 100.0]
lower = [-100, -100, -100, -100]


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
        'maxGen': 30, 'report': 10,
        # Genetic
        'nPop': 100,
        'pCross': 0.95,
        'pMute': 0.05,
        'pWin': 0.95,
        'bDelta': 5.,

        # Differential
        # 'strategy': 1,
        # 'NP': 400,
        # 'F': 0.6,
        # 'CR': 0.9,
    })
    a, b = fun1.run()
    return a, b

def plot_function(time_step, ):
    pass


if __name__ == "__main__":

    # simulation input
    time_step = np.linspace(0, 10, 10001)
    w = sg.chirp(time_step, f0=1, f1=6, t1=10, method='linear')
    white_noise = (np.random.rand(len(time_step)) - 0.5) * 0.2
    num = [2, 5]
    den = [1, 2, 10]
    tf = sg.TransferFunction(num, den)
    # aa, bb = sg.step(tf, T=time_step)
    # a = np.ones(len(time_step))
    dd, d1, d3d = sg.cont2discrete((num, den), 0.001, method="bilinear")
    aa, bb = calcc2d(w.tolist(), dd[0], d1, d3d)
    white_noise_output = np.array(bb) + white_noise


    # find model
    t0 = time()
    a, b = test_algorithm_rga(len(time_step), w, white_noise_output)
    print(a)
    # print(b)
    print(time() - t0)

    dd, d1, d3d = sg.cont2discrete(([a[2], a[3]], [1, a[0], a[1]]), 0.001, method="bilinear")
    t, yout = calcc2d(w.tolist(), dd[0], d1, d3d)
    plt.plot(aa, white_noise_output, 'r')
    plt.plot(aa, bb, 'b')
    plt.plot(t, yout, 'g')
    # plt.plot(time_step, omega_with_noise, 'r')
    # plt.plot(tt, outt)
    plt.show()


