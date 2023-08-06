import numpy as np
from matplotlib import pyplot as plt
from scipy.fftpack import fft, ifft
import sys
import ..math as mt
import pyfftw

class DoubleWellSimulation:
    def __init__(self, D, pot, c, N, Lim, cycle=1, plot=True, use_pyfftw=False, verbose=2, use_cpp=False):
        self.D = D
        self.pot = pot
        self.c = c
        self.N = N
        self.Lim = Lim
        self.x = np.linspace(-Lim, Lim, N)
        self.dx = (self.x[-1]-self.x[0])/(N-1)
        self.dk = np.pi * 2 / (2*Lim)
        self.k = np.array([n * self.dk for n in range(N//2)] + [n * self.dk for n in range(-(N-N//2), 0)])

        self.fields = []
        self.fields_k = []
        self.fft_hamsters = []
        self.ifft_hamsters = []
        for i in range(D):
            lam = pyfftw.empty_aligned(self.N, dtype='complex128')
            lamk = pyfftw.empty_aligned(self.N, dtype='complex128')
            lamp = pyfftw.empty_aligned(self.N, dtype='complex128')
            self.fft_hamsters.append(pyfftw.FFTW(lam, lamk))
            self.ifft_hamsters.append(pyfftw.FFTW(lamk, lamp, direction='FFTW_BACKWARD'))

            self.fields.append(lam)
            self.fields_k.append(lamk)
            b = 1
            self.fields[i][:] = -np.tanh(b*(self.x-Lim/2)) + np.tanh(b*(self.x+Lim/2)) - 1
        
        
        self.t_rec = []
        self.E_rec = []
        self.clock = 0
        self.cycle = cycle
        self.t = 0

        self.plot = plot
        self.use_pyfftw = use_pyfftw
        self.verbose = verbose
        self.use_cpp = use_cpp


    def reset(self, keep_profiles=False):
        self.t_rec = []
        self.E_rec = []
        self.t = 0
        self.clock = 0
        if not keep_profiles:
            for i in range(self.D):
                b = 1
                if self.c[i] == 0:
                    b = np.inf
                else:
                    b = np.sqrt(3*self.pot.tau([i])/2) / np.abs(self.c[i])
                self.fields[i][:] = -np.tanh(b*(self.x-self.Lim/2)) + np.tanh(b*(self.x+self.Lim/2)) - 1

        if self.plot:
            plt.figure()
            for i in range(self.D):
                plt.plot(self.x, self.fields[i])
            plt.show()
            
    def energy_functional(self):
        return self.potential_functional() + self.kinetic_functional()
    
    def potential_functional(self):
        return np.real(np.sum(self.dx * self.pot.U(self.fields)))

    def kinetic_functional(self):
        return np.sum(self.dx * self.kinetic_function())

    def energy_function(self):
        return self.kinetic_function() + self.potential_function()

    def potential_function(self):
        return np.real(self.pot.U(self.fields))

    def kinetic_function(self):
        K = 0
        if self.use_pyfftw:
            for i in range(self.D):
                kLam_k = self.fft_hamsters[i]()
                kLam_k *= 1j * self.k
                dLam = self.ifft_hamsters[i]()
                K += self.c[i]**2 * dLam**2 / 2
        else:
            for i in range(self.D):
                kLam_k = fft(self.fields[i]) * 1j * self.k
                dLam = -ifft(kLam_k)
                K += self.c[i]**2 * dLam**2 / 2
        return np.real(K)

    def evolve_pot(self, dt):
        dField = []
        for i in range(self.D):
            dField.append(-self.pot.U_gradient(self.fields, i) * dt)
        
        for i in range(self.D):
            self.fields[i] += dField[i]

    def evolve_kin(self, dt):
        if self.use_pyfftw:
            for i in range(self.D):
                c = self.c[i]
                lam_k = self.fft_hamsters[i]()
                lam_k *= np.exp(-c**2 * self.k**2 * dt)
                self.fields[i][:] = np.real(self.ifft_hamsters[i]())
        else:                
            for i in range(self.D):
                lam = self.fields[i]
                c = self.c[i]
                lam_k = fft(lam)
                lam_k *= np.exp(-c**2 * self.k**2 * dt)
                self.fields[i] = np.real(ifft(lam_k))

    def evolve_step(self, dt):
        self.evolve_pot(dt/2)
        self.evolve_kin(dt)
        self.evolve_pot(dt/2)

    def evolve(self, dt, T, phase=-1, extra_info=''):
        t = 0
        number_of_newlines = extra_info.count('\n')
        back_character = ''
        if number_of_newlines > 0:
            back_character = f'\033[{number_of_newlines}A'

        while t < T:
            self.evolve_step(dt)
            t += dt
            self.t += dt
            self.clock += 1
            if self.clock % self.cycle == 0:
                self.t_rec.append(self.t)
                self.E_rec.append(self.energy_functional())
                f = -np.int(np.log10(dt))
                t_simp = np.round(t, f)
                if self.verbose == 1:
                    if phase != -1:
                        sys.stdout.write(f'{back_character}\r{extra_info}[Phase {phase[0]}/{phase[1]}] {{:.{f}f}}/{T}      '.format(t_simp))
                    else:
                        sys.stdout.write(f'{back_character}\r{extra_info} | {{:.{f}f}}/{T}          '.format(t_simp))
                elif self.verbose == 2:
                        sys.stdout.write(f'{back_character}\r{extra_info} | {{:.{f}f}}/{T}          '.format(t_simp))
        if self.verbose >= 2:
            pass

    def evolve_with_scheme(self, scheme, extra_info=''):
        p = 0
        p0 = len(scheme)
        for phase in scheme:
            if self.verbose >= 2:
                print(f'phase {p}')

            self.evolve(phase[0], phase[1], phase=(p, p0-1), extra_info=extra_info)
            if self.verbose >= 2:
                print(self.snapshot())
            p += 1
            if self.plot:
                plt.figure()
                self.realize()
                for i in range(self.D):
                    plt.plot(self.x, self.fields[i])
                plt.show()
                plt.figure()
                plt.plot(self.t_rec, self.E_rec)
                plt.show()

    def evolve_smart(self, dt0, N, tmax=100, discrep=1e-6, dcp_factor=1/6, extra_info=''):
        t = 0 
        dsc = 1e8
        dt = dt0

        while t <= tmax and dsc >= discrep:
            self.evolve(dt, dt*N, extra_info=f'{extra_info}[dynamic] dscrep={dsc}|    dt={dt}|    t={t}')
            t += dt
            dsc = self.discrep_total()
            dt = dsc * dcp_factor


    def discrep(self):
        d = mt.distance_sequence(self.potential_functional(), self.kinetic_functional()) * self.dx
        E2 = mt.distance_sequence(self.energy_function(), 0) * self.dx
        return d/E2


    def discrep_prof(self):
        eleq = []
        eleq1 = []
        discrep1 = []
        discrep2 = []
        for i in range(self.D):
            d2psi = np.real(ifft(-self.k**2 * fft(self.fields[i])))
            p0 = 1/2 * d2psi
            p1 = -self.c[i]**2 * d2psi 
            p2 = self.pot.U_gradient(self.fields, i) 
            p = p1 + p2 

            discrep1.append((max(p)-min(p)) / (max(p0)-min(p0)))
            discrep2.append(np.sqrt(np.sum(p**2) / np.sum(p0**2)))

        return discrep1, discrep2

    def discrep_total(self):
        p_sq = 0
        p1_sq = 0
        for i in range(self.D):
            d2psi = np.real(ifft(-self.k**2 * fft(self.fields[i])))
            p0 = 1/2 * d2psi
            p1 = -self.c[i]**2 * d2psi 
            p2 = self.pot.U_gradient(self.fields, i) 
            p = p1 + p2 

            p_sq += np.sum(p**2)
            p1_sq += np.sum(p1**2)
        
        return np.sqrt(p_sq / p1_sq)

        

    def set_coeffs(self, c):
        self.c = c

    def snapshot(self):
        d1, d2 = self.discrep_prof()
        return {'energy': self.energy_functional(), 'energy_kin': self.kinetic_functional(), 'energy_pot': self.potential_functional(),
                'discrep': self.discrep(), 'discrep_prof1': d1, 'discrep_prof2': d2}

    def single_mode_theoretical(self, Deff, C0=1, theta=None):
        if theta is None:
            theta = np.linspace(0, np.pi*2, 1000)
        c = [C0 * np.abs(np.cos(theta + 2*np.pi*i/Deff)) for i in range(self.D)]
        ct = [c[i]/np.sqrt(self.pot.tau([i])) for i in range(self.D)]
        tau = self.pot.tau
        if self.D == 2:
            return theta, np.sqrt(2/3) * (2*tau([0])*ct[0] + 2*tau([1])*ct[1] + tau([0, 1])*np.sqrt(ct[0]*ct[1]))

        if self.D == 3:
            return theta, np.sqrt(2/3) * (2*tau([0])*ct[0] + 2*tau([1])*ct[1] + 2*tau([2])*ct[2]\
            +tau([0, 1])*np.sqrt(ct[0]*ct[1]) + tau([0, 2])*np.sqrt(ct[0]*ct[2]) + tau([1, 2])*np.sqrt(ct[1]*ct[2])\
            +tau([0, 1, 2])*(ct[0]*ct[1]*ct[2])**(1/3)
            )

        return None

    def realize(self):
        for i in range(self.D):
            self.fields[i] = np.real(self.fields[i])

