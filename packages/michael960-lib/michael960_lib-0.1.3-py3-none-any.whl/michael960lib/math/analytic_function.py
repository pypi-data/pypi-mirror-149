import numpy as np
import numbers
from .general import lcm, add_func, neg_func, scale_func, mul_func, inverse_func, compose_func
from matplotlib import pyplot as plt

class AnalyticFunction:
    def __init__(self, name, f):
        self.name = name
        self.func = f
        self.der = dict()
        self.der[0] = f
        #eg
        #f(x) = x^2 + 1   order=2, period=None
        #f(x) = sin(x)    order=None, period=4
        #f(x) = cos(x)+x^5 order =5, period=4
        self.period = None
        self.order = None

        self.is_compound = False
        self.component_track = None

        self.has_pointer = False
        self.deriv_pointer = None


    def set_derivative(self, N, der):
        self.der[N] = der

    def set_derivative_pointer(self, other):
        self.has_pointer = True
        self.deriv_pointer = other

    def get_func(self):
        return self.func

    def get_deriv_func(self, N):
        if self.is_compound or self.has_pointer:
            return None
    
        if (self.period is not None) and (self.order is None):
            N = N % self.period
            return self.der[N]

        if (self.period is None) and (self.order is not None):
            if N > self.order:
                return zero.get_func()
            else:
                return self.der[N]
        if (self.period is not None) and (self.order is not None):
            if N > self.order:
                N = self.order + (N-self.order) % self.period
                #print(f'{self.name}: {N}')
                return self.der[N]
            else:
                #print(f'{self.name}: {N}err')
                return self.der[N]
        
        return self.der[N]

    def set_period(self, P):
        self.period = P

    def set_order(self, O):
        self.order = O

    def set_name(self, name):
        self.name = name

    #get Nth derivative
    def deriv(self, N):
        if N == 0:
            return self
        
        if self.has_pointer:
            return self.deriv_pointer.deriv(N-1)

        if self.is_compound:
            return parse_track_deriv(self.component_track).deriv(N-1)


        res = AnalyticFunction(f'D{N}_{self.name}', self.get_deriv_func(N))

        if (self.period is not None) and (self.order is None):
            res.set_period(self.period)
            for n in range(1, res.period+1):
                res.set_derivative(n, self.get_deriv_func(N+n))
            return res
        
        if (self.order is not None) and (self.period is None):
            res.set_order(self.order-1)
            if N > self.order:
                return zero
            if not N in self.der:
                print(f'{self.name}: {N}th derivative is not defined.')

            for n in range(1, res.order+1):
                res.set_derivative(n, self.get_deriv_func(N+n))

            return res

        if (self.order is not None) and (self.period is not None):
            res.set_order(self.order-1)
            
            res.set_period(self.period)
            for n in range(1, res.period + res.order + 1):
                res.set_derivative(n, self.get_deriv_func(N+n))
            #convention
            if self.order == 1:
                res.set_order(None)
            return res
        
        if not N in self.der:
            print(f'{self.name}: {N}th derivative is not defined.')

        for n in self.der:
            if n >= N:
                res.set_derivative(n-N, self.get_deriv_func(n))
        return res

    def __add__(self, other):
        if isinstance(other, numbers.Number):
            res = AnalyticFunction(f'({self.name}+{other})', lambda x: self(x) + other)
            res.set_period(self.period)
            res.set_order(self.order)
            for N in self.der:
                if not N == 0:
                    res.set_derivative(N, self.der[N])
            return res

        elif isinstance(other, AnalyticFunction):
            if self.is_compound or other.is_compound:
                res = AnalyticFunction(f'({self.name}+{other.name})', lambda x: self(x) + other(x))
                res.is_compound = True
                res.component_track = ['add', [self, other]]
                return res


            res = AnalyticFunction(f'({self.name}+{other.name})', lambda x: self(x) + other(x))
            
            period, order = combine(self.period, self.order, other.period, other.order)
            res.set_period(period)
            res.set_order(order)
            max_der = min(max(self.der), max(other.der))
            if (res.period is not None) and (res.order is None):
                max_der = res.period
            if (res.period is None) and (res.order is not None):
                max_der = res.order
            if (res.period is not None) and (res.order is not None):
                max_der = res.period + res.order
        
            for Q in range(1, max_der + 1):
                #print(f'{res.name}: {Q}der')
                F1 = np.vectorize(self.get_deriv_func(Q))
                F2 = np.vectorize(other.get_deriv_func(Q))
                res.set_derivative(Q, add_func(F1, F2))
            return res

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        res = AnalyticFunction(f'-{self.name}', lambda x: -self(x))
        res.set_period(self.period)
        res.set_order(self.order)

        for Q in self.der:
            res.set_derivative(Q, neg_func(self.der[Q]))
        return res

    def __sub__(self, other):
        return self.__add__(-other)

    def __rsub__(self, other):
        return (-self).__add__(other)

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            res = AnalyticFunction(f'{self.name}*{other}', scale_func(self.get_func(), other))
            res.set_period(self.period)
            res.set_order(self.order)
            #res.is_compound = True
            #res.component_track = ['mul', [other, self]]
            
            for N in self.der:
                res.der[N] = scale_func(self.der[N], other)

            return res

        if isinstance(other, AnalyticFunction):
            res = AnalyticFunction(f'{self.name}*{other.name}', mul_func(self.get_func(), other.get_func()))
            res.is_compound = True
            res.component_track = ['mul', [self, other]]
            return res
    def __rmul__(self, other):
        return self.__mul__(other)

    def inverse(self):
        res = AnalyticFunction(f'({self.name})^-1', inverse_func(self.get_func()))
        res.is_compound = True
        res.component_track = ['inv', self]
        return res
    
    def __truediv__(self, other):
        if isinstance(other, numbers.Number):
            return self.__mul__(1/other)

        if isinstance(other, AnalyticFunction):
            return self.__mul__(other.inverse())

    def __rtruediv__(self, other):
        return other * self.inverse()

    
    def o(self, other):
        res = AnalyticFunction(f'({self.name}o{other.name})', compose_func(self.get_func(), other.get_func()))
        res.is_compound = True
        res.component_track = ['o', [self, other]]
        return res

    def __call__(self, x):
        return self.func(x)


