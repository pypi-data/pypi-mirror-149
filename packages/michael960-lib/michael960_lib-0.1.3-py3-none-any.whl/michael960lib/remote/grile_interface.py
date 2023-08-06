from ..file_util import path
from griled.grile import Grile


GRILED_FILE = 'griled_info.json'
def get_grile():
    return Grile(path.get_compute_root() + '/' + GRILED_FILE)
