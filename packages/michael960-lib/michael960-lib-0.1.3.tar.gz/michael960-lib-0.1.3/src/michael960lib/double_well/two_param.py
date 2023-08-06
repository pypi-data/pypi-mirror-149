import numpy as np
from ..math import hyperbolic_tangent as ht


class Potential:
    def __init__(self, name, U, U_lam, U_mu, tau, tau_p):
        self.name = name
        #self.U = U
        self.U0 = U
        self.U_lam = U_lam
        self.U_mu = U_mu
        self.tau_l = tau
        self.tau_p = tau_p

    def U(self, lammu):
        return self.U0(*lammu)

    def U_gradient(self, lammu, i):
        if i == 0:
            return self.U_lam(*lammu)
        if i == 1:
            return self.U_mu(*lammu)

    def get_dimension(self):
        return 2

    def tau(self, indices=[0]):
        if len(indices) != len(set(indices)):
            print('index error')
            return
        if len(indices) == 1:
            return self.tau_l
        if len(indices) == 2:
            return 2*self.tau_p
        


toy = Potential('toy', 
lambda lam, mu: (lam+mu)**4 - 32*lam*mu + 16,
lambda lam, mu: 4*(lam+mu)**3 - 32*mu,
lambda lam, mu: 4*(lam+mu)**3 - 32*lam,
-ht.T(4, 4) - 4*ht.T(4, 3) -3*ht.T(4, 2) + 16*ht.T(2, 1),
-ht.T(4, 4) - 4*ht.T(4, 3) -3*ht.T(4, 2) + 16*ht.T(2, 1) + 8*ht.t[4] - 16*ht.t[2]
)

indep = Potential('indep',
lambda lam, mu: (lam-1)**2 * (lam+1)**2 + (mu-1)**2 * (mu+1)**2,
lambda lam, mu: 4*lam*(lam**2-1),
lambda lam, mu: 4*mu*(mu**2-1),
-ht.T(4, 4) + 2*ht.T(2, 2),
0)

toy_2 = Potential('toy_2',
lambda lam, mu: (lam+mu-2)**2*(lam+mu+2)**2 + 16*(lam-mu)**2,
lambda lam, mu: 4*(lam+mu)**3 + 16*lam - 48*mu,
lambda lam, mu: 4*(lam+mu)**3 + 16*mu - 48*lam,
-ht.T(4, 4) - 4*ht.T(4, 3) - 3*ht.T(4, 2) - 8*ht.T(2, 2) + 24*ht.T(2, 1),
-ht.T(4, 4) - 4*ht.T(4, 3) - 3*ht.T(4, 2) - 8*ht.T(2, 2) + 24*ht.T(2, 1) + 8*ht.t[4] - 16*ht.t[2]
)

geo = Potential('geo',
lambda lam, mu: (lam**4+mu**4) - 2*(2*lam*mu) + 2,
lambda lam, mu: 4*(lam**3-mu),
lambda lam, mu: 4*(mu**3-lam),
-ht.T(4, 4) + 2*ht.T(2, 1),
-ht.T(4, 4) + 2*ht.T(2, 1) + ht.t[4] - 2*ht.t[2]
)

geo_2 = Potential('geo_2',
lambda lam, mu: (lam**4+mu**4)+2*(2*lam**2 *mu**2) - 6*(2*lam*mu) + 6,
lambda lam, mu: 4*lam**3 + 8*lam*mu**2 - 12*mu,
lambda lam, mu: 4*mu**3 + 8*lam**2*mu - 12*lam,
-ht.T(4, 4)-2*ht.T(4, 2)+6*ht.T(2, 1),
-ht.S(4, 4)-2*ht.S(4, 2)+6*ht.S(2, 1))



class Potential_Asymmetric:
    def __init__(self, name, U, U_lam, U_mu, tau_lam, tau_mu, tau_p):
        self.name = name
        self.U = U
        self.U_lam = U_lam
        self.U_mu = U_mu
        self.tau_lam = tau_lam
        self.tau_mu = tau_mu
        self.tau_p = tau_p


toy_asym = Potential_Asymmetric('toy_asym',
lambda lam, mu: (lam**4 + mu**4) + 2*(2*lam**2*mu**2) - 6*(2*lam*mu) + 6 + (lam**2-1)**2 + 2*(mu**2-1)**2,
lambda lam, mu: 4*lam**3 + 8*lam*mu**2 - 12*mu + 4*lam*(lam**2-1),
lambda lam, mu: 4*mu**3 + 8*lam**2 * mu - 12 * lam + 8*mu*(mu**2-1),
-ht.t[4]-4*ht.t[2]+12*ht.t[1]-ht.t[4]+2*ht.t[2],
-ht.t[4]-4*ht.t[2]+12*ht.t[1]-2*ht.t[4]+4*ht.t[2],
-1/2 * (ht.S(4, 4) + ht.S(4, 0) + 4*ht.S(4, 2) - 12*ht.S(2, 1) +\
     ht.S(4, 4) -2*ht.S(2, 2) + 2*ht.S(4, 0)-4*ht.S(2, 0))
)
