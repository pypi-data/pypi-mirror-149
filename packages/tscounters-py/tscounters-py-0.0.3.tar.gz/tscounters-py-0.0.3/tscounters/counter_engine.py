from prometheus_client import CollectorRegistry, Counter, Histogram, push_to_gateway
import json
import logging
import requests
import time


class CounterEngine:
    def commit_counter(self, counter):
        raise NotImplemented()


class OpenTSDBCounterEngine(CounterEngine):
    def __init__(self, hostname, port=4242):
        self.hostname = hostname
        self.port = port
        self.session = requests.Session()

    def commit_metrics(self, metrics):
        if not metrics:
            return True

        logging.debug("commiting metrics {} to opentsdb".format(metrics))

        res = self.session.post(
            "http://{}:{}/api/put?details=true".format(self.hostname, self.port),
            data=json.dumps(metrics),
        )
        return res.status_code == 200


class PrometheusCounterEngine(CounterEngine):
    def __init__(self, hostname, port=80, job_name="tscounters"):
        self.hostname = hostname
        self.port = port
        self.job_name = job_name

        self.registry = CollectorRegistry()
        self.counters = {}

    def get_counter(self, counter_name, tags):
        key = "{}({})".format(counter_name, ",".join(tags))

        if key not in self.counters:
            logging.info("creating counter {} with tags {}".format(counter_name, tags))
            self.counters[key] = Counter(
                counter_name,
                counter_name,
                tags,
                registry=self.registry,
            )

        return self.counters[key]

    def commit_metrics(self, metrics):
        if not metrics:
            return True

        logging.info("commiting metrics {} to prometheus".format(metrics))

        for metric in metrics:
            name = metric["metric"]
            tags = metric["tags"]
            value = metric["value"]

            counter = self.get_counter(name, list(tags.keys()))
            counter.labels(**tags).inc(value)

        push_to_gateway(
            "http://{}:{}".format(self.hostname, self.port),
            job=self.job_name,
            registry=self.registry,
        )

        return True
