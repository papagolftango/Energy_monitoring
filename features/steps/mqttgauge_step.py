import paho.mqtt.client as mqtt
import time
from unittest.mock import MagicMock
from behave import given, when, then

# Global variables
mqtt_client = None
received_messages = {}

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print(f"[DEBUG] Connected with result code {rc}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    received_messages[topic] = payload
    print(f"[DEBUG] Received message on topic: {topic} with payload: {payload}")

@given('the MQTT broker is running on "{host}" and port "{port}"')
def step_impl(context, host, port):
    global mqtt_client
    print(f"[DEBUG] Given step: MQTT broker is running on {host}:{port}")
    if 'use_real_mqtt' in context.tags:
        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        mqtt_client.connect(host, int(port), 60)
        mqtt_client.loop_start()
        time.sleep(5)  # Ensure the connection is established
        print(f"[DEBUG] Real MQTT client initialized and connected to {host}:{port}")
    else:
        mqtt_client = MagicMock()
        mqtt_client.connect.return_value = None
        mqtt_client.loop_start.return_value = None
        mqtt_client.publish.return_value = None
        print(f"[DEBUG] Mock MQTT client initialized")

@when('I publish a "query" command to the gauge "Motor 1" with payload ""')
def step_impl(context):
    topic = "gauge/Motor 1/query"
    payload = ""
    print(f"[DEBUG] When step: Publishing message to topic: {topic} with payload: {payload}")
    mqtt_client.publish(topic, payload)
    if 'use_mock_mqtt' in context.tags:
        mqtt_client.on_message(mqtt_client, None, MagicMock(topic=topic, payload=payload.encode('utf-8')))

@then(u'the response should be received on the gauge "Motor 1" with payload \'{"name": "Motor 1", "min_val": -100.0, "max_val": 100.0, "calibrated": true, "position": 0.0}\'')
def step_impl(context):
    expected_topic = "gauge/Motor 1/query"
    expected_payload = '{"name": "Motor 1", "min_val": -100.0, "max_val": 100.0, "calibrated": true, "position": 0.0}'
    
    # Wait for the message to be received
    time.sleep(2)
    
    # Check if the expected message was received
    assert expected_topic in received_messages, f"[DEBUG] Expected topic '{expected_topic}' not found in received messages"
    assert received_messages[expected_topic] == expected_payload, f"[DEBUG] Expected payload '{expected_payload}' but got '{received_messages[expected_topic]}'"
    print(f"[DEBUG] Then step: Received expected message on topic '{expected_topic}' with payload '{expected_payload}'")