from ..file_util import path as pt
import json


def from_poincare(date, name):
    s = pt.get_project_root()
    with open(f'{s}/mnt/office/compute/{date}/{name}', 'r') as f:
        s = f.read()
    return s

def json_from_poincare(date, name):
    return json.loads(from_poincare(date, name))

def json_from_liapunov(date, name):
    return
