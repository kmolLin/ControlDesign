# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from etfe import ETFE
from time import time
from scipy import signal

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
    n = 16384
    t0 = time()
    tfreq_h, tmag, tphase = ETFE(input, 0.0005, n, output)
    print(time() - t0)
    print(tmag)
    s1 = signal.lti([1], [1, 1])

    plt.figure("Mag")
    plt.semilogx(tfreq_h, tmag)
    plt.figure("Phase")
    plt.semilogx(tfreq_h, tphase)
    plt.show()
