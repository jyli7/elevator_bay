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
        self.current_floor = current_floor
        self.capacity = Elevator.ELEVATOR_CAPACITY
        self.dest_queue = collections.deque()
        self.num_passengers_to_floor = []
        self.next_dest = None
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

    def remove_passengers_traveling_to(self, floor_num):
        self.num_passengers_to_floor[floor_num - 1] = 0

    def remove_floor_button(self):
        self.num_passengers_to_floor.pop()

    def is_on_floor(self, floor_num):
        return self.current_floor == floor_num

    def cost_from_floor(self, floor_num):
        # What direction would the elevator need to go, to reach desired floor?
        if floor_num - self.current_floor > 0:
            direction_needed = 1
        elif floor_num - self.current_floor < 0:
            direction_needed = -1
        else:
            direction_needed = 0

        # What direction is the elevator currently going in?
        if not self.next_dest:
            current_direction_of_movement = 0
        elif self.next_dest < self.current_floor:
            current_direction_of_movement = -1
        else:
            current_direction_of_movement = 1

        if current_direction_of_movement == 0 or direction_needed == current_direction_of_movement:
            cost = abs(floor_num - self.current_floor)
        else:
            cost = abs(floor_num - self.current_floor) + 2 * abs(self.next_dest - self.current_floor)

        return cost

    def add_dest(self, floor_num):
        self.dest_queue.append(floor_num)

    def unload(self):
        self.remove_passengers_traveling_to(self.current_floor)

    def load(self, num_passengers, dest_floor):
            self.dest_queue.append(dest_floor)
            self.add_passengers_traveling_to(dest_floor, num_passengers)

    def on_a_dest_floor(self):
        return self.current_floor == self.next_dest or self.current_floor in self.dest_queue

    def open_doors(self):
        self.unload()

        if self.current_floor == self.next_dest:
            self.next_dest = None
            if self.dest_queue:
                self.next_dest = self.dest_queue.popleft()

        elif self.current_floor in self.dest_queue:
            self.dest_queue.remove(self.current_floor)

    def move_to_next_floor(self):
        '''Returns current floor'''
        # If we do not have a next_dest, set it
        if not self.next_dest:
            if self.dest_queue:
                self.next_dest = self.dest_queue.popleft()

        if self.next_dest:
            if self.next_dest > self.current_floor:
                self.current_floor += 1
            elif self.next_dest < self.current_floor:
                self.current_floor -= 1



