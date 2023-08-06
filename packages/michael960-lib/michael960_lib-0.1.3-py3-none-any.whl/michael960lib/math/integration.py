import sys
import numpy as np
from ..common import bcolors as bc
from numpy.polynomial.legendre import leggauss as lg


#integrate f within (0, 0, 0) (Lx, Ly, Lz)
def integrate_with_leggauss(f, deg, Lx, Ly, Lz, note=''):
    print(f'integrating {note}')
    q, w = lg(deg)
    s = 0
    
    for i in range(len(q)):
        for j in range(len(q)):
            for k in range(len(q)):
                s += f(Lx/2*(q[i]+1), Ly/2*(q[j]+1), Lz/2*(q[k]+1)) * w[i] * w[j] * w[k]
                
                
    return (Lx/2)*(Ly/2)*(Lz/2)*s


def get_leggauss_samples(f, deg, Lx, Ly, Lz):
    q, w = lg(deg)
    sam = []
    wei = []
    factor = Lx * Ly * Lz / 8
    N = len(w) ** 3
    n1 = 0
    for i in range(len(q)):
        for j in range(len(q)):
            for k in range(len(q)):
                sam.append(f(Lx/2*(q[i]+1), Ly/2*(q[j]+1), Lz/2*(q[k]+1)))
                wei.append(w[i]*w[j]*w[k])
                n1 += 1
                if n1 % 31 == 0 or n1 % 23 ==0 or n1 == N:
                    print(f'\r{n1}/{N}')
                    sys.stdout.flush()
    print()
    return np.array(sam), np.array(wei) * factor


