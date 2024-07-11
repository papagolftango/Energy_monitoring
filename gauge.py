import time
from motor import Motor

class GaugeStepper:
    def __init__(self, name, min_val, max_val, step_size, motor):
        self.name = name
        self.min_val = min_val
        self.max_val = max_val
        self.step_size = step_size
        self.motor = motor
        self.current_pos = min_val
        self.calibrated = False

    def move_to(self, value):
        if value < self.min_val:
            value = self.min_val
        elif value > self.max_val:
            value = self.max_val
        
        steps = (value - self.current_pos) / self.step_size
        self.motor.move(1, steps)
        self.current_pos = value
        
        steps = (value - self.current_pos) / self.step_size
        self.motor.move(1, steps)
        self.current_pos = value

    def get_pos(self):
        return self.current_pos

    def calibrate(self):
        self.motor.move(1, 0)
        self.calibrated = True

    def is_calibrated(self):
        return self.calibrated


import unittest
from gauge import GaugeStepper

class MockMotor:
    def __init__(self):
        self.moves = []

    def move(self, id, steps):
        self.moves.append((id, steps))

class TestGaugeStepper(unittest.TestCase):
    def setUp(self):
        self.mock_motor = MockMotor()
        self.gauge = GaugeStepper("TestGauge", 0, 100, 1, self.mock_motor)

    def test_move_to_within_range(self):
        self.gauge.move_to(50)
        self.assertEqual(self.gauge.get_pos(), 50)
        self.assertEqual(len(self.mock_motor.moves), 1)
        self.assertEqual(self.mock_motor.moves[0], (1, 50))

    def test_move_to_above_max(self):
        self.gauge.move_to(150)
        self.assertEqual(self.gauge.get_pos(), self.gauge.max_val)

    def test_calibration(self):
        self.gauge.calibrate()
        expected_scale = self.gauge._GaugeStepper__max_step / (self.gauge.max_val - self.gauge.min_val)
        self.assertEqual(self.mock_motor.moves[-1], (1, 0))  # Check if motor returned to start
        self.assertTrue(self.gauge._GaugeStepper__calibrated)

if __name__ == '__main__':
    unittest.main()


import unittest
from gauge import GaugeStepper

class MockMotor:
    def __init__(self):
        self.moves = []

    def move(self, id, steps):
        self.moves.append((id, steps))

class TestGaugeStepper(unittest.TestCase):
    def setUp(self):
        self.mock_motor = MockMotor()
        self.gauge = GaugeStepper("TestGauge", 0, 100, 1, self.mock_motor)

    def test_move_to_within_range(self):
        self.gauge.move_to(50)
        self.assertEqual(self.gauge.get_pos(), 50)
        self.assertEqual(len(self.mock_motor.moves), 1)
        self.assertEqual(self.mock_motor.moves[0], (1, 50))

    def test_move_to_above_max(self):
        self.gauge.move_to(150)
        self.assertEqual(self.gauge.get_pos(), self.gauge.max_val)

    def test_calibration(self):
        self.gauge.calibrate()
        expected_scale = self.gauge._GaugeStepper__max_step / (self.gauge.max_val - self.gauge.min_val)
        self.assertEqual(self.mock_motor.moves[-1], (1, 0))  # Check if motor returned to start
        self.assertTrue(self.gauge._GaugeStepper__calibrated)

if __name__ == '__main__':
    unittest.main()

import unittest
from gauge import GaugeStepper

class MockMotor:
    def __init__(self):
        self.moves = []

    def move(self, id, steps):
        self.moves.append((id, steps))

class TestGaugeStepper(unittest.TestCase):
    def setUp(self):
        self.mock_motor = MockMotor()
        self.gauge = GaugeStepper("TestGauge", 0, 100, 1, self.mock_motor)

    def test_move_to_within_range(self):
        self.gauge.move_to(50)
        self.assertEqual(self.gauge.get_pos(), 50)
        self.assertEqual(len(self.mock_motor.moves), 1)
        self.assertEqual(self.mock_motor.moves[0], (1, 50))

    def test_move_to_above_max(self):
        self.gauge.move_to(150)
        self.assertEqual(self.gauge.get_pos(), self.gauge.max_val)

    def test_calibration(self):
        self.gauge.calibrate()
        expected_scale = self.gauge._GaugeStepper__max_step / (self.gauge.max_val - self.gauge.min_val)
        self.assertEqual(self.mock_motor.moves[-1], (1, 0))  # Check if motor returned to start
        self.assertTrue(self.gauge._GaugeStepper__calibrated)

if __name__ == '__main__':
    unittest.main()