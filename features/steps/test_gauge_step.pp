import unittest
from unittest.mock import patch
from features.mock_motor import MockMotor

class TestGaugeSteps(unittest.TestCase):
    @patch('features.steps.gauge_steps.Motor', new=MockMotor)
    def test_perform_steps(self):
        max_steps = 2000
        self.assertEqual(max_steps, 1000)

if __name__ == '__main__':
    unittest.main()