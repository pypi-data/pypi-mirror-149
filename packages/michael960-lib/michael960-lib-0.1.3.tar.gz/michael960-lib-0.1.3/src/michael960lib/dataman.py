import json
import pathlib
import pprint
import os
import numpy as np
from .file_util import path as pt
#interface for various

#datapath = str(pathlib.Path(__file__).parent.parent.parent.absolute()) + '/data/'
datapath = pt.get_project_root()

def get_path():
    return datapath


#a dictionary of metal properties
def read_metals():
    with open(datapath + 'metals.json', 'r') as f:
        metals = json.load(f)
    metals1 = dict()
    for metal in metals:
        tmp = dict()
        tmp['Tm'] = metal['Tm']
        tmp['Tb'] = metal['Tb']
        tmp['lattice'] = metal['lattice']
        tmp['n'] = metal['n']
        tmp['a'] = metal['a']
        metals1[metal['symbol']] = tmp

    return metals1


#gets md simulation results
def get_md_data():
    md_path = datapath + 'md/'
    with open(md_path + 'meta.json', 'r') as f:
        meta = json.load(f)

    metals = read_metals()

    for key in meta:
        exp = meta[key]
        if exp['success']:
            exp_path = md_path + key + "/"

            #g(r)
            if os.path.isfile(exp_path + "g.dat"):
                with open(exp_path + "g.dat") as f:
                    gdat = f.read()
                r, g = read_data_1(gdat)
                exp['g'] = (r, g)

            #additional time step info (lat_param)
            if os.path.isfile(exp_path + "lat_param.json"):
                with open(exp_path + "lat_param.json") as f:
                    lat_param = json.load(f)
                exp['lat_param'] = lat_param
        
        metal = 'null'
        if exp['subject'] in metals:
            metal = metals[exp['subject']]
            print(metal)
        
        #determines simulation region
        if not 'region' in exp:
            exp['region'] = 'null'
        if ((not 'lattice' in exp) or exp['lattice'] == 'default') and metal != 'null':
            exp['lattice'] = {
                'type': metal['lattice'],
                'a': metal['a']
            }
        
        

            


    return meta
    

def read_data_1(raw):
    data = raw.split('\n')
    A = []
    B = []
    for ln in data:
        if not (ln.startswith('#') or len(ln)==0):
            nums = ln.split()
            A.append(float(nums[1]))
            B.append(float(nums[2]))
    return np.array(A), np.array(B)