class ParametrizedLegendreIntegrator:
    def __init__(self, deg, x_range, y_range, z_range, param_count, name, tolerance=1e-12):
        self.deg = deg
        self.x1, self.x2 = x_range[0], x_range[1]  
        self.y1, self.y2 = y_range[0], y_range[1]
        self.z1, self.z2 = z_range[0], z_range[1]
        self.Lx = self.x2 - self.x1
        self.Ly = self.y2 - self.y1
        self.Lz = self.z2 - self.z1
        self.name = name
        q, w = lg(deg)
        sites = []
        weights = []
        self.samsize = deg**3
        tmpN = 0
        self.verbose = True
        
        for i in range(deg):
            for j in range(deg):
                for k in range(deg):
                    weights.append(w[i]*w[j]*w[k])
                    s = ((1+q[i])/2 * self.x2 + (1-q[i])/2 * self.x1, (1+q[j])/2 * self.y2 + (1-q[j])/2 * self.y1, (1+q[k])/2 * self.z2 + (1-q[k])/2 * self.z1)
                    sites.append(s)
                    tmpN += 1
                    if tmpN % 31 ==0 or tmpN % 23 == 0 or tmpN == self.samsize:
                        self.notify(f'\rIntegrator {self.name}: initializing sampling sites and weights [{tmpN}/{self.samsize}]', True)
        print()

        self.weights = np.array(weights) * (self.Lx/2) * (self.Ly/2) * (self.Lz/2)
        self.sites = np.array(sites)
        self.samples = dict()
        self.param_count = param_count
        
        #self.cache_size = cache_size
        #self.mu_cache = collections.deque([], self.cache_size)
        self.mu = np.array([0 for i in range(self.param_count)])
        self.tolerance = tolerance
        

    #func(x, y, z, mu) or func(x, y, z)
    def register_function(self, func, name, parametrized=False):
        if name in self.samples:
            self.notify(f'{bc.WARNING}Integrator {self.name}: function {name} already exists. aborted{bc.ENDC}')
            return
        M = dict()
        if parametrized:
            M['parametrized'] = True
            M['func'] = func
            M['samples'] = self.take_samples(lambda x, y, z: func(x, y, z, self.mu), name)

        else:
            M['parametrized'] = False
            M['func'] = func
            M['samples'] = self.take_samples(func, name)

        
        self.samples[name] = M
    
    def purge(self, name):
        if not name in self.samples:
            self.notify(f'Integrator {self.name}: could not find {name}.')
        else:
            del self.samples[name]
            self.notify(f'Integrator {self.name}: deleted {name}.')

    def set_param(self, mu):
        if len(mu) != self.param_count:
            self.notify(f'{bc.WARNING}Integrator {self.name}: Invalid number of parameters. aborted{bc.ENDC}')
            return
        mu = np.array(mu)
        if max(np.abs(mu - self.mu)) > self.tolerance:
            self.notify(f'Integrator {self.name}: setting new params, resampling functions')
            self.mu = np.copy(mu)
            for name in self.samples:
                M = self.samples[name]
                #renew samples
                if M['parametrized']:
                    M['samples'] = self.take_samples(lambda x, y, z: M['func'](x, y, z, self.mu), name)

        else:
            self.notify(f'Integrator {self.name}: new parameters within tolerance')

    def take_samples(self, func, name, verbose=True):
        sam = []
        count = 0
        #self.notify(f'Integrator {self.name}: sampling function {name}')
        '''
        for s in self.sites:
            sam.append(func(s[0], s[1], s[2]))
            count += 1
            if verbose:
                if count % 31 == 0 or count % 23 == 0 or count == self.samsize:
                    self.notify(f'\rIntegrator {self.name}: sampling function {name} [{count}/{self.samsize}]', True)
        self.notify()
        '''
        sam = func(self.sites[:, 0], self.sites[:, 1], self.sites[:, 2])
        self.notify(f'Integrator {self.name}: sampled {name}.')
        #the last index, i.e. the "dotting" index, always corresponds to sites
        return np.array(sam)

    def integrate(self, name):
        if not name in self.samples:
            self.notify(f'{bc.WARNING}Integrator {self.name}: {name} not found. aborted.{bc.ENDC}')
            return
        return np.dot(self.samples[name]['samples'], self.weights)


    #F should be a scalar function with numpy array-compatible arithmetic expressions
    #integrates F(f1, f2, f3, ...) where fi correspond to *names
    #e.g. integrate_expr(lambda A, B, C: A*B+C, 'func1', 'func2', 'func3) integrates func1 * func2 + func3
    #these functions has no ndarray support. should fix.
    def integrate_expr(self, F, *names):
        for nom in names:
            if not nom in self.samples:
                self.notify(f'{bc.WARNING}Integrator {self.name}: {nom} not found. aborted.{bc.ENDC}')
                return
        funcs = [self.samples[nom]['samples'] for nom in names]
        sams = F(*funcs)
        return np.dot(sams, self.weights)


    #returns a function of {mu_i} integrated over x, y, z
    def interface_function(self, name):
        if not name in self.samples:
            self.notify(f'{bc.WARNING}Integrator {self.name}: {name} not found. aborted.{bc.ENDC}')
            return
        if not self.samples[name]['parametrized']:
            self.notify(f'{bc.WARNING}Integrator {self.name}: {name} is not parametrized. aborted. {bc.ENDC}')
            
        def f(mu2):
            self.set_param(mu2)
            I = self.integrate(name)
            return I
        return f

    
    def interface_function_expr(self, F, *names):
        for nom in names:
            if not nom in self.samples:
                self.notify(f'{bc.WARNING}Integrator {self.name}: {nom} not found. aborted.{bc.ENDC}')
                return
        
        try:
            k = F(*[0 for i in range(len(names))])
        except TypeError:
            self.notify(f'{bc.WARNING}Integrator {self.name}: receiving wrong amount of arguments. aborted.{bc.ENDC}')
        except ZeroDivisionError:
            pass
    
        def f(mu2):
            self.set_param(mu2)
            I = self.integrate_expr(F, *names)
            return I
        return f

    
    def set_verbose(self, verb):
        self.verbose = verb

    
    def notify(self, s, hard=False):
        if self.verbose:
            if hard:
                sys.stdout.write(s)
            else:
                print(s)

        
