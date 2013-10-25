__author__ = 'dankerrigan'

import sys

from riakjson.client import Client

from ..util.data import directory_reader

MAX_YEAR = 2012
START_YEAR = MAX_YEAR - 5
STOP_YEAR = MAX_YEAR

if __name__ == '__main__':
    state_file_path = sys.argv[1]

    client = Client()
    names = client.names

    count = 0
    for i, record in enumerate(directory_reader(state_file_path)):
        if START_YEAR <= record.year <= STOP_YEAR:
            count += 1
            names.insert(record._asdict())
            sys.stdout.write('{0:10d}\r'.format(count))

    print '\nFinished'
