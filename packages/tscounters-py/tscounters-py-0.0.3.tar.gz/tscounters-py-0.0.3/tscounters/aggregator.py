import time


class Aggregator:
    def aggregate(self, values):
        raise NotImplemented()

    def reset(self):
        pass


class SumAggregator(Aggregator):
    def aggregate(self, values):
        return sum(values)


class AvgAggregator(Aggregator):
    def aggregate(self, values):
        if not values:
            return 0
        else:
            return sum(values) / len(values)


class RateAggregator(Aggregator):
    def __init__(self):
        self.window_start_ts = time.time()

    def aggregate(self, values):
        window_end_ts = time.time()
        return sum(values) / (window_end_ts - self.window_start_ts)

    def reset(self):
        self.window_start_ts = time.time()
