from ..file_util import path as pt
import json, ujson
import socket
from os.path import isfile
from datetime import datetime
import os
import time

servers = ['poincare', 'lyapunov']
server_data_dir = pt.get_home() + '/Data'
server_common_dir = pt.get_home() + '/Common'
server_tmp_dir = pt.get_home() + '/Simulation/tmp'

existing_tmp_keys = set()

def get_machine():
    return socket.gethostname()


def at_server():
    name = get_machine()
    if name in servers:
        return True
    return False


def retrieve(machine, filename):
    if at_server():
        print('Can\'t retrieve data in server')
        return
    
    ss = pt.get_project_root()
    with open(f'{ss}/mnt/{machine}.data/{filename}', 'r') as f:
        s = f.read()
    return s

def retrieve_json(machine, filename):
    #return json.loads(retrieve(machine, filename))
    return ujson.loads(retrieve(machine, filename))


def get(machine, date, name):
    return retrieve(machine, f'{date}/{name}')

def get_json(machine, date, name):
    return retrieve_json(machine, f'{date}/{name}')

def read(filename):
    if not at_server():
        print('Use retrieve() instead to get data')
        return '{}'

    with open(f'{server_data_dir}/{filename}', 'r') as f:
        s = f.read()
    return s

def read_json(filename):
    return json.loads(read(filename))

def record(filename, s, check=False, verbose=True):
    if not at_server():
        print('Can\'t record data at client')
        return

    filepath = f'{server_data_dir}/{filename}'
    if check:
        if isfile(filepath):
            c = input(f'{filepath} already exists. Override?')
            if c == 'y' or c == 'Y':
                pass
            else:
                return


    with open(f'{server_data_dir}/{filename}', 'w+') as f:
        f.write(s)
        if verbose:
            print(f'Data written to {server_data_dir}/{filename}')

def record_json(filename, obj, check=False, verbose=True):
    record(filename, json.dumps(obj, indent=4), check, verbose)


def universal_retrieve(machine, filename):
    if at_server():
        with open(f'{server_common_dir}/{machine}.data/{filename}', 'r') as f:
            s = f.read()
        return s
    else:
        return retrieve(machine, filename)

def universal_retrieve_json(machine, filename):
    #return json.loads(universal_retrieve(machine, filename))
    return ujson.loads(universal_retrieve(machine, filename))
    

def universal_get(machine, date, name):
    return universal_retrieve(machine, f'{date}/{name}')

def universal_get_json(machine, date, name):
    return universal_retrieve_json(machine, f'{date}/{name}')

def generate_tmp_key(time_buffer=150):
    key = str(datetime.now()).replace('-', '_').replace(':', '_').replace('.', '_').replace(' ', '.')
    existing_tmp_keys.add(key)
    file_name = f'{server_tmp_dir}/{key}.tmp'

    with open(file_name, 'w+') as f:
        pass

    time.sleep(time_buffer/1000)
    return key

def del_tmp(key):
    if not at_server():
        print('Can\'t remove temp files at client')
        return

    if not key in existing_tmp_keys:
        print(f'Key {key} does not exist.')
        return

    existing_tmp_keys.remove(key)
    file_name = f'{server_tmp_dir}/{key}.tmp'
    try:
        os.remove(file_name)
    except:
        print(f'[TempFile]: {server_tmp_dir}/{key}.tmp does not exist, so it is not removed')


def dump_tmp(key, content):
    if not at_server():
        print('Can\'t dump temp files at client')
        return

    if not key in existing_tmp_keys:
        print('Please generate a key first.')
        return

    file_name = f'{server_tmp_dir}/{key}.tmp'
    with open(file_name, 'w+') as f:
        f.write(content)


def load_tmp(key):
    if not at_server():
        print('Can\'t load temp files at client')
        return

    if not key in existing_tmp_keys:
        print(f'Key {key} does not exist.')
        return

    file_name = f'{server_tmp_dir}/{key}.tmp'
    with open(file_name, 'r') as f:
        s = f.read()
    return s


def tmp_path(key):
    if not at_server():
        print('Can\'t load temp files at client')
        return

    if not key in existing_tmp_keys:
        print(f'Key {key} does not exist.')
        return

    return  f'{server_tmp_dir}/{key}.tmp'






