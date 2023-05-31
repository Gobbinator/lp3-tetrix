#! /usr/bin/env python3
#a test and prototype for implementing a fixed tickrate
from threading import Thread, Lock, Semaphore
from time import sleep, time
import datetime as dt

tick_wait = Semaphore()

def tick():
    while True:
        sleep(0.2)
        tick_wait.release()

tick_thread = Thread(target=tick)

def coreloop():
    time_last = time()
    while True:
        #----------------------------------------  DEBUG: time meter
        #print(time())
        timedif = time() - time_last
        #print('timedif = ' + str(timedif))
        if str(timedif)[:5] != '0.200' and str(timedif)[:5] != '0.199':
            print(str(timedif)[:5])
        time_last = time()
        #<---------------------------------------> END DEBUG
        
        
        
        tick_wait.acquire() #always last statement; wait for next tick
    
core_thread = Thread(target=coreloop)

tick_thread.start()
core_thread.start()
