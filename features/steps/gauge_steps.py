from behave import given, when, then
from unittest.mock import MagicMock, patch
from gauges import Gauges

# Mock pigpio
mock_pigpio = MagicMock()
mock_pigpio.wave_create = MagicMock()
mock_pigpio.wave_send_once = MagicMock()
mock_pigpio.wave_send_repeat = MagicMock()
mock_pigpio.wave_tx_busy = MagicMock()
mock_pigpio.wave_tx_stop = MagicMock()
mock_pigpio.wave_delete = MagicMock()

# Patch pigpio.pi to return the mock instance
patcher = patch('pigpio.pi', return_value=mock_pigpio)
patcher.start()

# Stop patching after tests
def after_all(context):
    patcher.stop()

@given('the gauges are initialized')
def step_impl(context):
    context.gauges = Gauges()

@when('all gauges are calibrated')
def step_impl(context):
    for motor in context.gauges.motor_config:
        motor_id = motor["motor_id"]
        context.gauges.calibrate(motor_id)

@then(u'all gauges should be calibrated')
def step_impl(context):
    all_calibrated = all(context.gauges.is_calibrated(motor["motor_id"]) for motor in context.gauges.motor_config)
    assert all_calibrated, "Not all gauges are calibrated"
     

@when('the gauge {gauge_id:d} is moved to {value:f}')
def step_impl(context, gauge_id, value):
    context.gauges.move_to(gauge_id, value)

@then('the gauge {gauge_id:d} should read {expected_value:f}')
def step_impl(context, gauge_id, expected_value):
    actual_value = context.gauges.get_position(gauge_id)
    assert actual_value == expected_value, f"Expected {expected_value}, but got {actual_value}"

@then('the gauge {gauge_id:d} should read its maximum value')
def step_impl(context, gauge_id):
    max_value = context.gauges.get_max_value(gauge_id)
    actual_value = context.gauges.get_position(gauge_id)
    assert actual_value == max_value, f"Expected {max_value}, but got {actual_value}"

@then('the gauge {gauge_id:d} should read its minimum value')
def step_impl(context, gauge_id):
    min_value = context.gauges.get_min_value(gauge_id)
    actual_value = context.gauges.get_position(gauge_id)
    assert actual_value == min_value, f"Expected {min_value}, but got {actual_value}"
    










@given('the gauge {gauge_id:d} has a max value of {max_val:f} and a min value of {min_val:f}')
def step_impl(context, gauge_id, max_val, min_val):
    context.gauges.set_max_value(gauge_id, max_val)
    context.gauges.set_min_value(gauge_id, min_val)
    assert context.gauges.get_max_value(gauge_id) == max_val, f"Expected max value {max_val}, but got {context.gauges.get_max_value(gauge_id)}"
    assert context.gauges.get_min_value(gauge_id) == min_val, f"Expected min value {min_val}, but got {context.gauges.get_min_value(gauge_id)}"

@when('I set the max value of gauge {gauge_id:d} to {max_val:f}')
def step_impl(context, gauge_id, max_val):
    context.gauges.set_max_value(gauge_id, max_val)

@when('I set the min value of gauge {gauge_id:d} to {min_val:f}')
def step_impl(context, gauge_id, min_val):
    context.gauges.set_min_value(gauge_id, min_val)

@then('the gauge {gauge_id:d} should have a max value of {max_val:f}')
def step_impl(context, gauge_id, max_val):
    assert context.gauges.get_max_value(gauge_id) == max_val, f"Expected max value {max_val}, but got {context.gauges.get_max_value(gauge_id)}"

@then('the gauge {gauge_id:d} should have a min value of {min_val:f}')
def step_impl(context, gauge_id, min_val):
    assert context.gauges.get_min_value(gauge_id) == min_val, f"Expected min value {min_val}, but got {context.gauges.get_min_value(gauge_id)}"

@when('I move the gauge {gauge_id:d} to {value:f}')
def step_impl(context, gauge_id, value):
    context.gauges.move_to(gauge_id, value)

@then('the gauge {gauge_id:d} should read {value:f}')
def step_impl(context, gauge_id, value):
    assert context.gauges.get_position(gauge_id) == value, f"Expected position {value}, but got {context.gauges.get_position(gauge_id)}"

@then('the gauge {gauge_id:d} should read its minimum value')
def step_impl(context, gauge_id):
    min_value = context.gauges.get_min_value(gauge_id)
    actual_value = context.gauges.get_position(gauge_id)
    assert actual_value == min_value, f"Expected {min_value}, but got {actual_value}"