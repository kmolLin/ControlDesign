# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from typing import List

__all__ = ['bode_plot']


def bode_plot(omega: List, mag: List, phase: List):

    fig = plt.gcf()
    ax_mag = None
    ax_phase = None

    # Get the current axes if they already exist
    for ax in fig.axes:
        if ax.get_label() == 'control-bode-magnitude':
            ax_mag = ax
        elif ax.get_label() == 'control-bode-phase':
            ax_phase = ax

    if ax_mag is None or ax_phase is None:
        plt.clf()
        ax_mag = plt.subplot(211, label='control-bode-magnitude')
        ax_phase = plt.subplot(212, label='control-bode-phase',
                               sharex=ax_mag)

    # Magnitude plot
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

    #plt.show()
