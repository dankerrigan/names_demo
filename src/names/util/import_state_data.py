__author__ = 'dankerrigan'

import sys

from riakjson.client import Client

from ..util.data import directory_reader

#from ..data import data


if __name__ == '__main__':
    state_file_path = sys.argv[1]

    client = Client()
    names = client.names

    count = 0
    for i, record in enumerate(directory_reader(state_file_path)):
        if record.year > 1950 and record.year < 2012 :
            count += 1
            names.insert(record._asdict())
            sys.stdout.write('{0:10d}\r'.format(count))

    print '\nFinished'
