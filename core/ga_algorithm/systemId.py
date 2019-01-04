# ** utf-8 **

from fitnessfunc import Fitne
from rga import Genetic
import numpy as np
from scipy import signal as sg
import matplotlib.pyplot as plt
from de import Differential
from time import time
from gatest import calcc2d

uplimit = pow(6280, 3)
low = 0 # -uplimit

upper = [uplimit] * 13
lower = [low] * 13

def test_algorithm_rga(data_time_step, u_input_data, y_output_data):
    """Real-coded genetic algorithm."""
    fun1 = Genetic(Fitne(data_time_step, u_input_data, y_output_data, upper, lower), {
        'maxGen': 50,
        'report': 10,
        # 'minFit': 1,
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


if __name__ == "__main__":
    path = "../ETFE/testcode.txt"

    file = open(path, "r")
    lines = file.readlines()
    timex = []
    dt = []
    ut = []
    for line in lines:
        timex.append(float(line.split(' ')[0]))
        dt.append(float(line.split(' ')[1]))
        ut.append(float(line.split(' ')[2]))
    file.close()

    uc = np.array(dt) + np.array(ut)
    yt = -(np.array(ut) / 0.1)

    # plt.plot(timex, yt)
    # plt.plot(timex, uc)
    # plt.show()

    t0 = time()
    a, b = test_algorithm_rga(len(timex), uc, yt)
    print(a)
    print(b)
    print(time() - t0)

    dd, d1, d3d = sg.cont2discrete((
        [a[5], a[6], a[7], a[8]],
        [1, a[0], a[1], a[2], a[3], a[4]]), 0.0005, method="bilinear")
    # tout, yout = sg.dlsim(([a[7], a[8], a[9], a[10], a[11], a[12]],
    #                       [1, a[0], a[1], a[2], a[3], a[4], a[5], a[6]], 0.0005), uc)
    t, yout = calcc2d(uc, dd[0], d1, d3d)

    testplot = plt.figure('Real and Simulation output')
    ax1 = testplot.add_subplot(1, 1, 1)
    plt.xlabel("Time (sec)")
    plt.ylabel("Voltage (v)", color='b')
    ax1.plot(t, yt, 'b')
    axR = testplot.add_subplot(1, 1, 1, sharex=ax1, frameon=False)
    axR.yaxis.tick_right()
    axR.yaxis.set_label_position("right")
    axR.plot(t, yout, 'r')
    plt.ylabel("Voltage (v)", color='r')
    # plt.show()
    # exit()
    iteration = []
    fit_valued = []
    timexxx = []
    for it, fit_value, time in b:
        iteration.append(it)
        fit_valued.append(fit_value)
        timexxx.append(time)

    fitness_lose = plt.figure('Fitness')
    ax2 = fitness_lose.add_subplot(111)
    ax2.plot(iteration, fit_valued)
    plt.title("Convergence Graph")
    plt.xlabel("iteration")
    plt.ylabel("fitness value")

    in_out = plt.figure('Modeling Output and Input')
    ax3 = in_out.add_subplot(1, 1, 1)
    plt.title("Time domain signals for system identification")
    plt.xlabel("Time (sec)")
    plt.ylabel("Voltage (v)", color='b')
    ax3.plot(timex, dt, 'b')
    ax3R = in_out.add_subplot(1, 1, 1, sharex=ax1, frameon=False)
    ax3R.yaxis.tick_right()
    ax3R.yaxis.set_label_position("right")
    ax3R.plot(timex, yout, 'r')
    plt.ylabel("Voltage (v)", color='r')

    plt.show()
    with open("Output.txt", "w") as text_file:
        for i in a:
            text_file.write(f"{str(i)}\n")



