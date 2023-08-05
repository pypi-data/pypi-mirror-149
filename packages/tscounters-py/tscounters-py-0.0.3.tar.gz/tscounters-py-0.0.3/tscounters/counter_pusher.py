import threading
import time
import logging

from .counters import counter_instances


counter_engines = []


def pusher_thread(commit_interval):
    while True:
        if counter_instances:
            logging.debug("Committing {} counters...".format(len(counter_instances)))

            for counter_instance in counter_instances:
                counter_instance.commit(counter_engines)

        time.sleep(commit_interval)


def init_counter_pusher(commit_interval=1):
    t = threading.Thread(target=pusher_thread, args=(commit_interval, ))
    t.daemon = True
    t.start()


def add_counter_engine(counter_engine):
    counter_engines.append(counter_engine)
