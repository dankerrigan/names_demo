__author__ = 'dankerrigan'

import os

from collections import namedtuple

StateName = namedtuple('StateName', ['state', 'gender', 'year', 'name', 'count'])


def state_name_reader(name_file):
    for line in name_file:
        try:
            fields = line.strip().split(',')
            if len(fields) == 5:
                fields[2] = int(fields[2])
                fields[4] = int(fields[4])
                yield StateName(*fields)
        except Exception as e:
            print line, e


def directory_reader(path):
    for f in os.listdir(path):
        full_path = os.path.join(path, f)
        if os.path.isfile(full_path) and full_path.endswith('TXT'):
            with open(full_path, 'rb') as data_file:
                for data in state_name_reader(data_file):
                    yield data





