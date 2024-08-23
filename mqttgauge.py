import paho.mqtt.client as mqtt
import json
from gauges import Gauges

# Initialize Gauges
gauges = Gauges()

# MQTT settings
BROKER = '192.168.68.86'
PORT = 1883
TOPIC_PREFIX = 'gauges/'

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(f"{TOPIC_PREFIX}#")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    print(f"Received message '{payload}' on topic '{topic}'")

    # Parse the topic to determine the action
    parts = topic.split('/')
    if len(parts) < 3:
        print("Invalid topic format")
        return

    gauge_name = parts[1]
    action = parts[2]

    # Find the gauge by name
    gauge_id = next((i for i, g in enumerate(gauges.motor_config) if g["name"] == gauge_name), None)
    if gauge_id is None:
        print(f"Gauge '{gauge_name}' not found")
        return

    if action == 'query':
        handle_query(client, gauge_id)
    elif action == 'calibrate':
        handle_calibrate(client, gauge_id)
    elif action == 'move':
        handle_move(client, gauge_id, payload)
    else:
        print(f"Unknown action '{action}'")

def handle_query(client, gauge_id):
    response_topic = f"{TOPIC_PREFIX}{gauges.get_name(gauge_id)}/response"
    client.publish(response_topic, json.dumps({"calibrated": gauges.is_calibrated(gauge_id)}))

def handle_calibrate(client, gauge_id):
    gauges.calibrate(gauge_id)
    response_topic = f"{TOPIC_PREFIX}{gauges.get_name(gauge_id)}/response"
    client.publish(response_topic, json.dumps({"calibrated": True}))

def handle_move(client, gauge_id, payload):
    try:
        position = float(payload)
        gauges.motor_steps(gauge_id, position)
        response_topic = f"{TOPIC_PREFIX}{gauges.get_name(gauge_id)}/response"
        client.publish(response_topic, json.dumps({"position": gauges.get_position(gauge_id)}))
    except ValueError:
        print(f"Invalid position value '{payload}'")

# Set up MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)

# Start the MQTT client loop
client.loop_forever()