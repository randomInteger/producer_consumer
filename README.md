# producer_consumer
Two implementations of the producer-consumer problem in Python3.

# fifo_queue.py
A bare bones version of a single producer and single consumer thread working
on a shared work queue.  Condition is used to handle thread synchronization,
as it is cleaner than using Lock or Semaphore in this case.

# multi_fifo_queue.py
This version is the more Pythonic way to handle this problem, as it uses the
amazing Queue() class to handle synchronization even for multiple producer and
multiple consumer threads all sharing the same work queue.
