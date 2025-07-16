import paho.mqtt.client as mqtt
from gauges import Gauges
import logging

logging.basicConfig(level=logging.INFO)

# === MQTT broker config ===
EMONPI_HOST = "emonpi.local"       # or IP, e.g. "192.168.1.100"
EMONPI_PORT = 1883
MQTT_USERNAME = "your_username"    # replace with emonPi MQTT user (e.g. "emonpi")
MQTT_PASSWORD = "your_password"    # replace with your MQTT password

# === Topic-to-gauge mapping ===
TOPIC_TO_GAUGE = {
    "emon/house/power": 0,
    "emon/house/voltage": 1,
    "emon/house/current": 2,
    "emon/house/frequency": 3
}

# === Setup gauges ===
gauges = Gauges()

# === MQTT Callbacks ===
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT broker")
        for topic in TOPIC_TO_GAUGE:
            client.subscribe(topic)
            logging.info(f"Subscribed to topic: {topic}")
    else:
        logging.error(f"Failed to connect to broker, return code={rc}")

def on_message(client, userdata, msg):
    try:
        value = float(msg.payload.decode())
        gauge_index = TOPIC_TO_GAUGE.get(msg.topic)
        if gauge_index is not None:
            logging.info(f"{msg.topic} → Gauge {gauge_index} → Value: {value}")
            gauges.move_gauge(gauge_index, value)
    except Exception as e:
        logging.error(f"Error processing message from {msg.topic}: {e}")

# === MQTT Client Setup ===
client = mqtt.Client()

# 🔐 Enable username/password authentication
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

# Uncomment this line and comment out the one above to disable authentication:
# client = mqtt.Client()  # No username/password

client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(EMONPI_HOST, EMONPI_PORT, 60)
    client.loop_forever()
except KeyboardInterrupt:
    logging.info("Interrupted by user")
finally:
    gauges.cleanup()
