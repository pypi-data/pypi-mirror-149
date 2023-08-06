import numpy as np
from matplotlib import pyplot as plt
from scipy.fftpack import fft, ifft
import pyfftw
import sys





# Solves the differential eq.
# D2f = a(x) f + b(x)
# in [x1, x2] with x_N samples
# 
# solves by relaxation
# df/dt = D2f - a(x) f - b(x)
class Relaxation:
    def __init__(self, x1, x2, x_N, a, b, use_pyfftw=True):
        self.x = np.linspace(x1, x2, x_N)
        self.x_N = x_N
        self.dx = (self.x[-1]-self.x[0]) / (x_N-1)
        self.dk = np.pi * 2 / (x2 - x1)
        self.k = np.array([n * self.dk for n in range(x_N//2)] + [n * self.dk for n in range(-(x_N-x_N//2), 0)])

        self.a = a(self.x)
        self.b = b(self.x)
        self.f = self.x * 0

        self.verbose = 0
        self.clock = 0
        self.t = 0
        self.cycle = 17

        self.t_rec = []
        self.E_rec = []

        self.plot = True
        self.use_pyfftw=use_pyfftw

    
    def reset(self, f0):
        self.f = f0(self.x)

    def evolve_step(self, dt):
        self.evolve_x(dt/2)
        self.evolve_k(dt)
        self.evolve_x(dt/2)

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
                digits = -np.int(np.log10(dt))
                t_simp = np.round(t, digits)
                if self.verbose == 1:
                    if phase != -1:
                        sys.stdout.write(f'{back_character}\r{extra_info}[Phase {phase[0]}/{phase[1]}] {{:.{digits}f}}/{T}      '.format(t_simp))
                    else:
                        sys.stdout.write(f'{back_character}\r{extra_info} | {{:.{digits}f}}/{T}     '.format(t_simp))
                elif self.verbose == 2:
                        sys.stdout.write(f'{back_character}\r{extra_info} | {{:.{digits}f}}/{T}     '.format(t_simp))


    def evolve_until(self, dt, discrep=1e-5, phase=-1, extra_info=''):
        tmp, dsc = self.discrep()
        m = 0

        number_of_newlines = extra_info.count('\n')
        back_character = ''
        if number_of_newlines > 0:
            back_character = f'\033[{number_of_newlines}A'

        while dsc >= discrep:
            self.evolve_step(dt)
            self.t += dt
            self.clock += 1
            m += 1
            if self.clock % self.cycle == 0:
                tmp, dsc = self.discrep()
                self.t_rec.append(self.t)
                self.E_rec.append(self.energy_functional())
                if self.verbose == 1:
                    if phase != -1:
                        sys.stdout.write(f'{back_character}\r{extra_info}[Phase {phase[0]}/{phase[1]}] discrep:{dsc}        ')
                    else:
                        sys.stdout.write(f'{back_character}\r{extra_info} | discrep:{dsc}        ')
                elif self.verbose == 2:
                    sys.stdout.write(f'{back_character}\r{extra_info}[Phase {phase[0]}/{phase[1]}] discrep:{dsc}        ')
                    #sys.stdout.write(f'{back_character}\r{extra_info} | discrep:{dsc}        ')



    def evolve_with_scheme(self, scheme, extra_info=''):
        p = 0
        p0 = len(scheme)
        for phase in scheme:
            if self.verbose >= 2:
                print(f'phase {p}')
            
            t_rec_before = self.t_rec.copy()
            E_rec_before = self.E_rec.copy()
            self.evolve(phase[0], phase[1], phase=(p, p0-1), extra_info=extra_info)

            if self.verbose >= 2:
                print(self.snapshot())
            p += 1
            if self.plot:
                plt.figure()
                plt.plot(self.x, self.f)
                plt.show()

                plt.figure()
                plt.plot(self.t_rec, self.E_rec, color='red')
                plt.plot(t_rec_before, E_rec_before, color='blue')
                plt.show()

    def evolve_smart(self, dt0, N, tmax=100, discrep=1e-6, dcp_factor=1/6):
        t = 0 
        dsc = 1e8
        dt = dt0

        while t <= tmax and dsc >= discrep:
            self.evolve(dt, dt*N, extra_info=f'dynamic dt={dt}')
            t += dt
            tmp, dsc = self.discrep()
            print(dsc/dt)
            dt = dsc * dcp_factor


    def evolve_intelligent(self, C, discrep=1e-6, showlog=True):
        tmp, dsc = self.discrep()
        k = 1.005
        if showlog:
            print(f'[ode]: target final discrepancy (log): {np.log(discrep)}')
        else:
            print(f'[ode]: target final discrepancy: {discrep}')
        
        if dsc < discrep:
            print('The functional is already minimized within the specified discrepancy.')
            return
        
        N = np.log(dsc / discrep) / np.log(k) # roughly the amount of batches to be run
        n = 0
        dt = 0
        if showlog:
            while n < 10 * N and dsc >= discrep:
                dsc2 = max(dsc / k, discrep)
                dt = dsc2 / C / 1.005
                self.evolve_until(min(dt, 0.01), discrep=dsc2, phase=(n, N), extra_info=f'target_discrep(log)={np.log(dsc2)}, dt={dt}    ')
                tmp, dsc = self.discrep()
                n += 1
        else:
             while n < 10 * N and dsc >= discrep:
                dsc2 = max(dsc / k, discrep)
                dt = dsc2 / C / 1.005
                self.evolve_until(min(dt, 0.01), discrep=dsc2, phase=(n, N), extra_info=f'target_discrep={dsc2}, dt={dt}    ')
                tmp, dsc = self.discrep()
                n += 1



    def evolve_k(self, dt):
        if self.use_pyfftw:
            pass
        else:
            f_k = fft(self.f)
            f_k *= np.exp(-self.k**2 * dt)
            self.f = np.real(ifft(f_k))

    def evolve_x(self, dt):
        self.f *= np.exp(-self.a*dt)
        self.f -= self.b * dt


    # verify solution
    def discrep(self):
        d2psi = np.real(ifft(-self.k**2 * fft(self.f)))
        p0 = 1/2 * d2psi
        p1 = p0 * 2
        p2 = -self.a * self.f - self.b
        p = p1 + p2 

        discrep1 = (max(p)-min(p)) / (max(p0)-min(p0))
        discrep2 = np.sqrt(np.sum(p**2) / np.sum(p0**2))

        return discrep1, discrep2


    def energy_functional(self):
        return self.energy_functional_x() + self.energy_functional_k()

    def energy_functional_x(self):
        return self.dx * np.sum(1/2 * self.a * self.f**2) + self.dx * np.sum(self.b * self.f) 

    def energy_functional_k(self):
        f_k = fft(self.f)
        df = np.real(ifft(1j*self.k*f_k))
        return self.dx * np.sum(1/2 * df**2)

    def snapshot(self):
        d1, d2 = self.discrep()
        return {'energy': self.energy_functional(), 'energy_k': self.energy_functional_k(), 'energy_x': self.energy_functional_x(),
                'discrep1': d1, 'discrep2': d2}

    def plot_f(self):
        plt.plot(self.x, self.f, color='red')
        plt.show()



