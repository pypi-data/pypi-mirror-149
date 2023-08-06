from .defin import DoubleWellPotential
import numpy as np
import ..math as mt


#quartic
k = 1
f = 1
def U(a):
    return k * (a-f)**2 * (a+f)**2


def dUda(a):
    return 4 * k * a * (a**2 - f**2)

quartic = DoubleWellPotential('quartic', U, dUda, -f, f, 0)
#/quartic

#sine
sine = DoubleWellPotential('sine', lambda a: 4*np.sin(a) + 4, lambda a: 4*np.cos(a), 3/2 * np.pi, 7/2*np.pi, 5/2 * np.pi)
#/sine

#asymmetric
k1 = 1
f1 = 1
def U2(a):
    return k1 * (np.log(a)-f1)**2 * (np.log(a)+f1)**2

def dU2da(a):
    return 4 * k1 * np.log(a) / a * (np.log(a)-f1) * (np.log(a)+f1)


asymmetric = DoubleWellPotential('log_asym', U2, dU2da, np.exp(-f1), np.exp(f1), 1)
#/asymmetric

#gaussian
def U3(a):
    return np.exp(-1*a**2) + 0.2 * np.exp(1*a**2) - 0.8944

def dU3da(a):
    return -2*a*np.exp(-1*a**2) + 0.2 * 2 * a * np.exp(1*a**2)

gaussian = DoubleWellPotential('gaussian', U3, dU3da, -0.897, 0.897, 0)
#/gaussian

#sharp
def U4(a):
    return (-a+1) * mt.bump(a, 0, 1) + (a+1) * mt.bump(a, -1, 0) + (-a-1) * mt.bump(a, -2, -1) + (a-1) * mt.bump(a, 1, 2)

def dU4da(a):
    return 1 * (mt.bump(a, -1, 0) + mt.bump(a, 1, 2)) - 1 * (mt.bump(a, 0, 1) + mt.bump(a, -2, -1))


sharp = DoubleWellPotential('sharp', U4, dU4da, -1, 1, 0)
#/sharp

#sinc
def U5(a):
    return np.sinc(a) - np.sinc(1.4302)

def dU5da(a):
    return mt.dsinc_dx(a)

sinc = DoubleWellPotential('sinc', U5, dU5da, -1.4302, 1.4302, 0)
#/sinc

#exp
def U6(a):
    return (np.exp(a) - 3)**2 * (np.exp(a) - 1)**2

def dU6da(a):
    return 4 * np.exp(a) * (np.exp(a)-3) * (np.exp(a)-1) * (np.exp(a)-2)

exp = DoubleWellPotential('exp', U6, dU6da, 0, np.log(3), np.log(2))
#/exp

#gauss-cosh

l = 0.771852
def U7(a):
    return np.cosh(a) + np.exp(-a**2) - np.cosh(l) - np.exp(-l**2)

def dU7da(a):
    return np.sinh(a) - 2*a*np.exp(-a**2)

gauss_cosh = DoubleWellPotential('gauss-cosh', U7, dU7da, -l, l, 0)
#/gauss-cosh

#double_exp
def U8(a):
    return (np.exp(np.exp(a))-2)**2 * (np.exp(np.exp(a))-4)**2

def dU8da(a):
    return 4 * np.exp(a)*np.exp(np.exp(a)) * (np.exp(np.exp(a))-3) * (np.exp(np.exp(a))-2) * (np.exp(np.exp(a))-4)

double_exp = DoubleWellPotential('double_exp', U8, dU8da, np.log(np.log(2)), np.log(np.log(4)), np.log(np.log(3)))
#/double_exp

#triple_exp
def U9(a):
    return (np.exp(np.exp(np.exp(a)))-4)**2 * (np.exp(np.exp(np.exp(a)))-6)**2

def dU9da(a):
    return 4 * np.exp(a)*np.exp(np.exp(a))*np.exp(np.exp(np.exp(a))) * (np.exp(np.exp(np.exp(a)))-4) * (np.exp(np.exp(np.exp(a)))-6) * (np.exp(np.exp(np.exp(a)))-5)

triple_exp = DoubleWellPotential('triple_exp', U9, dU9da, np.log(np.log(np.log(4))), np.log(np.log(np.log(6))), np.log(np.log(np.log(5))))
#/triple_exp

#slanted
def U10(a):
    b = -np.sqrt(1-a**2) + 1
    return (b-0.1)**2 * (b-0.95)**2

def dU10da(a):
    b = -np.sqrt(1-a**2) + 1
    return 4 * (b-0.1) * (b-0.95) * (b-0.525) * 2*a / np.sqrt(1-a**2)

slanted = DoubleWellPotential('slanted', U10, dU10da, np.sqrt(1-(0.1-1)**2), np.sqrt(1-(0.95-1)**2), np.sqrt(1-(0.525-1)**2))
#/slanted

#oscillatory
l1 = 12.78791
def U11(a):
    return np.cos(a) * (20-0.4*a**2) - np.cos(l1) * (20-0.4*l1**2)

def dU11da(a):
    return -np.sin(a) * (20-0.4*a**2) -0.8*a * np.cos(a)

oscillatory = DoubleWellPotential('oscillatory', U11, dU11da, -l1, l1, 0)
#/oscillatory


dw_potentials = [
    quartic,
    sine, 
    asymmetric,
    gaussian,
    sharp,
    sinc,
    exp,
    gauss_cosh,
    double_exp,
    triple_exp,
    slanted,
    oscillatory
]
