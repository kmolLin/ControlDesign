# -*- coding: utf-8 -*-

import numpy as np
import scipy.signal as sg


def notch_filter(mag, pha, freqency, num, den):

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
    freqency_t = freqency / (2 * np.pi)

    ori_w, ori_h = sg.freqresp(sg.TransferFunction(num, den), w=freqency)
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

    #           s^2 + fbz*s + fz^2
    # Fnot = --------------------------
    #           s^2 + fbn*s + fn^2
    # 1: fz
    # 2: Dn = fbn / 2 / fz(fn=fz)
    # 3: Dz = D * Dn(fbz=2 * Dz * fz)
    # 4: fn = fbn / 2 / Dn
    filter_tmp = []
    for i in range(1, NotchNum + 1):
        Ndep[i] = 10 ** (Ndep[i] / 20)  # 20log10 inverse
        fz = Ncf[i]  # Center frequency
        fbn = Nbw[i]  # Bandwidth
        fn = fz  # Bandstop natural frequency
        Dn = fbn / 2.0 / fn  # Denumerator damping, fbn = 2 * Dn * fn
        Dz = Ndep[i] * Dn  # Numerator damping, Dz = Ndep * Dn, fbz = 2 * Dz * fz
        fbz = 2 * Dz * fz
        hnot = sg.TransferFunction([1, fbz, fz ** 2], [1, fbn, fn ** 2])
        W, Hnot_fr = sg.freqresp(hnot, w=freqency)
        filter_tmp.append(Hnot_fr)
    # raw model
    Gnot = np.array([])
    for j in range(1, NotchNum):
        if j == 1:
            Gnot = filter_tmp[0]
        else:
            Gnot = Gnot * filter_tmp[j]

    grawNotch = ori_h * Gnot   # Velocity open-loop tansfer function
    grawNotch_mag = 20 * np.log10(np.abs(grawNotch))
    grawNotch_phase = np.angle(grawNotch, deg=True)

    # TODO: Transfer function of first order system model
    for i in range(20001):
        if pha[i] > -120 and pha[i + 1] < -120:
            freq = i + 1
            break

    return grawNotch, grawNotch_mag, grawNotch_phase, freq

