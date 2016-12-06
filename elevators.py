from __future__ import print_function
import collections
import uuid

class Building(object):
    def __init__(self, num_floors=4, num_elevators=2):
        self.floors = []
        self.elevators = []

        for _ in range(num_floors):
            self.add_floor()

        for i in range(num_elevators):
            self.add_elevator(i)

        self.add_elevator(2, current_floor=2)


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
        self.elevators.append(Elevator(id, self.get_num_floors(), current_floor=current_floor))


class Floor(object):
    def __init__(self):
        self._num_passengers_going_up = 0
        self._num_passengers_going_down = 0

    @property
    def num_passengers_going_up(self):
        return self._num_passengers_going_up

    @property
    def num_passengers_going_down(self):
        return self._num_passengers_going_down

    def add_passengers(self, num, going_up=True):
        if going_up:
            self._num_passengers_going_up += num
        else:
            self._num_passengers_going_down += num

    def total_passengers(self):
        return self.num_passengers_going_up + self.num_passengers_going_down

class Elevator(object):
    ELEVATOR_CAPACITY = 10

    def __init__(self, id, num_floors, current_floor=1):
        self.id = id
        self.current_floor = current_floor
        self.capacity = Elevator.ELEVATOR_CAPACITY
        self.dest_queue = collections.deque()
        self.num_passengers_to_floor = []
        self.next_dest = None

        for _ in range(num_floors):
            self.add_floor_button()

    def get_num_passengers_total(self):
        sum(self.num_passengers_to_floor)

    def add_floor_button(self):
        self.num_passengers_to_floor.append(0)

    def remove_floor_button(self):
        self.num_passengers_to_floor.pop()

    def is_on_floor(self, floor_num):
        return self.current_floor == floor_num

    def cost_from_floor(self, floor_num):
        if floor_num - self.current_floor > 0:
            direction_needed = 1
        elif floor_num - self.current_floor < 0:
            direction_needed = -1
        else:
            direction_needed = 0

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


    def offload_passengers(self):
        pass

    def pick_up_passengers(self):
        pass

    def run_next(self):
        print("RUNNING ELEVATOR NUM {}".format(self.id))
        if not self.next_dest:
            if self.dest_queue:
                self.next_dest = self.dest_queue.popleft()

        if self.next_dest:
            if self.next_dest > self.current_floor:
                self.current_floor += 1
            elif self.next_dest < self.current_floor:
                self.current_floor -= 1
            else:
                self.offload_passengers()
                self.pick_up_passengers()

class Controller(object):
    def __init__(self, building):
        self.building = building
        self.ELEVATOR_HEIGHT = 4
        self.ELEVATOR_WIDTH = 4
        self.WIDTH_BETWEEN_ELEVATORS = 2
        self.UP_PASSENGER = u'\u2191'
        self.DOWN_PASSENGER = u'\u2193'

    def get_floor_width(self):
        num_elevators = len(self.building.elevators)
        return (self.WIDTH_BETWEEN_ELEVATORS + self.ELEVATOR_WIDTH) * num_elevators + self.WIDTH_BETWEEN_ELEVATORS

    def render_floor(self, floor, elevator_indices, floor_num):
        num_elevators = len(self.building.elevators)

        # Print top line of floor
        for i in range(num_elevators):
            if i in elevator_indices:
                print(" " * self.WIDTH_BETWEEN_ELEVATORS, end="")
                print("_" * self.ELEVATOR_WIDTH, end="")
            else:
                print(" " * self.WIDTH_BETWEEN_ELEVATORS, end="")
                print(" " * self.ELEVATOR_WIDTH, end="")

        print(" " * self.WIDTH_BETWEEN_ELEVATORS, end="")
        print("\n", end="")

        # Print the sides of the elevator
        for _ in range(self.ELEVATOR_HEIGHT):
            for i in range(num_elevators):
                if i in elevator_indices:
                    print(" " * self.WIDTH_BETWEEN_ELEVATORS, end="")
                    print("|", end="")
                    print(" " * (self.ELEVATOR_WIDTH - 2), end="")
                    print("|", end="")
                else:
                    print(" " * self.WIDTH_BETWEEN_ELEVATORS, end="")
                    print(" " * self.ELEVATOR_WIDTH, end="")

            print(" " * self.WIDTH_BETWEEN_ELEVATORS, end="")
            print("\n", end="")

        # Print the passengers waiting on the floor
        print(self.UP_PASSENGER * floor.num_passengers_going_up, end="")
        print(self.DOWN_PASSENGER * floor.num_passengers_going_down, end="")
        print("")

        print("_" * self.get_floor_width() + " Floor: {}".format(floor_num))


    def render(self):
        for index, floor in enumerate(self.building.floors[::-1]):
            floor_num = self.building.get_num_floors() - index
            elevator_indices = [elevator_i for elevator_i, elevator in enumerate(self.building.elevators) if elevator.is_on_floor(floor_num)]
            self.render_floor(floor, elevator_indices, floor_num)


    def add_new_passengers(self):
        floor_num = int(raw_input("Which floor? ({} - {}) ".format(1, self.building.get_num_floors())))
        num_passengers = int(raw_input("How many passengers? (1 - 9) "))
        direction = raw_input("Are they going going up or down? (u or d) ")

        if direction == 'u':
            self.building.floors[floor_num - 1].add_passengers(num_passengers, going_up=True)
        else:
            self.building.floors[floor_num - 1].add_passengers(num_passengers, going_up=False)

        self.render()
        self.assign_elevator_to_passengers(floor_num)

    def run_elevators(self):
        print("RUNNING ELEVATORS")
        for elevator in self.building.elevators:
            elevator.run_next()

    def process_new_passengers(self):
        # Get num of passengers on each floor
        count = 1
        while True:
            choice = raw_input("Round {}. Would you like to add prospective passengers to a specific floor? (y or n) ".format(count))

            if choice == 'y':
                self.add_new_passengers()

            self.run_elevators()
            self.render()
            count += 1

    def assign_elevator_to_passengers(self, floor_num):
        # Find elevator of lowest cost
        cheapest_elevator = min(self.building.elevators, key=lambda e: e.cost_from_floor(floor_num))
        print("CHEAPEST: {}".format(cheapest_elevator.id))
        cheapest_elevator.add_dest(floor_num)


def main():
    # num_floors = int(raw_input("Hello! How many floors would you like in your building? (2 - 10): "))
    # num_elevators = int(raw_input("Hello! How many elevators would you like in your building? (2 - 4): "))
    # building = Building(num_floors=num_floors, num_elevators=num_elevators)

    building = Building()
    controller = Controller(building)

    # print "Great, we are going to have {} floors and {} elevators in this building".format(num_floors, num_floors)

    controller.render()

    while True:
        controller.process_new_passengers()

if __name__ == "__main__":
    main()