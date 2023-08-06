from ..math import hyperbolic_tangent as ht
import numpy as np
from matplotlib import pyplot as plt


class PotentialGeneral:
    def __init__(self, name, D, coeffs):
        self.name = name
        self.D = D
        self.coeffs = coeffs

    def exp_e(self, F):
        r = 0
        for p in self.coeffs:
            if np.sum(p) % 2 == 0:
                coeff = self.coeffs[p]
                r +=  coeff * F(p)
        return r

    def exp_o(self, F):
        r = 0
        for p in self.coeffs:
            if np.sum(p) % 2 == 1:
                coeff = self.coeffs[p]
                r +=  coeff * F(p)
        return r

    def exp(self, F):
        return self.exp_o(F) + self.exp_e(F)

    def U(self, lam_vec):
        def one_term(p):
            r = 1
            for i in range(self.D):
                r *= lam_vec[i] ** p[i]
            return r
        return self.exp(one_term)

    def U_gradient(self, lam_vec, i):
        def one_term(p):
            r = 1
            for j in range(self.D):
                if j == i:
                    if p[j] == 0:
                        r = 0
                        return r
                    else:
                        r *= p[j] * lam_vec[j] ** (p[j]-1)
                else:
                    rr = lam_vec[j] ** p[j]
                    r *= rr
            return r
        return self.exp(one_term)

    def get_dimension(self):
        return self.D

    def tau(self, indices):
        if len(indices) != len(set(indices)):
            print('index error')
            return

    def energy_prediction(self, theta):
        pass

class Potential2(PotentialGeneral):
    def __init__(self, name, coeffs):
        super().__init__(name, 2, coeffs)

    def tau(self, indices):
        if len(indices) != len(set(indices)):
            print('index error')
            return
        if len(indices) == 1:
            return -self.exp_e(lambda p: ht.t[p[indices[0]]])
        if len(indices) == 2:
            return -self.exp_e(lambda p: ht.t[p[0]+p[1]] - ht.t[p[0]] - ht.t[p[1]])
    
class Potential3(PotentialGeneral):
    def __init__(self, name, coeffs):
        super().__init__(name, 3, coeffs)

    def tau(self, indices):
        if len(indices) != len(set(indices)):
            print('index error')
            return
        if len(indices) == 1:
            i = indices[0]
            return -self.exp_e(lambda p: ht.t[p[i]])
        if len(indices) == 2:
            i = indices[0]
            j = indices[1]
            return -self.exp_e(lambda p: ht.t[p[i]+p[j]] - ht.t[p[i]] - ht.t[p[j]])
        if len(indices) == 3:
            i = indices[0]
            j = indices[1]
            k = indices[2]
            return -self.exp_e(lambda p: ht.t[p[i]+p[j]+p[k]] - ht.t[p[i]+p[j]] - ht.t[p[i]+p[k]] - ht.t[p[j]+p[k]] + ht.t[p[i]] + ht.t[p[j]] + ht.t[p[k]])

    #compat
    @property
    def tau_l(self):
        return self.tau([0])
    
    @property
    def tau_m(self):
        return self.tau([1])
    
    @property
    def tau_n(self):
        return self.tau([2])

    @property
    def tau_lm(self):
        return self.tau([0, 1])
    
    @property
    def tau_ln(self):
        return self.tau([0, 2])

    @property
    def tau_mn(self):
        return self.tau([1, 2])

    @property
    def tau_lmn(self):
        return self.tau([0, 1, 2])


def generate_sg_coeff(theta, D, Deff, C0):
    return [C0*np.abs(np.cos(theta + 2*np.pi*i/Deff)) for i in range(D)]

toy = Potential2('toy', 
{
    (4, 0): 1,
    (3, 1): 4,
    (2, 2): 6,
    (1, 3): 4,
    (0, 4): 1,
    (0, 0): 16,
    (1, 1): -32
})

indep = Potential2('indep',
{
    (4, 0): 1,
    (2, 0): -2,
    (0, 0): 2,
    (0, 4): 1,
    (0, 2): -2
})

toy_2 = Potential2('toy_2',
{
    (4, 0): 1,
    (3, 1): 4,
    (2, 2): 6,
    (1, 3): 4,
    (0, 4): 1,
    (2, 0): 8,
    (0, 2): 8,
    (1, 1): -48,
    (0, 0): 16
})

geo = Potential2('geo',
{
    (4, 0): 1,
    (0, 4): 1,
    (1, 1): -4,
    (0, 0): 2
})

geo_2 = Potential2('geo_2',
{
    (4, 0): 1,
    (0, 4): 1,
    (2, 2): 4,
    (1, 1): -12,
    (0, 0): 6
})


maja = Potential3('maja',
{
        (4, 0, 0): 1/80,
        (0, 4, 0): 1/80,
        (0, 0, 4): 1/80,
        (2, 2, 0): 1/20,
        (2, 0, 2): 1/20,
        (0, 2, 2): 1/20,
        (2, 0, 0): 17/40,
        (0, 2, 0): 17/40,
        (0, 0, 2): 17/40,
        (1, 1, 0): -11/20,
        (1, 0, 1): -11/20,
        (0, 1, 1): -11/20,
        (1, 1, 1): -3/4,
        (2, 1, 0): 1/10,
        (2, 0, 1): 1/10,
        (1, 2, 0): 1/10,
        (0, 2, 1): 1/10,
        (1, 0, 2): 1/10,
        (0, 1, 2): 1/10,
        (3, 0, 0): 1/20,
        (0, 3, 0): 1/20,
        (0, 0, 3): 1/20,
        (0, 0, 0): 3/16
})

triag = Potential3('triag', 
{
        (4, 0, 0): 9,
        (0, 4, 0): 5,
        (0, 0, 4): 3,
        (2, 0, 0): -16,
        (0, 2, 0): -8,
        (0, 0, 2): -4,
        (2, 1, 1): -1,
        (1, 2, 1): -1,
        (1, 1, 2): -1,
        (0, 0, 0): 14
})

geo_triag = Potential3('geo_triag',
{
    (4, 0, 0): 1,
    (0, 4, 0): 1,
    (0, 0, 4): 1,
    (1, 1, 0): -2,
    (1, 0, 1): -2,
    (0, 1, 1): -2,
    (0, 0, 0): 3
}
)
