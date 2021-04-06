import time
import threading
import datetime
import re
from fs.log_reader import LogReader
from storage.base_storage import BaseCLFStorageEngine
from log_aggregators.base_aggregator import LogAggregator


class MonitorController:

    def __init__(self):
        self.log_aggregators = []
        self.log_reader = None
        self.log_store = None

    def set_log_reader(self, log_reader):
        if not isinstance(log_reader, LogReader):
            raise TypeError("log_reader should be of type LogReader")

        self.log_reader = log_reader

    def set_log_store(self, log_store):
        if not isinstance(log_store, BaseCLFStorageEngine):
            raise TypeError("log_store should be of type BaseCLFStorageEngine")

        self.log_store = log_store

    def add_log_processor(self, log_processor):
        if not isinstance(log_processor, LogAggregator):
            raise TypeError("log_processor should be of type LogAggregator")

        self.log_aggregators.append(log_processor)

    @staticmethod
    def clf_log_parser(line):
        log = list(map(''.join, re.findall(r'\"(.*?)\"|\[(.*?)\]|(\S+)', line)))
        method, resource, protocol = log[4].split(" ")
        date = datetime.datetime.strptime(log[3], "%d/%b/%Y:%H:%M:%S %z")
        time_tuple = date.timetuple()
        log_timestamp = int(time.mktime(time_tuple))
        log_obj = {"ip": log[0],
                   "user": log[2],
                   "log_time": log_timestamp,
                   "method": method,
                   "resource": "/{0}/*".format(log[4].split("/")[1]),
                   "protocol": protocol,
                   "response_code": int(log[5]),
                   "size": int(log[6])
                   }
        return log_obj

    def start(self):
        for log_agg in self.log_aggregators:
            threading.Thread(target=log_agg.start).start()

        while True:
            time.sleep(0.001)
            next_entry = self.log_reader.next()
            parsed_entry = self.clf_log_parser(next_entry)
            self.log_store.insert(parsed_entry)
            # print(parsed_entry)

