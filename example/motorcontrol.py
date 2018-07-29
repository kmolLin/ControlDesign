# motor block diogram

Kp = 1
Ki = 0.1
n = [Kp, Ki]
d = [1, 0]
kvi = block(n, d)

num = [0.07]
den = [1, 16.67]
c = block(num, den)
tmp = (kvi*c).cloop()
ss = tmp*Kp*block([1], [1, 0])
an = ss.cloop()
answer(an)