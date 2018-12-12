#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from scipy import signal as sg
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, LSTM, TimeDistributed, SimpleRNN
from keras.optimizers import Adam

h = 3
s = 3
h = 3
h2 = 3

BATCH_START = 0
TIME_STEPS = 1
BATCH_SIZE = 100
INPUT_SIZE = 1
OUTPUT_SIZE = 1
CELL_SIZE = 100
LR = 0.006


def get_batch():
    global BATCH_START, TIME_STEPS
    # xs shape (50batch, 20steps)
    xs = np.arange(BATCH_START, BATCH_START+TIME_STEPS*BATCH_SIZE).reshape((BATCH_SIZE, TIME_STEPS)) / (10*np.pi)
    seq = np.sin(xs)
    res = np.cos(xs)
    BATCH_START += TIME_STEPS
    # plt.plot(xs[0, :], res[0, :], 'r', xs[0, :], seq[0, :], 'b--')
    # plt.show()
    return [seq[:, :, np.newaxis], res[:, :, np.newaxis], xs]


def simple_LM(ui, yi):
    nx = 3
    d = 0.0001
    alpha = 10.0
    k = 0
    STOP = False
    omega = np.random.uniform(-1, 1, (nx, (nx + len(ui) + len(yi) + 1)))
    print(omega.shape)


def nnwork(w, u, t):
    model = Sequential()
    # model.add(Dense(output_dim=1, input_dim=1, use_bias=True))
    model.add(LSTM(
        batch_input_shape=(BATCH_SIZE, TIME_STEPS, INPUT_SIZE),  # Or: input_dim=INPUT_SIZE, input_length=TIME_STEPS,
        output_dim=CELL_SIZE,
        return_sequences=True,
        stateful=True,
        # activation=None,
        use_bias=False
    ))
    # model.add(SimpleRNN(
    #     batch_input_shape=(BATCH_SIZE, TIME_STEPS, INPUT_SIZE),
    #     output_dim=CELL_SIZE,
    #     use_bias=False,
    #     return_sequences=True,
    #     # stateful=True,
    # ))

    model.add(TimeDistributed(Dense(OUTPUT_SIZE)))
    adam = Adam(LR)
    model.compile(loss='mse', optimizer=adam)
    print(model.summary())

    print('Training -----------')
    for step in range(501):
        X_batch, Y_batch, xs = w, u, t
        cost = model.train_on_batch(X_batch, Y_batch)
        # exit()
        pred = model.predict(X_batch, BATCH_SIZE)
        plt.plot(xs[:], Y_batch.flatten(), 'r', xs[:], pred.flatten()[:], 'b--')
        plt.ylim((-1.2, 1.2))
        plt.draw()
        plt.pause(0.1)
        if step % 10 == 0:
            # print('train cost: ', cost)
            pass
        if step == 500:
            print('train cost: ', cost)
            # print(model.layers[0].get_weights())
            return model.predict(X_batch, BATCH_SIZE).flatten()


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
    num = [10]
    den = [1, 10]
    tf = sg.TransferFunction(num, den)
    t, yout = sg.step(tf)
    a = np.ones((len(t), 1))[:, :, np.newaxis]
    # dd, d1, d3d = sg.cont2discrete((num, den), 0.002, method="bilinear")
    # # t = np.linspace(0, 10, 101)
    # t = np.linspace(0, 10, 5001)
    # w = sg.chirp(t, f0=1, f1=6, t1=10, method='linear')
    # t, u = calcc2d(w.tolist(), dd[0], d1, d3d)
    # # print(w.reshape(5001, 1))
    # print(np.array(u).shape)
    # a = w.reshape(5001, 1)[:, :, np.newaxis]
    # b = np.array(u).reshape(5001, 1)[:, :, np.newaxis]
    b = np.array(yout).reshape((len(t), 1))[:, :, np.newaxis]
    xxx = nnwork(a, b, t)
    plt.plot(t, yout, 'b')
    plt.plot(t, xxx, 'g')
    # plt.plot(t, w, 'r')
    plt.show()


