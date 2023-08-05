from .aggregator import SumAggregator, AvgAggregator, RateAggregator
from .counter_engine import OpenTSDBCounterEngine
from .counter_pusher import init_counter_pusher, add_counter_engine
from .counters import SimpleCounter


def init(commit_interval=1):
    init_counter_pusher(commit_interval=commit_interval)
