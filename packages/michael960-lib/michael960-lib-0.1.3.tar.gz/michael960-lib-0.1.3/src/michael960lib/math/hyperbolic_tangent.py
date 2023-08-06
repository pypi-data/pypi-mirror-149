import numpy as np

t = {
    0: 0,
    1: np.log(4),
    2: 2,
    3: 1 + np.log(4),
    4: 8/3,
    5: 3/2 + np.log(4),
    6: 46/15,
    7: 11/6 + np.log(4),
    8: 352/105,
    9: 25/12 + np.log(4),
    10: 1126 / 315,
    11: 137/60 + np.log(4),
    12: 13016/3465
}

def T(n, k):
    return t[n-k] + t[k]

def S(n, k):
    return T(n, k) - t[n]
