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