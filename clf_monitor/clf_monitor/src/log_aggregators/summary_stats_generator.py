from log_aggregators.base_aggregator import LogAggregator
from storage.base_storage import BaseCLFStorageEngine
import time


class SummaryStats:
    def __init__(self):
        self.TOP_RESOURCES = None
        self.TOP_USERS = None
        self.TOP_METHODS = None
        self.TOP_RESPONSE_CODES = None
        self.AVG_REQUEST_SIZE = None
        self.REQUEST_COUNT = None
        self.TRAFFIC_SPEED = None

    def __eq__(self, other):

        if len(set(self.TOP_RESOURCES) - set(other.TOP_RESOURCES)) > 0:
            return False
        if len(set(self.TOP_USERS) - set(other.TOP_USERS)) > 0:
            return False
        if len(set(self.TOP_METHODS) - set(other.TOP_METHODS)) > 0:
            return False
        if len(set(self.TOP_RESPONSE_CODES) - set(other.TOP_RESPONSE_CODES)) > 0:
            return False
        if self.AVG_REQUEST_SIZE != other.AVG_REQUEST_SIZE:
            return False
        if self.REQUEST_COUNT != other.REQUEST_COUNT:
            return False
        if int(self.TRAFFIC_SPEED) != int(other.TRAFFIC_SPEED):
            return False

        return True


class SummaryStatGenerator(LogAggregator):
    def __init__(self, name, interval, period, store):
        super().__init__(period, interval)
        self.name = name
        if not isinstance(store, BaseCLFStorageEngine):
            raise TypeError("store should be of type BaseCLFStorageEngine!")
        self.store = store

    def _aggregate(self, now):
        response = SummaryStats()

        start_time = int(now - self.interval)
        end_time = int(now)
        resources = self.store.group_by(fields="resource",
                                        aggr_method="COUNT",
                                        aggr_field="*",
                                        start_time=start_time,
                                        end_time=end_time)
        resources.sort(key=lambda x: x[1], reverse=True)

        users = self.store.group_by(fields="user",
                                    aggr_method="COUNT",
                                    aggr_field="*",
                                    start_time=start_time,
                                    end_time=end_time)
        users.sort(key=lambda x: x[1], reverse=True)

        methods = self.store.group_by(fields="method",
                                      aggr_method="COUNT",
                                      aggr_field="*",
                                      start_time=start_time,
                                      end_time=end_time)
        methods.sort(key=lambda x: x[1], reverse=True)

        response_codes = self.store.group_by(fields="response_code",
                                             aggr_method="COUNT",
                                             aggr_field="*",
                                             start_time=start_time,
                                             end_time=end_time)
        response_codes.sort(key=lambda x: x[1], reverse=True)

        avg_req_size_ = self.store.aggregate_by(field="size",
                                               aggr_method="AVG",
                                               start_time=start_time,
                                               end_time=end_time)
        avg_req_size = 0
        if avg_req_size_[0]:
            if avg_req_size_[0][0]:
                avg_req_size = avg_req_size_[0][0]


        request_count = self.store.aggregate_by(field="*",
                                                aggr_method="COUNT",
                                                start_time=start_time,
                                                end_time=end_time)
        
        request_count = request_count[0][0] if request_count[0] else None
        response.TOP_RESOURCES = resources[:5]
        response.TOP_USERS = users[:5]
        response.TOP_METHODS = methods[:5]
        response.TOP_RESPONSE_CODES = response_codes[:5]
        response.AVG_REQUEST_SIZE = int(avg_req_size)
        response.REQUEST_COUNT = request_count
        response.TRAFFIC_SPEED = request_count / self.interval

        return response

    def aggregate(self):
        now = time.time()

        response = self._aggregate(now)
        summary_template = "\n" \
                           "Summary Stats:\n" \
                           "TOP RESOURCES: ------- {0}\n" \
                           "TOP USERS: ----------- {1}\n" \
                           "TOP METHODS: --------- {2}\n" \
                           "TOP RESPONSE CODES: -- {3}\n" \
                           "AVG REQUEST SIZE: ---- {4}\n" \
                           "REQUEST COUNT: ------- {5}\n" \
                           "Traffic SPEED: ------- {6}\n"

        summary = summary_template.format(
            response.TOP_RESOURCES,
            response.TOP_USERS,
            response.TOP_METHODS,
            response.TOP_RESPONSE_CODES,
            response.AVG_REQUEST_SIZE,
            response.REQUEST_COUNT,
            response.TRAFFIC_SPEED
        )
        print(summary)
