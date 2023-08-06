import numpy as np
from collections import defaultdict

from typing import Union
from numbers import Number

import os
import re

import readline
import warnings


def overrides(interface_class):
    def overrider(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return overrider

def deprecated(message):
    def deprecator(func):
        def wrapper(*args, **kwargs):
            warnings.warn(message, DeprecationWarning)
            return func(*args, **kwargs)
        return wrapper
    return deprecator

def experimental(message):
    def dec(func):
        def wrapper(*args, **kwargs):
            warnings.warn(message, RuntimeWarning)
            return func(*args, **kwargs)
        return wrapper 
    return dec


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    OKCYAN = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Dummy:
    def __init__(self, name):
        self.name = name

    def __add__(self, other):
        if other == 0:
            return self
        return Dummy(f'{self.name}+{str(other)}')
        

    def __mul__(self, other):
        if other == 0:
            return 0
        return Dummy(f'{self.name}*{str(other)}')

    def __rmul__(self, other):
        if other == 0:
            return 0
        return Dummy(f'{str(other)}*{self.name}')

    def __radd__(self, other):
        if other == 0:
            return self
        return Dummy(f'{str(other)}+{self.name}')

    def __truediv__(self, other):
        return Dummy(f'{self.name}/{str(other)}')

    def __sub__(self, other):
        return Dummy(f'{self.name}-{str(other)}')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __array_ufunc__(self, *args, **kwargs):
        fname = args[0].__name__
        if fname == 'add':
            return self.__radd__(args[2])
        if fname == 'multiply':
            return self.__rmul__(args[2])
        return Dummy(f'{fname}({self.name})')

    def __pow__(self, other):
        return Dummy(f'{self.name}^{str(other)}')


def generate_title(title, line_char, length, length_left):
    l = len(title)
    if length_left == -1:
        length_left = (length - l - 2) // 2
    prefix = line_char * length_left
    suffix = line_char * (length - length_left - l - 2)
    s = f'{prefix} {title} {suffix}'
    print(s)


def confirm():
    input('Press enter to proceed')
    print()




RE_SPACE = re.compile('.*\s+$', re.M)

class Completer(object):
    def __init__(self, commands):
        self.commands = commands

    def _listdir(self, root):
        "List directory 'root' appending the path separator to subdirs."
        res = []
        for name in os.listdir(root):
            path = os.path.join(root, name)
            if os.path.isdir(path):
                name += os.sep
            res.append(name)
        return res

    def _complete_path(self, path=None):
        "Perform completion of filesystem path."
        if not path:
            return self._listdir('.')
        dirname, rest = os.path.split(path)
        tmp = dirname if dirname else '.'
        res = [os.path.join(dirname, p)
                for p in self._listdir(tmp) if p.startswith(rest)]
        # more than one match, or single match which does not exist (typo)
        if len(res) > 1 or not os.path.exists(path):
            return res
        # resolved to a single directory, so return list of files below it
        if os.path.isdir(path):
            return [os.path.join(path, p) for p in self._listdir(path)]
        # exact file match terminates this completion
        return [path + ' ']

    def complete_extra(self, args):
        "Completions for the 'extra' command."
        if not args:
            return self._complete_path('.')
        # treat the last arg as a path and complete it
        return self._complete_path(args[-1])

    def complete(self, text, state):
        "Generic readline completion entry point."
        buffer = readline.get_line_buffer()
        line = readline.get_line_buffer().split()
        # show all commands
        if not line:
            return [c + ' ' for c in self.commands][state]
        # account for last argument ending in a space
        if RE_SPACE.match(buffer):
            line.append('')
        # resolve command to the implementation function
        cmd = line[0].strip()
        if cmd in self.commands:
            impl = getattr(self, 'complete_%s' % cmd)
            args = line[1:]
            if args:
                return (impl(args) + [None])[state]
            return [cmd + ' '][state]
        results = [c + ' ' for c in self.commands if c.startswith(cmd)] + [None]
        return results[state]





class IllegalActionError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ModifyingReadOnlyObjectError(IllegalActionError):
    def __init__(self, message, obj):
        super().__init__(message)
        self.obj = obj


# decorator for exporting objects
def with_type(type_name: str):
    def wrapper(export):
        def wrapped_export(self):
            state = export(self)
            state['type'] = type_name
            return state
        return wrapped_export
    return wrapper


def scalarize(data: Union[dict, list, np.ndarray, Number, str]):

    if isinstance(data, Number) or type(data) == str:
        return data

    if isinstance(data, np.ndarray):
        try:
            return scalarize(data.item())
        except ValueError:
            return data

    if type(data) == dict:
        r = dict()
        for key in data:
            r[key] = scalarize(data[key])
        return r
    
    if type(data) == list:
        return [scalarize(item) for item in data]

