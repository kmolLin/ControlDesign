#coreof etfe
import math

def etfemethod(data, M, N, T):
    index = 1
    if len(input) != len(output):
        return -1
    yd = [0] * n
    Ud = [0] * n
    Ncap = len(input)
    U = input
    Y = output
    if Ncap < n:
        start = n - Ncap - index
        end = n
        for  i in range(start, end, 1):
            U[i] = 0
            Y[i] = 0
    else:
        Ncap = n
    nfft = 2 * math.ceil(Ncap / n) * n
    L = nfft
    M = 150
    M /= 2
    M1 = Fix(L/M)
    sc = L/(2*n)
    if sc != sc:
        return -1
        
    start = L-M1+2-index
    end = L-index
    cnt = 0
    YY = []
    ##YY = [0] * (end-start+1)
    for i in range(start, i < end):
        cnt = cnt + 1
        YY[cnt] = Y[i]
        YY.append(Y)
    
    start = L-M1+2-index
    end = L-index
    cnt = 0
    UU = []
    cnt = 0
    for i in range(start, i < end):
        cnt = cnt + 1
        UU[cnt] = U[i]
    UU.append(U)
    
    Y1 = []
    
    for i in range(0, i < len(YY)):
        Y1[i].real = YY[i].real*UU[i].real + YY[i].imag*UU[i].imag
        Y1[i].imag = YY[i].imag*UU[i].real - YY[i].real*UU[i].imag
        YY.append(Y1[i])
    ##ha_norm = Norm(ha)
    
    
    for i in range(0, i < len(UU)):
        UU[i].real = pow(math.sqrt(pow(UU[i].real, 2)+pow(UU[i].imag, 2)), 2)
        UU[i].imag = 0
    
    if (M1 > 1):
        ha = [0] * (M1+1)
        for i in range(0, i <= M1):
            ha[i] = 0.54-0.46 * math.cos(math.pi*i/M1)

