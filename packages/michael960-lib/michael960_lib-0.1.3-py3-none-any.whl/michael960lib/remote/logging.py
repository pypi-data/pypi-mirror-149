from ..file_util import path as pt
from .remote import at_server
import json
from datetime import datetime
import os

server_log_dir = pt.get_home() + '/Simulation/log'

def get_log():
    if not at_server():
        print('Cannot get log at client')
        return

    elements = pt.get_elements()
    if len(elements) >= 3:
        logfile = get_log_file()
        if os.path.isfile(logfile):
            with open(logfile, 'r') as f:
                log = json.load(f)
        else:
            print(f'Log file does not exist. {logfile} is created')
            with open(logfile, 'w+') as f:
                f.write('[]')
            log = []
        return log
    
    else:
        print('Not a valid simulation')

def get_log_file():
    elements = pt.get_elements()
    if len(elements) >= 3:
        group = elements[0]
        sim = elements[1]
        logfile = f'{server_log_dir}/{group}/{sim}.json'
        return logfile
    return None

class Logger:
    def __init__(self):
        self.time_start = None
        self.time_end = None
        self.duration = 0
        self.log = dict()

    def start(self):
        self.time_start = datetime.now()
        year = str(self.time_start.year)
        month = str(self.time_start.month)
        day = str(self.time_start.day)
        hour = str(self.time_start.hour)
        minute = str(self.time_start.minute)
        second = str(self.time_start.second)
        self.log['date'] = f'{year}-{month.rjust(2, "0")}-{day.rjust(2, "0")}'
        self.log['time'] = f'{hour.rjust(2, "0")}-{minute.rjust(2, "0")}-{second.rjust(2, "0")}'

    def end(self):
        if self.time_start is None:
            print('Call start() before calling end()')
            return
        self.time_end = datetime.now()
        self.log['duration'] = (self.time_end - self.time_start).seconds
        

        if at_server():
            main_log = get_log()
            main_log.append(self.log)
            logfile = get_log_file()
            with open(logfile, 'w+') as f:
                json.dump(main_log, f, indent=4)
        else:
            print('Could not update log file at client')

    def put(self, key, val):
        if not self.time_start is None:
            if self.time_end is None:
                self.log[key] = val
            else:
                print('Logger has already ended')
        else:
            print('Logger has not started yet')
