from __future__ import print_function
import collections
import uuid

class Building(object):
    def __init__(self, num_floors=4, num_elevators=2):
        self.floors = []
        self.elevators = []

        for _ in range(num_floors):
            self.add_floor()

        for _ in range(num_elevators):
            self.add_elevator()

    def get_num_floors(self):
        return len(self.floors);

    def add_floor(self):
        self.floors.append(Floor())
        for elevator in self.elevators:
            elevator.add_floor_button()

    def remove_floor(self):
        self.floors.pop()
        for elevator in self.elevators:
            elevator.add_floor_button()

    def add_elevator(self):
        self.elevators.append(Elevator(self.get_num_floors()))


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

    def add_passengers_up(self, num):
        self._num_passengers_going_up += num

    def add_passengers_down(self, num):
        self._num_passengers_going_down += num

    def total_passengers(self):
        return self.num_passengers_going_up + self.num_passengers_going_down

class Elevator(object):
    ELEVATOR_CAPACITY = 10

    def __init__(self, num_floors):
        self.current_floor = 1
        self.capacity = Elevator.ELEVATOR_CAPACITY
        self.dest_queue = collections.deque
        self.num_passengers_to_floor = []

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


class View(object):
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

    def ask_for_input(self):
        # Get num of passengers on each floor
        for index, floor in enumerate(self.building.floors):
            print("\n")
            if index != len(self.building.floors) - 1:
                new_num_going_up = int(input("Floor {}: There are {} passengers going UP here. How many new passengers going up? ".format(index + 1, floor.num_passengers_going_up)))
                floor.add_passengers_up(new_num_going_up)
                self.render()
                print("Great, there are now {} passengers waiting to go up on floor {}".format(floor.num_passengers_going_up, index + 1))

            if index > 0:
                new_num_going_down = int(input("Floor {}: There are {} passengers going DOWN here. How many new passengers going down? ".format(index + 1, floor.num_passengers_going_down)))
                floor.add_passengers_down(new_num_going_down)
                self.render()
                print("Great, there are now {} passengers waiting to go down on floor {}".format(floor.num_passengers_going_down, index + 1))

        # occupied_elevators = [elevator for elevator in self.building.elevators if elevator.get_num_passengers_total > 0]
        # # For any elevators that have passengers in them, have those passengers press buttons
        # for index, elevator in enumerate(self.building.elevators):
        #     if elevator.get_num_passengers_total() > 0:
        #         int(input("Elevator {}: There are {} passengers here.".format(index + 1, elevator.get_num_passengers_total()))


def main():
    # num_floors = int(input("Hello! How many floors would you like in your building? (2 - 10): "))
    # num_elevators = int(input("Hello! How many elevators would you like in your building? (2 - 4): "))
    # building = Building(num_floors=num_floors, num_elevators=num_elevators)

    building = Building()
    view = View(building)

    # print "Great, we are going to have {} floors and {} elevators in this building".format(num_floors, num_floors)

    view.render()

    while True:
        view.ask_for_input()
        view.render()


if __name__ == "__main__":
    main()