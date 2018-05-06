#!/usr/bin/env python3
'''
This is an example of the producer consumer problem for single threads
in a Pythonic way without using Queue (deliberately).

Using Condition is really elegant in that it completely removes the need to deal
wtih Locks (formerly mutex in Python2) and Semaphores.

If you were to extend this to having MULTIPLE producers and consumers at the
same time, you would be best served to use Queue().

Author:  c.gleeson May 2018
'''
import random
from time import sleep
from threading import Thread, Condition
#Condition is really the key to making this easier if you cannot use Queue()

#Note we are deliberately not using the very excellent Queue() class.
work_queue = []
max_queue_size = 64
condition = Condition()

#Subclassing Thread() makes this way cleaner
class Producer(Thread):
    def run(self):
        while True:
            item = random.randrange(1,1000000)
            #Enter critical section
            condition.acquire()
            if len(work_queue) == max_queue_size:
                print("Producer going to sleep, queue is full...")
                #We need to give up control until the consumer meets the condition
                condition.wait()
                print("Producer woken up, proceeding with item:", str(item))
            work_queue.append(item)
            #Must notify in case the consumer is sleeping
            condition.notify()
            #Must give the condition back because we are done
            condition.release()
            #sleep a small time so we have interesting results...
            sleep(random.random()/10)

#Subclassing Thread() makes this way cleaner
class Consumer(Thread):
    def run(self):
        while True:
            #Enter critical section
            condition.acquire()
            #Check the Queue
            if len(work_queue) == 0:
                print("Consumer going to sleep, queue is empty...")
                #We need to wait for a signal from the producer
                condition.wait()
                print("Consumer woken up, proceeding to do work...")
            item = work_queue.pop()
            print("Consumer consumed item:", str(item))
            #We must notify in case the producer is sleeping
            condition.notify()
            #We must give back the condiition
            condition.release()
            sleep(random.random()/10)

print("Producer - Consumer single threads example without Queue starting with:")
print("Work Queue Size:", str(max_queue_size))
print("Sleeping for 2 sec, then proceeding.  CTRL+C to kill.")
sleep(2)


#lets create a few new objects to use
prod = Producer()
con = Consumer()


#Call start which will start the thread activity, automatically invoking our
#run method.  You can start them in either order.
prod.start()
con.start()
