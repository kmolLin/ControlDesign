# test S method
model("test model")
num = [50]
den = [1, 20, 20, 0]
c = block(num, den).cloop()
answer(c)