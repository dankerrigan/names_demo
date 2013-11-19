__author__ = 'dankerrigan'

import multiprocessing
import sys

from riakjson.client import Client


_data_queue = multiprocessing.Queue(100)
_result_queue = multiprocessing.Queue(100)
_status_flag = multiprocessing.Value('i', 0)
_worker_count = 4


def named_tuple_dict_reader(named_tuples):
    for named_tuple in named_tuples:
        yield named_tuple._asdict()


def data_inserter(collection_name, data_queue, result_queue, status_flag):
    client = Client()
    collection = client[collection_name]

    while True:
        data = data_queue.get()
        if data:
            try:
                key = collection.insert(data)
                result_queue.put(key)
            except Exception as e:
                print e
                # set status to stopped because of error, should stop import_data
                _status_flag = -1
                # send stopped to result_processor
                result_queue.put(None)
                break
        else:
            result_queue.put(None)
            break


def result_processor(result_queue):
    stop_count = 0
    result_count = 0

    while True:
        result = result_queue.get()
        if not result:
            stop_count += 1
        else:
            result_count += 1
            sys.stdout.write('{0:10d}\r'.format(result_count))
        if stop_count == _worker_count:
            break


def import_data(data_source, data_queue):
    for data in data_source:
        if _status_flag < 0:
            print 'Exception encountered, stopping'
            break
        data_queue.put(data)

    # stop data_inserter workers
    for i in xrange(_worker_count):
        data_queue.put(None)


def importer(collection_name, data_source):
    print 'Started'
    workers = list()
    for i in xrange(_worker_count):
        workers.append(multiprocessing.Process(target=data_inserter, args=(collection_name,
                                                                           _data_queue,
                                                                           _result_queue,
                                                                           _status_flag)))

    result_proc = multiprocessing.Process(target=result_processor, args=[_result_queue])

    result_proc.start()
    for worker in workers:
        worker.start()

    import_data(data_source, _data_queue)

    for worker in workers:
        worker.join()

    result_proc.join()

    print 'Finished'