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

    # Handle the action
    if action == 'discover':
        handle_discover(client)
    else:
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

def handle_discover(client):
    status_list = gauges.get_all_gauges_status()
    response = {
        "gauges": status_list
    }
    client.publish(f"{TOPIC_PREFIX}discover/status", json.dumps(response))

def handle_query(client, gauge_id):
    gauge = gauges.motor_config[gauge_id]
    is_calibrated = gauge["motor"].is_calibrated()
    response = {
        "gauge": gauge["name"],
        "is_calibrated": is_calibrated,
        "range": gauge["range"]
    }
    client.publish(f"{TOPIC_PREFIX}{gauge['name']}/status", json.dumps(response))

def handle_calibrate(client, gauge_id):
    gauge = gauges.motor_config[gauge_id]
    gauge["motor"].calibrate(gauges.MOTOR_MAX_STEPS)
    response = {
        "gauge": gauge["name"],
        "calibrated": gauge["motor"].is_calibrated(),
        "range": gauge["range"]
    }
    client.publish(f"{TOPIC_PREFIX}{gauge['name']}/status", json.dumps(response))

def handle_move(client, gauge_id, payload):
    try:
        data = json.loads(payload)
        position = data.get("position")
        if position is not None:
            gauges.move_gauge(gauge_id, position)
        else:
            print("Invalid payload: 'position' not found")
    except json.JSONDecodeError:
        print("Failed to decode JSON")

# Set up MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker and start loop
client.connect(BROKER, PORT, 60)
client.loop_forever()