import sys
import os

# Append the project root directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from behave import given, when, then
from gauge import GaugeStepper
from unittest.mock import Mock

@given('a GaugeStepper with a range from {min_val:d} to {max_val:d}')
def step_given_gauge_stepper(context, min_val, max_val):
	context.mock_motor = Mock()
	context.gauge = GaugeStepper("TestGauge", min_val, max_val, 1, context.mock_motor)
	print(f"GaugeStepper created with range: {min_val} to {max_val}")

@when('I move the gauge to {value:d}')
def step_when_move_gauge(context, value):
	print(f"Moving gauge to: {value}")
	context.gauge.move_to(value)

@then('the gauge position should be {expected_pos:d}')
def step_then_gauge_position(context, expected_pos):
	actual_pos = context.gauge.get_pos()
	print(f"Expected gauge position: {expected_pos}, Actual gauge position: {actual_pos}")
	assert actual_pos == expected_pos, f"Expected gauge position: {expected_pos}, Actual gauge position: {actual_pos}"

@then('the motor should have moved 50 steps')
def step_impl_motor_moved_50_steps(context):
	context.mock_motor.move.assert_any_call(1, 50.0)

@when('I calibrate the gauge')
def step_impl_calibrate_gauge(context):
	context.gauge.calibrate()

@then('the motor should return to the start position')
def step_impl_motor_return_start(context):
	context.mock_motor.move.assert_any_call(1, 0)

@then('the gauge should be calibrated')
def step_impl_gauge_calibrated(context):
	assert context.gauge.is_calibrated()