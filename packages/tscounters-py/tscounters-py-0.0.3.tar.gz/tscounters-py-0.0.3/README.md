# Overview

tscounters implements time series counters based on opentsdb. The key contribution of this library is to aggregate the counter submission to opentsdb to avoid high QPS to the counter server.


# Example Code

The following is an example of how to use tscounters:

```
import tscounters
import time
import random


tscounters.init()
tscounters.add_counter_engine(
    tscounters.OpenTSDBCounterEngine(
        hostname="opentsdb-server-hostname"
    )
)

counter = tscounters.SimpleCounter(
    name="counter-name",
    aggregator=tscounters.SumAggregator(),
)

while True:
    counter.set(random.randint(0, 9), {"tag1": "1", "tag2": "2"})
    time.sleep(0.1)
```
