import abc
import time
import traceback

class LogAggregator:
    def __init__(self, period, interval):
        """

        By using base aggregation you can implement statistic generation,
        alerting and so on. Then you can inject those custom aggregations
        into main monitoring engine. Keep in mind you aggregations should
        implement this interface.

        @param period: Time in seconds, How many second aggregator should wait
        before starting another aggregation. Kind of once per how many second ?
        @type period: int
        @param interval: Interval in seconds. How big should be aggregation
        frame/window, time frame for this instance of aggregation.
        @type interval: int
        """

        self.period = period
        self.interval = interval

    @abc.abstractmethod
    def aggregate(self):
        raise NotImplementedError('Please implement aggregate method!')

    def start(self):
        # start this agg. only after min interval time.
        sleep_time = self.interval
        while True:
            time.sleep(sleep_time)
            start = time.time()
            try:
                self.aggregate()
            except BaseException as e:
                traceback.print_exc()
                print("Aggregation phase failed!")
            end = time.time()
            sleep_time = self.period - (end - start)
