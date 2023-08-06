import numpy as np

#direct correlation function
def C(r, R, eta):
    c = -((1+2*eta)**2 - 6*eta*(1+0.5*eta)**2 *(r/R) + eta*(1+2*eta)**2 * (r/R)**3 /2)/(1-eta)**4
    c = c * np.heaviside(R-r, 0)
    return c


#direct correlation function derivative w.r.t. r
def dCdr(r, R, eta):
    dcdr = -(-6*eta*(1+0.5*eta)**2 *(1/R) + eta*(1+2*eta)**2 * (3*r**2/R**3) /2)/(1-eta)**4
    return dcdr * np.heaviside(R-r, 0)


#direct correlation function second derivative w.r.t. r
def dCdr2(r, R, eta):
    dcdr2 = -(eta*(1+2*eta)**2 * (6*r/R**3) /2)/(1-eta)**4
    return dcdr2 * np.heaviside(R-r, 0)


#fourier transformed direct correlation function
def Ck(q, R, eta):
    k = np.where(q<1e-1, 1e-1, q)
    K0 = -(1+2*eta)**2 / (1-eta)**4
    K1 = 6*eta*(1+0.5*eta)**2 * (1/R) /(1-eta)**4
    K3 = -eta*(1+2*eta)**2 * (1/R**3)/2 / (1-eta)**4

    C0 = -K0 * (k*R*np.cos(k*R) - np.sin(k*R)) / k**2
    C1 = K1 * (-R**2 *np.cos(k*R)/k + 2*R*np.sin(k*R)/k**2 + 2*(np.cos(k*R)-1)/k**3)
    C3 = K3 * (-R**4*np.cos(k*R)/k + 4*R**3*np.sin(k*R)/(k**2) + 6*R**2*np.cos(k*R)/(k**3/2) \
        - 4*R*np.sin(k*R)/(k**4/6) + (1-np.cos(k*R))/(k**5/24))
 
    return  4 * np.pi / k * (C0 + C1 + C3)


def F(eta):
    return (-8 * eta * (1+2*eta)**2 + 36 * eta**2 * (1+0.5*eta)**2 - 2 * eta**2*(1+2*eta)**2) / (1-eta)**4


#equation of state. p*beta/rho
def EOS(eta):
    return (1 + eta + eta**2 - eta**3) / (1-eta)**3


#conversion for eta (or xi), rho
def convert(X, param1, param2, R):
    eta = X
    if param1 == 'eta':
        eta = X
    elif param1 == 'rho':
        eta = X * R**3 * np.pi / 6
    else:
        raise ValueError(f'{param1} is not a valid hard sphere parameter.')
    
    if param2 == 'eta':
        return eta
    elif param2 == 'rho':
        return 6 / (np.pi * R**3) * eta
    else:
        raise ValueError(f'{param2} is not a valid hard sphere parameter.')