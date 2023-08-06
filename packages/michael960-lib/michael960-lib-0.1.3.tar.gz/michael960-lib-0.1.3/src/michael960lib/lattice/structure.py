import numpy as np
from ..math import length


def get_bcc_site(a, ml):
    seeds = get_bcc_seed(ml)
    r = set()
    dg_dc = []
    for seed in seeds:
        dg = 0
        mag = length(seed) * 0.5 * a
        for s1 in sym_neg(seed):
            for s2 in sym_perm(s1):
                if not s2 in r:
                    dg += 1
                r.add(s2)
        dg_dc.append([seed, dg, mag])
    return np.array(sorted(r, key=lambda e: length(e) + 1e-10 * max(np.abs(e)))) * 0.5 * a, dg_dc


def get_fcc_site(a, ml):
    seeds = get_fcc_seed(ml)
    r = set()
    dg_dc = []
    for seed in seeds:
        dg = 0
        mag = 0.5 * a * length(seed)
        for s1 in sym_neg(seed):
            for s2 in sym_perm(s1):
                if not s2 in r:
                    dg += 1
                r.add(s2)
        dg_dc.append([seed, dg, mag])
    return np.array(sorted(r, key=lambda e: length(e) + 1e-10 * max(np.abs(e)))) * 0.5 * a, dg_dc


def get_bcc_rlv(a, ml):
    return get_fcc_site(4 * np.pi / a, ml)


def get_fcc_rlv(a, ml):
    return get_bcc_site(4 * np.pi / a, ml)


def get_bcc_seed(ml):
    px = np.array([-1, 1, 1])
    py = np.array([1, -1, 1])
    pz = np.array([1, 1, -1])
    r = set()
    N = int(np.ceil(ml / np.sqrt(3))) + 1
    for i in range(N):
        for j in range(N):
            for k in range(N):
                p = np.abs(px*i + py*j + pz*k)
                if length(p) <= ml:
                    r.add(tuple(sorted(np.abs(px*i + py*j + pz*k))[::-1]))
    r1 = []
    for sd in r:
        r1.append(sd)
    return (sorted(r1, key=lambda e: length(e) + 1e-10 * max(e)))    


def get_fcc_seed(ml):
    px = np.array([0, 1, 1])
    py = np.array([1, 1, 0])
    pz = np.array([1, 0, 1])
    r = set()
    N = int(np.ceil(ml / np.sqrt(2))) + 1
    for i in range(-N, N):
        for j in range(-N, N):
            for k in range(-N, N):
                p = np.abs(px*i + py*j + pz*k)
                if length(p) <= ml:
                    r.add(tuple(sorted(np.abs(px*i + py*j + pz*k))[::-1]))
    r1 = []
    for sd in r:
        r1.append(sd)
    return (sorted(r1, key=lambda e: length(e) + 1e-10 * max(e)))


def sym_perm(e):
    return [(e[0], e[1], e[2]), (e[0], e[2], e[1]), 
            (e[1], e[0], e[2]), (e[1], e[2], e[0]),
            (e[2], e[0], e[1]), (e[2], e[1], e[0])]


def sym_neg(e):
    return [
        (e[0], e[1], e[2]), (-e[0], e[1], e[2]),
        (e[0], -e[1], e[2]), (e[0], e[1], -e[2]),
        (-e[0], -e[1], e[2]), (e[0], -e[1], -e[2]),
        (-e[0], e[1], -e[2]), (-e[0], -e[1], -e[2]),
    ]

    
def sym(seed):
    r = set()
    for s1 in sym_neg(seed):
        for s2 in sym_perm(s1):
            r.add(s2)
    return r


#conversion for lattice constant, number density, nearest neighbor distance, first shell rlv length
def convert(X, param1, param2, structure):
    if structure == 'fcc':
        a = X
        if param1 == 'a':
            a = X
        elif param1 == 'rho':
            a = (4 / X) ** (1/3)
        elif param1 == 'd':
            a = np.sqrt(2) * X
        elif param1 == 'k':
            a = 2 * np.sqrt(3) * np.pi / X
        else:
            raise ValueError(f'{param1} is not a valid lattice parameter.')

        if param2 == 'a':
            return a
        elif param2 == 'rho':
            return 4 / a**3
        elif param2 == 'd':
            return a / np.sqrt(2)
        elif param2 == 'k':
            return 2 * np.sqrt(3) * np.pi / a
        else:
            raise ValueError(f'{param2} is not a valid lattice parameter.')
    elif structure == 'bcc':
        a = X
        if param1 == 'a':
            a = X
        elif param1 == 'rho':
            a = (2/X) ** (1/3)
        elif param1 == 'd':
            a = 2/np.sqrt(3) * X
        elif param1 == 'k':
            a = 4 * np.sqrt(2) * np.pi / X
        else:
            raise ValueError(f'{param1} is not a valid lattice parameter.')

        if param2 == 'a':
            return a
        elif param2 == 'rho':
            return 2 / a**3
        elif param2 == 'd':
            return np.sqrt(3)/2 * a
        elif param2 == 'k':
            return 4 * np.sqrt(2) * np.pi / a
        else:
            raise ValueError(f'{param2} is not a valid lattice parameter.')
    else:
        raise ValueError(f'{structure} is not a valid lattice structure.')
