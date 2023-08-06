import numpy as np
from .structure import sym
from ..math import length

def harmonic(seed, mag, use_cos=False):
    c = sym(seed)
    D = len(c)
    if use_cos:
        def fl(x, y, z):
            s = 0
            for c1 in c:
                L = length(seed)
                cr = np.array([0, 0, 0])
                if L != 0:
                    cr = np.array(c1) * mag / L
                arg = cr[0]*x + cr[1]*y + cr[2]*z
                s += np.cos(cr[0]*x+cr[1]*y+cr[2]*z)
                #s += nexp.evaluate('cos(arg)')
            return s
        return fl
    else:
        def fl(x, y, z):
            s = 0
            for c1 in c:
                L = length(seed)
                cr = np.array([0, 0, 0])
                if L != 0:
                    cr = np.array(c1) * mag / L
                arg = cr[0]*x + cr[1]*y + cr[2]*z
                s += np.exp(1j * (cr[0]*x+cr[1]*y+cr[2]*z))
                #s += nexp.evaluate('exp(1j*arg)')
            if np.any(np.imag(s) >= 1e-8):
                print('nonreal f!')
            return np.real(s)
        return fl


def short_id(seed):
    return f'{seed[0]}-{seed[1]}-{seed[2]}'
