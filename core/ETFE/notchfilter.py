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
    mag_tmp = [0]
    pha_tmp = [0]

    mcCf = []
    mcdB = []
    mcCnt = []

    mtCf = []
    mtdB = []
    mtCnt = []
    mtNum = 0
    McNum = 0

    pcNum = 0
    PcCf = []
    # TODO: need to check the freqency units (* 10)
    freqency_t = freqency * 10 / (2 * np.pi)
    for i in range(1, len(mag)):
        mag_tmp.append(mag[i] - mag[i - 1])
        pha_tmp.append(pha[i] - pha[i - 1])

        if mag_tmp[i - 1] > 0.0 and mag_tmp[i] < 0.0:
            McNum += 1
            mcCf.append(freqency_t[i])
            mcdB.append(mag[i])
            mcCnt.append(i)
        elif mag_tmp[i - 1] < 0.0 and mag_tmp[i] > 0.0:
            mtNum += 1
            mtCf.append(freqency_t[i])
            mtdB.append(mag[i])
            mtCnt.append(i)
        if (pha_tmp[i - 1] > 0.0) and (pha_tmp[i] < 0.0):
            pcNum += 1
            PcCf.append(freqency_t[i])

    tmp_freq = []
    NotchNum = 0
    VibCfreq = [0]
    Ncf = [0]
    Nbw = [0]
    Ndep = [0]
    k = 0
    for i in range(pcNum):
        for j in range(k, McNum):
            CfreqErr = (PcCf[i] - mcCf[j]) / PcCf[i]
            if abs(CfreqErr) <= 0.2:
                if NotchNum > 0 and VibCfreq[NotchNum] == mcCf[j]:
                    break
                NotchNum += 1
                VibCfreq.append(mcCf[j])
                Ncf.append(VibCfreq[NotchNum] * 2 * np.pi)
                Nbw.append((VibCfreq[NotchNum] - mtCf[j]) * 4 * np.pi)
                BwdB = (mcCnt[j] - mtCnt[j]) + mcCnt[j]
                if BwdB > 20001:
                    Ndep.append(mtdB[j] - mcdB[j])
                else:
                    Ndep.append((mag[BwdB] + mtdB[j]) / 2 - mcdB[j])

                if Ndep[NotchNum] + mcdB[j] > 0:
                    Ndep.append(-3 - mcdB[j])
                k = k + 1
    print(Ndep)
    print(Nbw)
    print(Ncf)
