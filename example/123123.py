# PID controller


Kp = 18
Ki = 3
Kd = 10
gsnum = [1]

gsden = [1, 1, 2]

gblock = block(gsnum, gsden)
num = [Kd, Kp, Ki]
den = [1, 0]

c = block(num, den).cloop()
d = gblock*c


answer(d)