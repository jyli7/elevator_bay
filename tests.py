import unittest
from classes import Building, Elevator, Floor

class TestElevatorMethods(unittest.TestCase):
    def setUp(self):
        self.building = Building(10)
        self.elevator = self.building.elevators[0]
        self.elevator.current_floor = 3

    def test_cost_from_floor(self):
        # Stationary elevator
        self.assertEqual(self.elevator.cost_from_floor(2, self.elevator.current_floor, self.elevator.dest_queue), 1)
        self.assertEqual(self.elevator.cost_from_floor(4, self.elevator.current_floor, self.elevator.dest_queue), 1)

        # Elevator with one item in queue
        self.elevator.dest_queue = [1]

        self.assertEqual(self.elevator.cost_from_floor(2, self.elevator.current_floor, self.elevator.dest_queue), 1)
        self.assertEqual(self.elevator.cost_from_floor(4, self.elevator.current_floor, self.elevator.dest_queue), 5)

        self.elevator.dest_queue = [6, 8, 4, 7]

        self.assertEqual(self.elevator.cost_from_floor(2, self.elevator.current_floor, self.elevator.dest_queue), 17)
        self.assertEqual(self.elevator.cost_from_floor(7, self.elevator.current_floor, self.elevator.dest_queue), 4)

    def test_unload(self):
        self.elevator.add_passengers_traveling_to(4, 4)
        self.elevator.unload()
        self.assertEqual(self.elevator.get_num_passengers_traveling_to(4), 4)

        self.elevator.current_floor += 1
        self.elevator.unload()
        self.assertEqual(self.elevator.get_num_passengers_traveling_to(4), 0)

if __name__ == '__main__':
    unittest.main()