import numpy as np
from .analytic_function import AnalyticFunction, zero, power



#get a test polynomial of degree N
def get_test_polynomial(N):
    def f(x, *a):
        S = 0
        for i in range(N+1):
            S += x**i * a[i]
        return S

    return f


def to_analytic(*a):
    res = zero
    for i in range(len(a)):
        res = res + power(i) * a[i]
    return res


def poly_deriv(*a):
    res = []
    for i in range(len(a)-1):
        res.append((i+1)*a[i+1])
    return res
