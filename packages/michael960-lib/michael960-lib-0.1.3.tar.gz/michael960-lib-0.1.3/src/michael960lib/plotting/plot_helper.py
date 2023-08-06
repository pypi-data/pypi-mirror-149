import numpy as np
from scipy import optimize

def first_peak(S):
    m = -1
    ind = 0
    for i in range(len(S)):
        if S[i] > m:
            ind = i
            m = S[i]
    return ind


def val_to_ind(x, x0):
    for i in range(len(x)-1):
        if x[i] <= x0 <= x[i+1]:
            return i


def second_der(x, v, i, rng):
    v1 = v[i-rng:i+rng]
    x1 = x[i-rng:i+rng]
    x0 = x[i]
    p, q = optimize.curve_fit(test_pol, x1, v1, p0=[0, 0, 0, 0, 0, 0, 0])
    (a, b, c, d, e, f, g) = p
    

    return 2*c + 6*d*x0 + 12*e*x0**2 + 20*f*x0**3 + 30*g*x0**4


def first_der(x, v, i, rng):
    v1 = v[i-rng:i+rng]
    x1 = x[i-rng:i+rng]
    x0 = x[i]
    p, q = optimize.curve_fit(test_pol, x1, v1, p0=[0, 0, 0, 0, 0, 0, 0])
    (a, b, c, d, e, f, g) = p

    return b + 2*c*x0 + 3*d*x0**2 + 4*e*x0**3 + 5*f*x0**4 + 6*g*x0**5


def test_pol(x, a, b, c, d, e, f, g):
    return a + b*x + c*x**2 + d*x**3 + e*x**4 + f*x**5 + g*x**6



