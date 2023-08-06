import numpy as np
from scipy import fftpack


def fourier_transform(x, f):
    N = len(x)
    dx = (x[-1] - x[0]) / (N-1)
    dk = 2 * np.pi / (N * dx)
    M = N//2
    k = np.array([n*dk for n in range(0, M)] + [n*dk for n in range(M-N, 0)])
    f_til = fftpack.fft(f)
    return k, f_til


def sine_transform(r, f):
    N = len(r)
    dr = (r[-1] - r[0]) / (N-1)
    dk = np.pi / (N * dr)
    k = np.array([n*dk for n in range(1, N+1)])
    #scipy discrete fourier sine transform
    f_til = fftpack.dst(f)
    return k, f_til


def radial_fourier(r, f):
    k, f_til = sine_transform(r, r*f)
    return k, f_til * np.pi * 4 / k


def radial_fourier_2(r, f):
    r_sym = np.append(-r[::-1], r)
    f_sym = np.append(f[::-1], f)
    N = len(r_sym)
    dr = (r_sym[-1] - r_sym[0]) / (N-1)
    dk = 2*np.pi / (N * dr)
    k = [n * dk for n in range(N)]
    f_til = fftpack.fft(f_sym * r_sym)
    return k, f_til

def get_k(x):
    N = len(x)
    dx = (x[-1] - x[0]) / (N-1)
    dk = 2*np.pi / (N*dx)
    M = N//2
    k = np.array([n*dk for n in range(0, M)] + [n*dk for n in range(M-N, 0)])
    return k


#####
def generate_xk(L, N, center=False, real=False):
    x = np.linspace(0, L, N+1)[:-1]
    dx = L/N
    dk = np.pi*2 / L

    M = N//2
    k = np.array([n*dk for n in range(0, M)] + [n*dk for n in range(M-N, 0)])

    if center:
        x = np.linspace(-L/2, L/2, N+1)[:-1]


    if real:
        k = np.array([n*dk for n in range(M+1)])

    return x, k, dx, dk


def generate_xk_2d(Lx, Ly, Nx, Ny, real=False):
    x = np.linspace(0, Lx, Nx+1)[:-1]
    y = np.linspace(0, Ly, Ny+1)[:-1]
    
    dx = Lx / Nx
    dy = Ly / Ny

    dkx = np.pi*2 / Lx
    dky = np.pi*2 / Ly

    Mx = Nx//2
    My = Ny//2

    kx = np.array([n*dkx for n in range(0, Mx)] + [n*dkx for n in range(Mx-Nx, 0)])
    ky = np.array([n*dky for n in range(0, My)] + [n*dky for n in range(My-Ny, 0)])


    if real:
        ky = np.array([n*dky for n in range(My+1)])

    return x, kx, dx, dkx, y, ky, dy, dky

