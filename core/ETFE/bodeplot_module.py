# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import math
from typing import List


def bode_plot(omega: List, mag: List, phase: List):

    fig = plt.gcf()
    ax_mag = None
    ax_phase = None
    ax_mag = plt.subplot(211, label='control-bode-magnitude')
    ax_phase = plt.subplot(212, label='control-bode-phase', sharex=ax_mag)
    pltline = ax_mag.semilogx(omega, mag)

    ax_mag.grid(True, which='both')
    ax_mag.set_ylabel("Magnitude (dB)")

    phase_plot = phase
    ax_phase.semilogx(omega, phase_plot)
    ax_phase.set_ylabel("Phase (deg)")

    def gen_Zero_Centered_Series(val_min, val_max, period):
        v1 = np.ceil(val_min / period - 0.2)
        v2 = np.floor(val_max / period + 0.2)
        return np.arange(v1, v2 + 1) * period

    ylim = ax_phase.get_ylim()
    ax_phase.set_yticks(gen_Zero_Centered_Series(ylim[0], ylim[1], 45.))
    ax_phase.set_yticks(gen_Zero_Centered_Series(ylim[0], ylim[1], 15.), minor=True)
    ax_phase.grid(True, which='both')
    ax_phase.set_xlabel("Frequency (Hz)")

    plt.show()
