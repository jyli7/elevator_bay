import unittest
from classes import Building, Elevator, Floor

class TestElevatorMethods(unittest.TestCase):
    def setUp(self):
        self.building = Building()
        self.elevator = self.building.elevators[0]
        self.elevator.current_floor = 3

    def test_cost_from_floor(self):
        # Stationary self.evator
        self.assertEqual(self.elevator.cost_from_floor(2), 1)
        self.assertEqual(self.elevator.cost_from_floor(4), 1)

        # Moving self.elevator
        self.elevator.next_dest = 2

        # In same direction
        self.assertEqual(self.elevator.cost_from_floor(2), 1)

        # In opposite direction
        self.assertEqual(self.elevator.cost_from_floor(4), 3)

    def test_unload(self):
        self.elevator.add_passengers_traveling_to(4, 4)
        self.elevator.unload()
        self.assertEqual(self.elevator.get_num_passengers_traveling_to(4), 4)

        self.elevator.current_floor += 1
        self.elevator.unload()
        self.assertEqual(self.elevator.get_num_passengers_traveling_to(4), 0)

    def test_pickup_passengers(self):
        third_floor_obj = self.building.get_floor_obj_from_num(3)

        self.assertEqual(self.elevator.get_num_passengers_total(), 0)

        third_floor_obj.add_passengers(5, True)
        self.elevator.pick_up_passengers()
        self.assertEqual(self.elevator.get_num_passengers_total(), 5)

if __name__ == '__main__':
    unittest.main()