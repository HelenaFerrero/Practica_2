"""
Solution to the one-way tunnel
"""
import time
import random
from multiprocessing import Lock, Condition, Process
from multiprocessing import Value

SOUTH = 1
NORTH = 0

NCARS = 5
NPED = 10
TIME_CARS_NORTH = 0.5  # a new car enters each 0.5s
TIME_CARS_SOUTH = 0.5  # a new car enters each 0.5s
TIME_PED = 5 # a new pedestrian enters each 5s
TIME_IN_BRIDGE_CARS = (1, 0.5) # normal 1s, 0.5s
TIME_IN_BRIDGE_PEDESTRIAN = (30, 10) # normal 1s, 0.5s

class Monitor():
    def __init__(self):
        self.mutex = Lock()
        self.carsnorth = Value('i', 0)
        self.carssouth = Value('i', 0)
        self.peds = Value('i', 0)
        self.carsnorth_waiting = Value('i',0)
        self.carssouth_waiting = Value('i',0)
        self.peds_waiting = Value('i',0)
        self.turn = Value('i',0)
        #turn 0 for carsnorth
        #turn 1 for carssouth
        #turn 2 for pedestrians
        self.no_carssouth = Condition(self.mutex)
        self.no_carsnorth = Condition(self.mutex)
        self.no_peds = Condition(self.mutex)
        
    def are_no_carsnorth(self):
        return self.carsnorth.value == 0 and \
            (self.turn.value == 1 or self.turn.value == 2 or \
             self.carsnorth_waiting.value == 0)
    
    def are_no_carssouth(self):
        return self.carssouth.value == 0 and \
            (self.turn.value == 0 or self.turn.value == 2 or \
             self.carssouth_waiting.value == 0)
    
    def are_no_peds(self):
        return self.peds.value == 0 and \
            (self.turn.value == 0 or self.turn.value == 1 or \
             self.peds_waiting.value == 0)
            
    def wants_enter_car(self, direction: int) -> None:
        self.mutex.acquire()
        if direction == 0:
            self.carsnorth_waiting.value += 1
            self.no_carssouth.wait_for(self.are_no_carssouth)
            self.no_peds.wait_for(self.are_no_peds)
            self.carsnorth_waiting.value -= 1
            self.carsnorth.value += 1
        else:
            self.carssouth_waiting.value += 1
            self.no_carsnorth.wait_for(self.are_no_carsnorth)
            self.no_peds.wait_for(self.are_no_peds)
            self.carssouth_waiting.value -= 1
            self.carssouth.value += 1
        self.mutex.release()

    def leaves_car(self, direction: int) -> None:            
        self.mutex.acquire() 
        if direction == 0:
            self.carsnorth.value -= 1
            self.turn = 1
            if self.carsnorth.value == 0:
                self.no_carsnorth.notify()
                self.no_carssouth.notify()
                self.no_peds.notify()
        else:
            self.carssouth.value -= 1
            self.turn = 2
            if self.carssouth.value == 0:
                self.no_carssouth.notify()
                self.no_peds.notify()
                self.no_carsnorth.notify()
        self.mutex.release()

    def wants_enter_pedestrian(self) -> None:
        self.mutex.acquire()
        self.peds_waiting.value += 1
        self.no_carsnorth.wait_for(self.are_no_carsnorth)
        self.no_carssouth.wait_for(self.are_no_carssouth)
        self.peds_waiting.value -= 1
        self.peds.value += 1
        self.mutex.release()

    def leaves_pedestrian(self) -> None:
        self.mutex.acquire()
        self.peds.value -= 1
        self.turn = 0
        if self.peds.value == 0:
                self.no_peds.notify()
                self.no_carsnorth.notify()
                self.no_carssouth.notify()
        self.mutex.release()

    def __repr__(self) -> str:
        return f'Monitor: {self.carsnorth.value, self.carssouth.value, self.peds.value}'

def delay_car_north() -> None:
    time.sleep(TIME_IN_BRIDGE_CARS[random.randint(0,1)])

def delay_car_south() -> None:
    time.sleep(TIME_IN_BRIDGE_CARS[random.randint(0,1)])

def delay_pedestrian() -> None:
    time.sleep(TIME_IN_BRIDGE_PEDESTRIAN[random.randint(0,1)])

def car(cid: int, direction: int, monitor: Monitor)  -> None:
    print(f"car {cid} heading {direction} wants to enter. {monitor}")
    monitor.wants_enter_car(direction)
    print(f"car {cid} heading {direction} enters the bridge. {monitor}")
    if direction==NORTH :
        delay_car_north()
    else:
        delay_car_south()
    print(f"car {cid} heading {direction} leaving the bridge. {monitor}")
    monitor.leaves_car(direction)
    print(f"car {cid} heading {direction} out of the bridge. {monitor}")

def pedestrian(pid: int, monitor: Monitor) -> None:
    print(f"pedestrian {pid} wants to enter. {monitor}")
    monitor.wants_enter_pedestrian()
    print(f"pedestrian {pid} enters the bridge. {monitor}")
    delay_pedestrian()
    print(f"pedestrian {pid} leaving the bridge. {monitor}")
    monitor.leaves_pedestrian()
    print(f"pedestrian {pid} out of the bridge. {monitor}")



def gen_pedestrian(monitor: Monitor) -> None:
    pid = 0
    plst = []
    for _ in range(NPED):
        pid += 1
        p = Process(target=pedestrian, args=(pid, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1/TIME_PED))

    for p in plst:
        p.join()

def gen_cars(direction: int, time_cars, monitor: Monitor) -> None:
    cid = 0
    plst = []
    for _ in range(NCARS):
        cid += 1
        p = Process(target=car, args=(cid, direction, monitor))
        p.start()
        plst.append(p)
        time.sleep(random.expovariate(1/time_cars))

    for p in plst:
        p.join()

def main():
    monitor = Monitor()
    gcars_north = Process(target=gen_cars, args=(NORTH, TIME_CARS_NORTH, monitor))
    gcars_south = Process(target=gen_cars, args=(SOUTH, TIME_CARS_SOUTH, monitor))
    gped = Process(target=gen_pedestrian, args=(monitor,))
    gcars_north.start()
    gcars_south.start()
    gped.start()
    gcars_north.join()
    gcars_south.join()
    gped.join()


if __name__ == '__main__':
    main()

