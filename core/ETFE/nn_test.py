import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
import matplotlib.pyplot as plt
from etfe import ETFE, sys_frq_rep
from bodeplot_module import bode_plot
from numpy import inf

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
    # TODO : N = 8 * 1024 ???
    n = 1024. * 16
    # t_freq_h: units (Hz)
    # t_mag: units (DB)
    # t_phase: units (Deg)
    tfreq, tfreq_h, tmag_sys, tphase, imag_value, real_value = \
        ETFE(input, 0.0005, n, output)
    mag, pha = sys_frq_rep(0.01, real_value, imag_value, tfreq,
                           tmag_sys, tphase)
    mag[mag == -inf] = 0
    x_train = np.array(tfreq_h)
    y_train = np.array(mag)

    x_test = np.array(tfreq_h)
    y_test = np.array(mag)

    model = Sequential()
    model.add(Dense(units=100, input_dim=1, kernel_initializer='normal'))
    model.add(Activation('relu'))
    model.add(Dense(units=45))
    model.add(Activation('relu'))
    model.add(Dense(units=1))

    model.compile(loss='mean_squared_error',
                  optimizer='adam')

    model.fit(x_train, y_train, epochs=100, batch_size=50, verbose=1)

    loss_and_metrics = model.evaluate(x_test, y_test, batch_size=100)

    classes = model.predict(x_test, batch_size=1)

    test = x_test.reshape(-1)
    tmp_container = [mag, classes]
    plt.plot(test, classes, c='r')
    plt.plot(test, y_test, c='b')
    bode_plot(test, tmp_container, pha, True)
    plt.show()
