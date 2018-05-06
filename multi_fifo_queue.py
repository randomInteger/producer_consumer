#!/usr/bin/env python3
'''
This is a very straightforward example of how the amazing Queue() class can
make it extremely easy to write straightforward, idiomatic Python3 code to
solve the producer-consumer problem with multiple threads working on the same
queue.

Compare this to the fifo_queue.py version and see how much more we can do with
less code when we use Queue().

Author:  c.gleeson May 2018
'''
import random
from queue import Queue
from time import sleep
from threading import Thread


#Note we do not need to use the threadsafe Queue class.
max_queue_size = 64
work_queue = Queue(max_queue_size)
condition = Condition()
max_producers = 8
max_consumers = 8

#Subclassing Thread() makes this way cleaner
class Producer(Thread):
    def run(self):
        while True:
            item = random.randrange(1,1000000)
            #Queue handles sleeping and signaling between threads
            work_queue.put(item)
            print("Produced item:", str(item))
            #sleep a small time so we have interesting results...
            sleep(random.random()/100000)

#Subclassing Thread() makes this way cleaner
class Consumer(Thread):
    def run(self):
        while True:
            #Queue handles sleeping and signaling between threads
            item = work_queue.get()
            print("Consumed item:", str(item))
            sleep(random.random()/100000)

#Announcements
print("Producer - Consumer example starting with:")
print("Number of producer threads:", str(max_producers))
print("Number of consumer threads:", str(max_consumers))
print("Work Queue Size:", str(max_queue_size))
print("Sleeping for 2 sec, then proceeding.  CTRL+Z to kill.")
sleep(2)


#Start the work
producer_list = []
for x in range(1,max_producers+1):
    producer_list.append(Producer())

consumer_list = []
for x in range(1,max_consumers+1):
    producer_list.append(Consumer())

for prod in producer_list:
    prod.start()

for con in consumer_list:
    con.start()
