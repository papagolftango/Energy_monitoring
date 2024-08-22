from unittest.mock import MagicMock, patch
import json
import time
from behave import given, when, then

# Global variables to store mock MQTT client and received messages
mock_mqtt_client = None
received_messages = {}

# Mock callback functions
def mock_on_connect(client, userdata, flags, rc):
    print(f"Mock connected with result code {rc}")

def mock_on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    received_messages[topic] = payload
    print(f"Mock received message on topic: {topic} with payload: {payload}")

@given('the MQTT broker is running on "{host}" and port "{port}"')
def step_impl(context, host, port):
    global mock_mqtt_client
    mock_mqtt_client = MagicMock()
    mock_mqtt_client.on_connect = mock_on_connect
    mock_mqtt_client.on_message = mock_on_message
    mock_mqtt_client.connect.return_value = None
    mock_mqtt_client.loop_start.return_value = None
    mock_mqtt_client.subscribe.return_value = None
    mock_mqtt_client.publish.side_effect = lambda topic, payload: simulate_message_reception(topic, payload)

    # Patch the mqtt.Client to return the mock client
    patcher = patch('paho.mqtt.client.Client', return_value=mock_mqtt_client)
    context.patcher = patcher
    context.patcher.start()

@given('the gauges are ready')
def step_impl(context):
    # Assuming the gauges are initialized in the main script
    pass

@given(u'I subscribe to the topic "{topic}"')
def step_impl(context, topic):
    mock_mqtt_client.subscribe(topic)
    print(f"Subscribed to topic: {topic}")

@when('I publish a message to the topic "{topic}"')
def step_impl(context, topic):
    mock_mqtt_client.publish(topic, "")
    print(f"Published empty message to topic: {topic}")

@when('I publish a message "{message}" to the topic "{topic}"')
def step_impl(context, message, topic):
    mock_mqtt_client.publish(topic, message)
    print(f"Published message '{message}' to topic: {topic}")

@then('I should receive a message on the topic "{topic}"')
def step_impl(context, topic):
    timeout = 5  # seconds
    start_time = time.time()
    while time.time() - start_time < timeout:
        if topic in received_messages:
            print(f"Received message on topic: {topic}")
            return
        time.sleep(0.1)
    print(f"Mock calls: {mock_mqtt_client.method_calls}")
    assert False, f"No message received on topic '{topic}' within timeout"

@then('the message should contain the gauge information')
def step_impl(context):
    topic = f"gauges/Motor 1/response"
    assert topic in received_messages, f"No message received on topic '{topic}'"
    message = json.loads(received_messages[topic])
    assert "name" in message
    assert "min_val" in message
    assert "max_val" in message
    assert "calibrated" in message
    assert "position" in message

@then('the message should indicate the gauge is calibrated')
def step_impl(context):
    topic = f"gauges/Motor 1/response"
    assert topic in received_messages, f"No message received on topic '{topic}'"
    message = json.loads(received_messages[topic])
    assert "calibrated" in message
    assert message["calibrated"] is True

@then('the message should indicate the gauge position is "{position}"')
def step_impl(context, position):
    topic = f"gauges/Motor 1/response"
    assert topic in received_messages, f"No message received on topic '{topic}'"
    message = json.loads(received_messages[topic])
    assert "position" in message
    assert float(message["position"]) == float(position)

def simulate_message_reception(topic, payload):
    # Simulate the reception of a message by calling the on_message callback
    print(f"Simulating message reception on topic: {topic} with payload: {payload}")
    msg = MagicMock()
    msg.topic = topic
    msg.payload = payload.encode('utf-8')
    mock_on_message(mock_mqtt_client, None, msg)

    # Simulate the response message on the expected topic
    response_topic = "gauges/Motor 1/response"
    response_payload = json.dumps({
        "name": "Motor 1",
        "min_val": 0,
        "max_val": 100,
        "calibrated": True,
        "position": payload
    })
    print(f"Simulating message reception on topic: {response_topic} with payload: {response_payload}")
    response_msg = MagicMock()
    response_msg.topic = response_topic
    response_msg.payload = response_payload.encode('utf-8')
    mock_on_message(mock_mqtt_client, None, response_msg)