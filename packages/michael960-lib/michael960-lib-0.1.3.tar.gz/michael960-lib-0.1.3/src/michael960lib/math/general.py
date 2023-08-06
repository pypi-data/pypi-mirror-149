import numpy as np
from scipy import fftpack
from pprint import pprint
import numbers
import math


def volume(region):
    if (not 'style' in region) or region == 'null':
        return -1
    if region['style'] == 'box':
        return region['X'] * region['Y'] * region['Z']
    if region['style'] == 'sphere':
        return np.pi * 4/3 * region['R']**3
    return -1

#kronecker
def dlt(a, b):
    return np.where(a==b, 1, 0)


#solves Fl(xl)=0. Fl: Nx1 valued, Jlk: NxN valued, x0: Nx1 valued
def solve(Fl, Jlk, xl0, it=10, check=True, name='', policy=''):
    x = xl0
    for i in range(it): 
        print('-----------------')
        print(f'iter {i+1}')
        print('-----------------')
        if check:
            F = np.array(Fl(x))
            print(f'======val{i}======')
            pprint(F)
            print('===============')
        print(f'=========={name}{i+1}=============')
        x -= np.matmul(np.linalg.inv(Jlk(x)), Fl(x))
        pprint(x)
        print(f'==========================')
        
    F = np.array(Fl(x))
    print(f'======val{it}======')
    pprint(F)
    print('===============')


def length(e, square=False):
    ee = e[0]**2 + e[1]**2 + e[2]**2
    if square:
        return ee
    else:
        return np.sqrt(ee)


def xlogx(x):
    return np.where(x==0, 0, x * np.log(x))

#a < b
def bump(x, a, b):
    return np.heaviside(x-a, 0.5) * np.heaviside(b-x, 0.5)


#derivative of sinc
def dsinc_dx(x):
    x1 = np.where(np.abs(x) < 1e-9, 1e-9, x)
    return (np.cos(np.pi*x1) - np.sinc(x1)) / x1

def lcm(a, b):
    if a is None or b is None:
        return None
    return abs(a*b) // math.gcd(a, b)


def add_func(F1, F2):
    def F(x):
        return F1(x) + F2(x)
    return F

def mul_func(F1, F2):
    def F(x):
        return F1(x) * F2(x)
    return F

def neg_func(F):
    def G(x):
        return -F(x)
    return G

def scale_func(F, a):
    def G(x):
        return a * F(x)
    return G

def inverse_func(F):
    def G(x):
        return 1 / F(x)
    return G

def compose_func(F1, F2):
    def F(x):
        return F1(F2(x))
    return F

def distance_sequence(seq_1, seq_2):
    return np.sum(np.absolute((seq_1-seq_2)**2))


def n_fold_cos(N, theta):
    r = []
    for i in range(N):
        r.append(np.cos(theta + i/N * np.pi * 2))
    return r
