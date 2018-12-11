#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from scipy import signal as sg
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, SimpleRNN

h = 3
s = 3
h = 3
h2 = 3


def simple_LM(ui, yi):
    nx = 3
    d = 0.0001
    alpha = 10.0
    k = 0
    STOP = False
    omega = np.random.uniform(-1, 1, (nx, (nx + len(ui) + len(yi) + 1)))
    print(omega.shape)


def nnwork(w, u):
    model = Sequential()
    # model.add(Dense(output_dim=5, input_dim=1, use_bias=False))
    model.add(SimpleRNN(input_dim=5, output_dim=5, use_bias=False, return_sequences=True))
    # model.add(Dense(output_dim=5, input_dim=1, use_bias=False))
    model.compile(loss='mse', optimizer='sgd')
    print(model.summary())
    return 0
    print('Training -----------')
    for step in range(1000):
        cost = model.train_on_batch(w, u)
        if step % 100 == 0:
            print('train cost: ', cost)

    cost = model.evaluate(w, u, batch_size=40)
    print(model.layers[0].get_weights())
    # print(model.layers[1].get_weights())
    return model.predict(w)
    # print('Weights=', W, '\nbiases=', b)


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


if __name__ == "__main__":
    num = [1, 1]
    den = [1, 3, 1]
    tf = sg.TransferFunction(num, den)
    dd, d1, d3d = sg.cont2discrete((num, den), 0.002, method="bilinear")
    # t = np.linspace(0, 10, 101)
    t = np.linspace(0, 10, 5001)
    w = sg.chirp(t, f0=1, f1=6, t1=10, method='linear')
    t, u = calcc2d(w.tolist(), dd[0], d1, d3d)
    print(len(w))
    print(len(u))
    print(tf.to_ss())
    xxx = nnwork(w, u)
    # simple_LM(w, u)
    # plt.plot(t, u, 'b')
    # plt.plot(t, xxx, 'g')
    # plt.plot(t, w, 'r')
    # plt.show()


