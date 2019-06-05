# -*- coding: utf-8 -*-

import numpy as np


def notch_filter(mag, pha, freqency):

    #           s^2 + fbz*s + fz^2
    # Fnot = --------------------------
    #           s^2 + fbn*s + fn^2
    # 1: fz
    # 2: Dn = fbn / 2 / fz(fn=fz)
    # 3: Dz = D * Dn(fbz=2 * Dz * fz)
    # 4: fn = fbn / 2 / Dn
    pass
