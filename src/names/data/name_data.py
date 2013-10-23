__author__ = 'dankerrigan'

from riakjson.client import Client
from riakjson.query import Query
from riakjson.query import ASCENDING, DESCENDING, and_args, eq, between, regex

from states import states

MAX_YEAR = 2012

#from collections import OrderedDict

class NameData(object):
    def __init__(self):
        self.client = Client()
        self.names = self.client.names

    def _aggregate_year_gender(self, data, start_year=MAX_YEAR, stop_year=MAX_YEAR):
        year_data = dict()

        for i in xrange(start_year, stop_year + 1):
            year_data[i] = {'M': 0, 'F': 0}

        for item in data:
            year_data[item['year']][item['gender']] += item['count']

        return year_data

    def _aggregate_name(self, data):
        names = dict()
        for item in data:
            try:
                names[item['name']] += item['count']
            except KeyError:
                names[item['name']] = item['count']

        return names


    def _print_result(self, data):
        for item in data:
            print item

    def name_usage(self, name, start_year=MAX_YEAR, stop_year=MAX_YEAR):
        q = Query(and_args(eq('name', name), between('year', start_year, stop_year)))
        q.limit(1000)

        result = self.names.find(q.build())

        return self._aggregate_year_gender(result, start_year, stop_year)

    def partial_name_search(self, name_prefix):
        q = Query(regex('name', name_prefix + '*'))
        q.limit(1000)

        result = self.names.find(q.build())

        return self._aggregate_name(result)

    def popularity_by_state(self, state, count, sort_order):
        popular = [dict() for i in xrange(count)]

        for gender in ['M', 'F']:
            q = Query(and_args(eq('state', state), eq('gender', gender)))
            q.limit(count)
            q.order({'count': sort_order})

            result = self.names.find(q.build(), result_limit=count)

            for i, item in enumerate(result):
                popular[i][gender] = [item['name'], item['count']]

        return popular

    def state_popularity(self, count, sort_order):
        popular = dict()
        for state in states:
            popular[state] = self.popularity_by_state(state, count, sort_order)

        return popular



if __name__ == '__main__':
    import sys
    names = NameData()

    if sys.argv[1] == 'usage':
        print names.name_usage(sys.argv[2])

    elif sys.argv[1] == 'partial':
        print names.partial_name_search(sys.argv[2])

    elif sys.argv[1] == 'most_state':
        print names.popularity_by_state(sys.argv[2], int(sys.argv[3]), DESCENDING)

    elif sys.argv[1] == 'least_state':
        print names.popularity_by_state(sys.argv[2], int(sys.argv[3]), ASCENDING)