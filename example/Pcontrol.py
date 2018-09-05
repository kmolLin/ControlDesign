# PID controller


Kp = 18
Ki = 3
Kd = 10
gsnum = [1]
gsden = [1, 1, 2+Kp]
gblock = block(gsnum, gsden)

answer(gblock)