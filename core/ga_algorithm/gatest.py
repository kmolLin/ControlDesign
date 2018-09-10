# test GA 

from fitnessfunc import Fitne
from rga import Genetic
from dialogBlock import DialogBlock
from scipy.signal import step
import matplotlib
import matplotlib.pyplot as plt

block = DialogBlock([1], [1, 1, 2], )
upper = [100, 100, 100]
lower = [0.0, 0.0, 0.0]

def test_algorithm_rga():
    """Real-coded genetic algorithm."""
    fun1 = Genetic(Fitne(block, 0.8, upper, lower), {
        'maxGen': 100, 'report': 10,
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
    a, b = test_algorithm_rga()
    print(a)
    #print(b)
    #a[2], a[0], a[1] [15.27945163 35.1988434   0.11054415]
    #a = [ 0.27535107 ,41.54292406, 71.99587281]
    #a = [0.00000000e+00 ,6.14027430e+01 ,9.91786806e-03]
    pidblock = (block * DialogBlock([ a[0], a[1], a[2]], [1, 0])).cloop()
    T, yout = step((pidblock.num, pidblock.den))
    #print(T, yout)
    fig, ax = plt.subplots()
    ax.plot(T, yout)
    plt.show()
    
