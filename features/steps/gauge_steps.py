from behave import given, when, then
from unittest.mock import Mock
from mock_motor import MockMotor
from gauge import Gauge  # Import the Gauge class from the gauge module
 

@given('the gauges are initialized with the following parameters')
def step_impl(context):
    context.gauges = {}
    for row in context.table:
        motor_id = int(row['motor_id'])
        min_val = float(row['min_val'])
        max_val = float(row['max_val'])
        context.gauges[motor_id] = Gauge(motor=MockMotor(), motor_name=f"TestMotor{motor_id}", motor_id=motor_id, min_val=min_val, max_val=max_val)

@given('the gauge is initialized with motor ID {motor_id:d} and min value {min_val:f} and max value {max_val:f}')
def step_impl(context, motor_id, min_val, max_val):
    context.gauge = Gauge(motor=MockMotor(), motor_name=f"TestMotor{motor_id}", motor_id=motor_id, min_val=min_val, max_val=max_val)

@given('the gauge is initialized')
def step_impl(context):
    motor_id = "test"
    motorName = "1"
    min_val = 0
    max_val = 1000
    mock_motor = MockMotor()  # Mock the Motor class
 #   mock_motor.get_position.return_value = 0  # Ensure it returns an
    context.gauge = Gauge(mock_motor, motorName, motor_id, min_val, max_val)

@given('the gauge is calibrated')
def step_impl(context):
    motor_id = "test"
    motorName = "1"
    min_val = 0
    max_val = 1000
    mock_motor = MockMotor()  # Mock the Motor class
    context.gauge = Gauge(mock_motor, motorName, motor_id, min_val, max_val)
    context.gauge.calibrate()
    assert context.gauge.is_calibrated()

@when('the gauges are moved to the following positions')
def step_impl(context):
    for row in context.table:
        motor_id = int(row['motor_id'])
        move_to = float(row['move_to'])
        context.gauges[motor_id].move_to(move_to)

@when('the gauge is moved to {value:f}')
def step_impl(context, value):
    context.gauge.move_to(value)

@when('the gauge is calibrated')
def step_impl(context):
    context.gauge.calibrate()

@when('the gauge is moved to {value:d}')
def step_impl(context, value):
    context.gauge.move_to(value)

@then('the gauge should read {value:d}')
def step_impl(context, value):
    print(context.gauge.get_position(),value)
    assert context.gauge.get_position() == value

@then('the gauge should read its maximum value')
def step_impl(context):
    print(context.gauge.get_position(),context.gauge.max_value())
    assert context.gauge.get_position() == context.gauge.max_value()

@then('the gauge should read its minimum value')
def step_impl(context):
    print(context.gauge.get_position(),context.gauge.min_value())
    assert context.gauge.get_position() == context.gauge.min_value()

@then('the gauge should read {value:f}')
def step_impl(context, value):
    assert context.gauge.get_position() == value

@then('the gauges should read the following values')
def step_impl(context):
    for row in context.table:
        motor_id = int(row['motor_id'])
        expected_value = float(row['expected_value'])
        actual_value = context.gauges[motor_id].get_position()
        assert actual_value == expected_value, f"Motor {motor_id}: Expected {expected_value}, but got {actual_value}"

@then('the gauge should be calibrated')
def step_impl(context):
    assert context.gauge.is_calibrated()

