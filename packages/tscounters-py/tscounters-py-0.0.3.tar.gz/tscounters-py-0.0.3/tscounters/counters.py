import collections
import time
import threading


counter_instances = []


class Counter:
    def __init__(self, name, aggregator=None):
        self.name = name
        self.data = collections.defaultdict(list)
        self.aggregator = aggregator
        self.lock = threading.Lock()

        counter_instances.append(self)

    def get_tags_str(self, tags):
        return ",".join(["{}:{}".format(k, v) for k, v in sorted(tags.items())])

    def set(self, value, tags=None):
        raise NotImplemented()

    def commit(self, counter_engines):
        raise NotImplemented()


class SimpleCounter(Counter):
    def set(self, value, tags=None):
        # Acquire lock.
        self.lock.acquire()

        # Update data.
        tags = tags or {}
        key = self.get_tags_str(tags)
        self.data[key].append((time.time(), value, tags))

        # Release lock.
        self.lock.release()

    def commit(self, counter_engines):
        # Acquire lock.
        self.lock.acquire()

        # Generate metrics.
        metrics = []
        for tag_str, tag_data in self.data.items():
            if self.aggregator is None:
                for ts, value, tags in tag_data:
                    metrics.append({
                        "metric": self.name,
                        "timestamp": int(ts * 1000),
                        "value": value,
                        "tags": tags,
                    })
            else:
                agg_value = self.aggregator.aggregate([
                    value for _, value, tags in tag_data
                ])

                metrics.append({
                    "metric": self.name,
                    "timestamp": int(time.time() * 1000),
                    "value": agg_value,
                    "tags": tag_data[0][2],
                })

        # Commit metrics.
        for counter_engine in counter_engines:
            counter_engine.commit_metrics(metrics)

        # Clear data.
        self.data.clear()

        # Reset aggregator.
        self.aggregator.reset()

        # Release lock.
        self.lock.release()
