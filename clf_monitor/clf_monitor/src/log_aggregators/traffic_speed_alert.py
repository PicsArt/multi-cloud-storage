from log_aggregators.base_aggregator import LogAggregator
from storage.base_storage import BaseCLFStorageEngine
import time
from datetime import datetime


class TrafficSpeedAlert(LogAggregator):
    def __init__(self, name, interval, period, speed_threshold, store):
        super().__init__(period, interval)
        self.name = name
        self.speed_threshold = speed_threshold
        if not isinstance(store, BaseCLFStorageEngine):
            raise TypeError("store should be of type BaseCLFStorageEngine!")
        self.store = store
        self.alert_is_on = False

    def _aggregate(self, now):

        message = "High traffic generated an alert - " \
                  "hits = {0}, triggered at {1}"
        recovery_message = "Recovered from Traffic Alert  - " \
                           "his = {0} recovered at {1}"

        time_str = datetime.utcfromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')

        res = self.store.aggregate_by(field="*",
                                      aggr_method="COUNT",
                                      start_time=int(now - self.interval),
                                      end_time=int(now))
        req_count = res[0][0]
        speed = req_count / self.interval
        if self.alert_is_on is False:
            if speed > self.speed_threshold:
                self.alert_is_on = True
                return message.format(speed, time_str)
        else:
            if speed < self.speed_threshold:
                self.alert_is_on = False
                return recovery_message.format(speed, time_str)

        return None

    def aggregate(self):
        now = time.time()
        message = self._aggregate(now)
        if message:
            print(message)
