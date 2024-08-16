from behave import given, when, then
from unittest.mock import Mock
from gauge import Gauge  # Replace 'your_module' with the actual module name where Gauge is defined
from mock_motor import MockMotor

@given('the gauge is initialized')
def step_impl(context):
    motor_id = "test"
    motorName = "1"
    min_val = 0
    max_val = 1000
    mock_motor = MockMotor()  # Mock the Motor class
 #   mock_motor.get_position.return_value = 0  # Ensure it returns an
    context.gauge = Gauge(mock_motor, motorName, motor_id, min_val, max_val)
 

@when('the gauge is calibrated')
def step_impl(context):
    context.gauge.calibrate()

@then('the gauge should be calibrated')
def step_impl(context):
    assert context.gauge.is_calibrated()

@given('the gauge is calibrated')
def step_impl(context):
    motor_id = "test"
    motorName = "1"
    min_val = 0
    max_val = 1000
    mock_motor = Mock()  # Mock the Motor class
    context.gauge = Gauge(mock_motor, motorName, motor_id, min_val, max_val)
    context.gauge.calibrate()
    assert context.gauge.is_calibrated()

@when('the gauge is moved to {value:d}')
def step_impl(context, value):
    context.gauge.move_to(value)

@then('the gauge should read {value:d}')
def step_impl(context, value):
    assert context.gauge.get_position() == value

@then('the gauge should read its maximum value')
def step_impl(context):
    assert context.gauge.get_position() == context.gauge.max_value()

@then('the gauge should read its minimum value')
def step_impl(context):
    assert context.gauge.get_position() == context.gauge.min_value()