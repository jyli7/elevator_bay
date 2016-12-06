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
        self.num_passengers = 0
        self.up_button_on = False
        self.down_button_on = False


class Elevator(object):
    ELEVATOR_CAPACITY = 10

    def __init__(self, num_floors):
        self.current_floor = 1
        self.capacity = Elevator.ELEVATOR_CAPACITY
        self.dest_queue = collections.deque
        self.floor_buttons = []

        for _ in range(num_floors):
            self.add_floor_button()

    def add_floor_button(self):
        self.floor_buttons.append(False)

    def remove_floor_button(self):
        self.floor_buttons.pop()

    def is_on_floor(self, floor_num):
        return self.current_floor == floor_num


class View(object):
    def __init__(self, building):
        self.building = building
        self.ELEVATOR_HEIGHT = 4
        self.ELEVATOR_WIDTH = 4
        self.WIDTH_BETWEEN_ELEVATORS = 2

    def get_floor_width(self):
        num_elevators = len(self.building.elevators)
        return (self.WIDTH_BETWEEN_ELEVATORS + self.ELEVATOR_WIDTH) * num_elevators + self.WIDTH_BETWEEN_ELEVATORS

    def render_floor(self, elevator_indices, floor_num):
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

        print("_" * self.get_floor_width() + " Floor: {}".format(floor_num))


    def render(self):
        for index, floor in enumerate(self.building.floors[::-1]):
            floor_num = self.building.get_num_floors() - index
            elevator_indices = [elevator_i for elevator_i, elevator in enumerate(self.building.elevators) if elevator.is_on_floor(floor_num)]
            self.render_floor(elevator_indices, floor_num)


def main():
    # num_floors = int(input("Hello! How many floors would you like in your building? (2 - 10): "))
    # num_elevators = int(input("Hello! How many elevators would you like in your building? (2 - 4): "))
    # building = Building(num_floors=num_floors, num_elevators=num_elevators)

    building = Building()
    view = View(building)

    # print "Great, we are going to have {} floors and {} elevators in this building".format(num_floors, num_floors)

    view.render()

    # while True:
    #     ask_for_input()
    #     render_building()


if __name__ == "__main__":
    main()