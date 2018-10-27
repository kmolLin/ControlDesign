# PID controller

model("Motor controller Design")
Kp = 15.27
Ki = 35.19
Kd = 0.11
gsnum = [1]

gsden = [1, 1, 2]
gblock = block(gsnum, gsden)

num = [Kd, Kp, Ki]
den = [1, 0]

c = block(num, den).cloop()
d = gblock*c

answer(d)