def combine(p1, o1, p2, o2):
    if ((p1 is None) and (o1 is None)) or ((p2 is None) and (o2 is None)):
        return None, None

    period = lcm(p1, p2)
    order = None
    if p1 is None:
        period = p2
    if p2 is None:
        period = p1

    if (o1 is not None) and (o2 is not None):
        order = max(o1, o2)

    elif (o1 is not None) and (p2 is not None):
        order = o1
    elif (o2 is not None) and (p1 is not None):
        order = o2
    
    return period, order

def parse_track_deriv(track):  
    if track[0] == 'add':
        res = zero
        l = []
        name = ''
        for f in track[1]:
            g = f.deriv(1)
            res = res + g
            l.append(g)
            name = name + f.name + '+'
        name = name[:len(name)-1]
        res.component_track = ['add', l]
        res.set_name(f'({name})')
        res.is_compound = True
        return res
    if track[0] == 'mul':
        if isinstance(track[1][1], numbers.Number):
            res1 = zero
            name1 = track[1][1]
        else:
            res1 = track[1][0] * track[1][1].deriv(1)
            name1 = track[1][1].name
        if isinstance(track[1][0], numbers.Number):
            res2 = zero
            name2 = track[1][0]
        else:
            res2 = track[1][0].deriv(1) * track[1][1]
            name2 = track[1][0].name

        res = res1 + res2
        res.set_name(f'D[{name1}*{name2}]')
        res.is_compound = True
        res.component_track = ['add', [res1, res2]]
        return res

    if track[0] == 'inv':
        return -1/(track[1]*track[1]) * track[1].deriv(1)

    if track[0] == 'o':
        res1 = track[1][1].deriv(1)
        res2 = track[1][0].deriv(1).o(track[1][1])
        res = res1 * res2
        res.is_compound = True
        res.component_track = ['mul', [res1, res2]]
        res.set_name(f'D[({track[1][0].name})o({track[1][1].name})]')
        return res
        



zero = AnalyticFunction('zero', lambda x: 0*x)
zero.set_order(0)

one = AnalyticFunction('one', lambda x: 1 + 0*x)
one.set_order(0)

sin = AnalyticFunction('sin', np.sin)
sin.set_derivative(1, np.cos)
sin.set_derivative(2, lambda x: -np.sin(x))
sin.set_derivative(3, lambda x: -np.cos(x))
sin.set_derivative(4, np.sin)
sin.set_period(4)

cos = sin.deriv(1)
cos.set_name('cos')

tan = sin / cos

sinh = AnalyticFunction('sinh', np.sinh)
sinh.set_derivative(1, np.cosh)
sinh.set_derivative(2, np.sinh)
sinh.set_period(2)

cosh = sinh.deriv(1)
cosh.set_name('cosh')

tanh = sinh / cosh

ident = AnalyticFunction('x', lambda x: x)
ident.set_derivative(1, lambda x: 1 + 0*x)
ident.set_order(1)


log = AnalyticFunction('log', lambda x: np.log(x))
log.set_derivative_pointer(ident.inverse())


exp = AnalyticFunction('exp', lambda x: np.exp(x))
exp.set_derivative(1, lambda x: np.exp(x))
exp.set_period(1)


square = AnalyticFunction('square', lambda x: x**2)
square.set_derivative(1, lambda x: 2*x)
square.set_derivative(2, lambda x: 2 + 0*x)
square.set_order(2)


sqrt = AnalyticFunction('sqrt', lambda x: np.sqrt(x))
sqrt.set_derivative_pointer(0.5 / sqrt)

def _power(N):
    return lambda x: x**N

#x^N
def power(N):
    if N == 0:
        return one
    if N == 1:
        return ident
    if N == 2:
        return square
    xN = AnalyticFunction('x^N', lambda x: x**N)
    xN.set_order(N)
    S = 1
    for n in range(1, N+1):
        S *= (N-n+1)
        xN.set_derivative(n, scale_func(_power(N-n), S))
    return xN
