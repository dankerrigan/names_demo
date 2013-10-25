__author__ = 'dankerrigan'

from riakjson.client import Client
from riakjson.query import Query
from riakjson.query import ASCENDING, DESCENDING, and_args, eq, gte, lte, regex

from states import states

from pprint import pprint

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

    def _rank(self, data):
        min, max = 999, 0
        for key, value in data.items():
            if value > max:
                max = value
            if value < min:
                min = value

        ranked = dict()

        for key, value in data.items():
            ranked[key] = value/max

        return ranked


    def _print_result(self, data):
        for item in data:
            print item

    def name_usage(self, name, start_year=MAX_YEAR, stop_year=MAX_YEAR):
        q = Query(and_args(eq('name', name),
                           gte('year', start_year),
                           lte('year', stop_year)))
        q.limit(1000)

        result = self.names.find(q.build())

        return self._aggregate_year_gender(result.objects(), start_year, stop_year)

    def partial_name_search(self, name_prefix, start_year=MAX_YEAR, stop_year=MAX_YEAR):
        q = Query(and_args(regex('name', name_prefix + '.*'),
                           gte('year', start_year),
                           lte('year', stop_year)))

        q.limit(1000)

        #print q.build()

        result = self.names.find(q.build())

        return self._aggregate_name(result.objects())

    def popularity_by_state(self, state, count, sort_order, start_year=MAX_YEAR, stop_year=MAX_YEAR):
        popular = [dict() for i in xrange(count)]

        for gender in ['M', 'F']:
            q = Query(and_args(eq('state', state),
                               eq('gender', gender),
                               gte('year', start_year),
                               lte('year', stop_year)))
            q.limit(count)
            q.order({'count': sort_order})

            #print q.build()

            result = self.names.find(q.build())

            for i, item in enumerate(result.objects(result_limit=count)):
                popular[i][gender] = [item['name'], item['count']]

        return popular

    def state_popularity(self, count, sort_order, start_year=MAX_YEAR, stop_year=MAX_YEAR):
        popular = dict()
        for state in states:
            popular[state] = self.popularity_by_state(state, count, sort_order, start_year, stop_year)

        return popular

if __name__ == '__main__':
    import sys
    names = NameData()

    if sys.argv[1] == 'usage':
        pprint(names.name_usage(sys.argv[2]))

    elif sys.argv[1] == 'partial':
        pprint(names.partial_name_search(sys.argv[2]))

    elif sys.argv[1] == 'most_state':
        pprint(names.popularity_by_state(sys.argv[2], int(sys.argv[3]), DESCENDING))

    elif sys.argv[1] == 'least_state':
        pprint(names.popularity_by_state(sys.argv[2], int(sys.argv[3]), ASCENDING))

    elif sys.argv[1] == 'states_most':
        pprint(names.state_popularity(int(sys.argv[2]), DESCENDING))