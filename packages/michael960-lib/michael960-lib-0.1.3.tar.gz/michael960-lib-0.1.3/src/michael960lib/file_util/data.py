import csv
import json
import numpy as np


def collect(lst, key, np_arr=False):
    l = []
    for d in lst:
        l.append(d[key])

    if np_arr:
        l = np.array(l)
    return l


def ndarray_to_list(arr):
    return [arr[i] for i in range(len(arr))]
