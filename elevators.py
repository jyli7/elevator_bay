from __future__ import print_function
from classes import Building, Floor, Elevator

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


    def add_new_passengers(self, floor_num):
        num_passengers = int(raw_input("How many passengers? (1 - 9) "))
        direction = raw_input("Are they going going up or down? (u or d) ")

        if direction == 'u':
            self.building.floors[floor_num - 1].add_passengers(num_passengers, going_up=True)
        else:
            self.building.floors[floor_num - 1].add_passengers(num_passengers, going_up=False)

        self.render()
        self.assign_elevator_to_passengers(floor_num)

    def run_elevators(self):
        for elevator in self.building.elevators:
            elevator.move_to_next_floor()
            if elevator.on_a_dest_floor():
                elevator.open_doors()
                floor_obj = self.building.get_floor_obj_from_num(elevator.current_floor)
                if (floor_obj.get_total_passengers() > 0):
                    dest_floor = int(raw_input(
                        "Elevator {} has reached floor {}. Picking up {} passengers. To what floor would these passengers like to go?".format(
                            elevator.id, elevator.current_floor, floor_obj.get_total_passengers()
                        )))
                    elevator.load(floor_obj.get_total_passengers, dest_floor)
                    floor_obj.clear_floor()

            print("Elevator {} with next_dest {}, queue {}".format(elevator.id, elevator.next_dest, elevator.dest_queue))

    def process_new_passengers(self):
        # Get num of passengers on each floor
        count = 1
        while True:
            floor_num = int(raw_input("Round {}. To which floor would you like to add new passengers? (0 to skip) ".format(count)))
            if floor_num > 0:
                self.add_new_passengers(floor_num)

            self.run_elevators()
            self.render()
            count += 1

    def assign_elevator_to_passengers(self, floor_num):
        # Find elevator of lowest cost
        cheapest_elevator = min(self.building.elevators, key=lambda e: e.cost_from_floor(floor_num))
        print("CHEAPEST: {}".format(cheapest_elevator.id))
        cheapest_elevator.add_dest(floor_num)

    def ask_for_passenger_dest(self, elevator_id, current_floor, num_passengers):
        return

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