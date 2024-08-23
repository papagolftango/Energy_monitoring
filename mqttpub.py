BROKER = '192.168.68.86'
PORT = 1883
TOPIC_PREFIX = 'gauges/'

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print(f"[DEBUG] Connected with result code {rc}")
    client.subscribe(f"{TOPIC_PREFIX}#")
    print(f"[DEBUG] Subscribed to topic: {TOPIC_PREFIX}#")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')
    print(f"[DEBUG] Received message '{payload}' on topic '{topic}'")

    # Parse the topic to determine the action
    parts = topic.split('/')
    if len(parts) < 3:
        print("[DEBUG] Invalid topic format")
        return

    gauge_name = parts[1]
    action = parts[2]

    # Find the gauge by name
    gauge_id = next((i for i, g in enumerate(gauges.motor_config) if g["name"] == gauge_name), None)
    if gauge_id is None:
        print(f"[DEBUG] Gauge '{gauge_name}' not found")
        return

    if action == 'query':
        handle_query(client, gauge_id)
    elif action == 'calibrate':
        handle_calibrate(client, gauge_id)
    elif action == 'move':
        handle_move(client, gauge_id, payload)
    else:
        print(f"[DEBUG] Unknown action '{action}'")