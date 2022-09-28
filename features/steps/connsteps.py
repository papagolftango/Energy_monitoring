from behave import *


@given(u'the device is in operation')
def step_impl(context):
    return(True)


@when(u'its switched operation')
def step_impl(context) :
    return(True)   


@then(u'the LED lights')
def step_impl(context):
    return(True)

    
@when(u'its switched off')
def step_impl(context):
    return(False)


@then(u'the LED turns off')
def step_impl(context):
    return(True)