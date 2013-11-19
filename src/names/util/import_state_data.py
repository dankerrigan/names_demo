__author__ = 'dankerrigan'

import sys

from data import directory_reader
from importer import importer, named_tuple_dict_reader

MAX_YEAR = 2012
START_YEAR = MAX_YEAR - 5
STOP_YEAR = MAX_YEAR
COLLECTION = 'names'

def year_filter(dict_reader):
    for data in dict_reader:
        if START_YEAR <= data['year'] <= MAX_YEAR:
            yield data

if __name__ == '__main__':
    state_file_path = sys.argv[1]

    data_source = year_filter(named_tuple_dict_reader(directory_reader(state_file_path)))

    importer(COLLECTION, data_source)
