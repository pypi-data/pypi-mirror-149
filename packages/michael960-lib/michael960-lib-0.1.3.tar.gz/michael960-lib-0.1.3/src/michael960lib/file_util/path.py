import sys
import pathlib
from pprint import pprint
import __main__

def get_project_root():
    main_path = pathlib.Path(__main__.__file__).absolute()
    new_path = main_path
    s = str(main_path)
    while s != "" and s != "/":
        new_path = new_path.parent
        if new_path.name == 'compute':
            return str(new_path.parent)
    return None

def get_compute_root():
    return get_project_root() + '/compute'


def get_home():
    return str(pathlib.Path.home())

def get_running_script():
    main_path = pathlib.Path(__main__.__file__).absolute()
    return str(main_path)


def get_elements():
    compute_root = get_compute_root()
    relative_main = get_running_script().lstrip(compute_root)
    elements = relative_main.split('/')
    return elements

