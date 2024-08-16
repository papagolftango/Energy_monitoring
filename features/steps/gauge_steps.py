from behave import given, when, then
from gauge import GaugeStepper
from unittest.mock import Mock


@given('the gauge is initialized')
def step_given_gauge_initialized(context):
    context.motor = Mock(spec=Motor)  # Create a mocked instance of Motor
    context.motor.get_position.return_value = 0  # Set the return value of get_position to 0
    context.gauge = GaugeStepper(context.motor, "Motor1", 1, 0, 100)

@given('the gauge is at position {position:d}')
def step_given_gauge_at_position(context, position):
    if not hasattr(context, 'gauge'):
        context.motor = Mock(spec=Motor)  # Create a mocked instance of Motor
        context.motor.get_position.return_value = position  # Set the return value of get_position
        context.gauge = GaugeStepper(context.motor, "Motor1", 1, 0, 100)
    context.gauge.move_to(position)

@given('the motor is initialized')
def step_given_motor_initialized(context):
    if not hasattr(context, 'gauge'):
        context.motor = Mock(spec=Motor)  # Create a mocked instance of Motor
        context.motor.get_position.return_value = 0  # Set the return value of get_position to 0
        context.gauge = GaugeStepper(context.motor, "Motor1", 1, 0, 100)
    context.motor = context.gauge.motor  # Assuming motor control is part of the gauge

@when('the gauge is calibrated')
def step_when_gauge_calibrated(context):
    context.gauge.calibrate()

@when('I move the gauge to position {position:d}')
def step_when_move_gauge_to_position(context, position):
    context.gauge.move_to(position)

@then(u'the gauge should be calibrated')
def step_impl(context):
    # Check if the gauge is calibrated
    assert context.gauge.calibrated, "Gauge is not calibrated"

    # Check if the gauge's position is at the minimum value
    assert context.gauge.position == context.gauge.min_val, (
        f"Gauge position is {context.gauge.position}, expected {context.gauge.min_val}"
    )