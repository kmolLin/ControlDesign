# test GA
# TODO: this method isn't good because time serial data can't fit

from .Adesign import Verification
from .fitnessfunc import Fitne
from .Adesign import Genetic
import numpy as np

# block = DialogBlock([1], [1, 1, 2], )


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


def test_algorithm_rga(step, a, b, orignal_g, OM, indb, indg, w_f):
    """Real-coded genetic algorithm."""
    distance = 1e-10
    scale = 1
    tmp_a = np.delete(a, 0)
    tmp_array = np.append(tmp_a, b)
    fun1 = Genetic(Fitne(step, tmp_a, b, orignal_g, (tmp_array + distance) * scale,
                         (tmp_array - distance) * scale, OM, indb, indg, w_f), {
        'max_gen': 20,
        'report': 1,
        # 'min_fit': 1,
        # 'max_time': 3,
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

    # TODO: add the new fitnessfunc
    step = 1000
    # test_algorithm_rga(step, a, b, orignal_g)

    print("XD")
