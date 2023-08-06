from ..file_util.path import get_project_root, get_compute_root, get_running_script, get_elements, get_home
import __main__
import json
from .remote import record_json, record, at_server
from ..file_util.data import ndarray_to_list as tolist
from .logging import get_log, Logger
import os
import pathlib

#logs simulations
project_root = get_project_root()
compute_root = get_compute_root()
server_data_dir = get_home() + '/Data'

class Logger:
    def __init__(self):
        pass

# returns the registered information in info.json. 
def get_data_dump():
    relative_main = get_running_script().lstrip(compute_root)
    elements = relative_main.split('/')
    if len(elements) >= 3:
        return get_sim_info()['data']
    return None

def get_sim_info():
    relative_main = get_running_script().lstrip(compute_root)
    elements = relative_main.split('/')
    if len(elements) >= 3:
        info = get_info()
        sim_id = elements[1]
        return info[sim_id]
    return None

def get_info():
    relative_main = get_running_script().lstrip(compute_root)
    elements = relative_main.split('/')
    if len(elements) >= 2:
        datedir = elements[0]
        infofile = f'{compute_root}/{datedir}/info.json'
        with open(infofile, 'r') as f:
            info = json.load(f)
        return info
    return None

def get_group():
    relative_main = get_running_script().lstrip(compute_root)
    elements = relative_main.split('/')
    if len(elements) >= 2:
        return elements[0]
    return None

def get_sim():
    elements = get_elements()
    if len(elements) >= 3:
        return elements[1]
    return None

def prepare_new_run(logger: Logger, params=None):
    logger.start()
    log = get_log()


    max_id = -1
    curr_id = 0
    elements = get_elements()
    group = None
    sim_id = None
    if len(elements) >= 3:
        group = elements[0]
        sim_id = elements[1]

    if at_server():
        for run in log:
            max_id = max(run['id'], max_id)
        curr_id = max_id + 1

        dest_dir = f'{server_data_dir}/{group}/{sim_id}/{curr_id}'
        print(f'Destination: {dest_dir}')
        if not os.path.isdir(dest_dir):
            pathlib.Path(dest_dir).mkdir(parents=True, exist_ok=True)
            print('Destination does not exist. Made directory')
    else:
        print('Simulation running at client')


    sim_info = {''}
    if not params is None:
        sim_info = params

    logger.put('params', sim_info)
    logger.put('id', curr_id)

def finalize_run(logger: Logger):
    logger.end()
    write_json(logger, '.log', logger.log)
    


def update_params(logger: Logger, params: dict):
    logger.put('params', params)


def get_file(logger, file_id):
    dump = get_data_dump()

    if not at_server():
        print('Cannot write at client')
        return

    if dump is None:
        print('Not a valid simulation')
        return
    
    group = get_group()
    sim_id = get_sim()
    dir0 = f'{group}/{sim_id}/{logger.log["id"]}'

    if file_id == '.log':
        return f'{dir0}/.log.json'

    if file_id not in dump:
        print(f'Permission denied: {file_id} is not a registered key')
        return

    filename = dump[file_id]['file']
    return f'{dir0}/{filename}'

# write data
def write(logger, file_id, data):
    fullpath = get_file(logger, file_id)
    if not fullpath is None:
        record(fullpath, data)

#write json data
def write_json(logger, file_id, obj):
    write(logger, file_id, json.dumps(obj, indent=4))
