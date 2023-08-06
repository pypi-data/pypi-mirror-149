import numpy as np
from matplotlib import pyplot as plt
from .property import Ck
from ..plotting import first_peak

#k = np.linspace(0, 10, 10000)

def fake_Ck_1(k, R, eta):
    A = 7
    B = 2.5
    C = 60
    k = np.where(k < B/R * 1e-7, B/R * 1e-7, k)
    return -C / A**2 * B**2 * np.sin((k*R/B)**2) / (k*R/A)**2


def fake_Ck_2(q, R, eta):
    k = np.where(q<1e-1, 1e-1, q)
    K0 = -(1+2*eta)**2 / (1-eta)**4
    K1 = 6*eta*(1+0.5*eta)**2 * (1/R) /(1-eta)**4
    K3 = -eta*(1+2*eta)**2 * (1/R**3)/2 / (1-eta)**4

    C0 = -K0 * (k*R*np.cos(k*R) - np.sin(k*R)) / k**2
    C1 = K1 * (-R**2 *np.cos(k*R)/k + 2*R*np.sin(k*R)/k**2 + 2*(np.cos(k*R)-1)/k**3)
    C3 = K3 * (-R**4*np.cos(k*R)/k + 4*R**3*np.sin(k*R)/(k**2) + 6*R**2*np.cos(k*R)/(k**3/2) \
        - 4*R*np.sin(k*R)/(k**4/6) + (1-np.cos(k*R))/(k**5/24))
 
    SCALE = 0.25
    return  4 * np.pi / k * (C0) * SCALE


def fake_Ck_3(q, R, eta):
    k = np.where(q<1e-1, 1e-1, q)
    K0 = -(1+2*eta)**2 / (1-eta)**4
    K1 = 6*eta*(1+0.5*eta)**2 * (1/R) /(1-eta)**4
    K3 = -eta*(1+2*eta)**2 * (1/R**3)/2 / (1-eta)**4

    C0 = -K0 * (k*R*np.cos(k*R) - np.sin(k*R)) / k**2
    C1 = K1 * (-R**2 *np.cos(k*R)/k + 2*R*np.sin(k*R)/k**2 + 2*(np.cos(k*R)-1)/k**3)
    C3 = K3 * (-R**4*np.cos(k*R)/k + 4*R**3*np.sin(k*R)/(k**2) + 6*R**2*np.cos(k*R)/(k**3/2) \
        - 4*R*np.sin(k*R)/(k**4/6) + (1-np.cos(k*R))/(k**5/24))
 
    Z1 = 1.05
    Z2 = 1
    Z3 = 3 - Z2 - Z1

    return  4 * np.pi / k * (Z1 * C0 + Z2 * C1 + Z3 * C3)

