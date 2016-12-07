import collections
import uuid

class Building(object):
    def __init__(self, num_floors=6, num_elevators=3):
        self.floors = []
        self.elevators = []

        for _ in range(num_floors):
            self.add_floor()

        for i in range(num_elevators):
            self.add_elevator(i)

    def get_num_floors(self):
        return len(self.floors)

    def add_floor(self):
        self.floors.append(Floor())
        for elevator in self.elevators:
            elevator.add_floor_button()

    def remove_floor(self):
        self.floors.pop()
        for elevator in self.elevators:
            elevator.add_floor_button()

    def add_elevator(self, id, current_floor=1):
        self.elevators.append(Elevator(self, id, self.get_num_floors(), current_floor=current_floor))

    def get_floor_obj_from_num(self, floor_num):
        return self.floors[floor_num - 1]


class Floor(object):
    def __init__(self):
        self.num_passengers_going_up = 0
        self.num_passengers_going_down = 0

    def add_passengers(self, num, going_up=True):
        if going_up:
            self.num_passengers_going_up += num
        else:
            self.num_passengers_going_down += num

    def get_total_passengers(self):
        return self.num_passengers_going_up + self.num_passengers_going_down

    def clear_floor(self):
        self.num_passengers_going_down = 0
        self.num_passengers_going_up = 0

class Elevator(object):
    ELEVATOR_CAPACITY = 10

    def __init__(self, building, id, num_floors, current_floor=1):
        self.id = id
        self.name = self.id + 1
        self.current_floor = current_floor
        self.capacity = Elevator.ELEVATOR_CAPACITY
        self.dest_queue = []
        self.num_passengers_to_floor = []
        self.building = building

        for _ in range(num_floors):
            self.add_floor_button()

    def get_num_passengers_total(self):
        return sum(self.num_passengers_to_floor)

    def add_floor_button(self):
        self.num_passengers_to_floor.append(0)

    def get_num_passengers_traveling_to(self, floor_num):
        return self.num_passengers_to_floor[floor_num - 1]

    def add_passengers_traveling_to(self, floor_num, num_passengers):
        self.num_passengers_to_floor[floor_num - 1] = num_passengers

    def remove_floor_button(self):
        self.num_passengers_to_floor.pop()

    def is_on_floor(self, floor_num):
        return self.current_floor == floor_num

    def next_dest(self):
        if self.dest_queue:
            return self.dest_queue[0]
        else:
            return None

    def cost_from_floor(self, desired_floor, current_floor, queue):
        if desired_floor == current_floor:
            return 0

        if queue:
            if desired_floor > current_floor and queue[0] >= desired_floor:
                return abs(desired_floor - current_floor)
            elif desired_floor < current_floor and queue[0] <= desired_floor:
                return abs(desired_floor - current_floor)
            else:
                return abs(queue[0] - current_floor) + self.cost_from_floor(desired_floor, queue[0], queue[1:])
        else:
            return abs(desired_floor - current_floor)

    def add_dest(self, floor_num):
        self.dest_queue.append(floor_num)

    def process_dest_floor(self):
        self.unload()
        self.dest_queue.pop(0)

    def unload(self):
        self.num_passengers_to_floor[self.current_floor - 1] = 0

    def load(self, num_passengers, dest_floor):
        self.dest_queue.append(dest_floor)
        self.add_passengers_traveling_to(dest_floor, num_passengers)

    def is_on_dest_floor(self):
        return self.current_floor in self.dest_queue

    def move_to_next_floor(self):
        '''Returns current floor'''
        if self.next_dest():
            if self.next_dest() > self.current_floor:
                self.current_floor += 1
            elif self.next_dest() < self.current_floor:
                self.current_floor -= 1
