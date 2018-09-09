# test GA 

from fitnessfunc import Fitne
from rga import Genetic
from dialogBlock import DialogBlock
from scipy.signal import step
import matplotlib
import matplotlib.pyplot as plt

block = DialogBlock([1], [1, 1, 2], )
upper = [100, 100, 100]
lower = [0.000001, 0.0000000001, 0.00000000001]

def test_algorithm_rga():
    """Real-coded genetic algorithm."""
    fun1 = Genetic(Fitne(block, 0.8, upper, lower), {
        'maxGen': 500, 'report': 10,
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
    print(b)
    pidblock = (block * DialogBlock([ a[2], a[0], a[1]], [1, 0])).cloop()
    T, yout = step((pidblock.num, pidblock.den))
    #print(T, yout)
    fig, ax = plt.subplots()
    ax.plot(T, yout)
    plt.show()
    
