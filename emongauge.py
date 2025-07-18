import paho.mqtt.client as mqtt
from gauges import Gauges
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)

# === MQTT broker config from environment variables ===
EMONPI_HOST = os.getenv("EMONPI_HOST", "emonpi.local")  # Default fallback
EMONPI_PORT = int(os.getenv("EMONPI_PORT", "1883"))     # Default fallback
MQTT_USERNAME = os.getenv("MQTT_USERNAME")              # Required
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")              # Required

# Validate required environment variables
if not MQTT_USERNAME or not MQTT_PASSWORD:
    raise ValueError("MQTT_USERNAME and MQTT_PASSWORD environment variables must be set")


# === Build topic-to-gauge mapping from environment variables ===
def build_topic_mapping():
    topic_to_gauge = {}
    
    # Get all environment variables that start with TOPIC_
    for key, value in os.environ.items():
        if key.startswith("TOPIC_") and ":" in value:
            topic, gauge_index = value.split(":", 1)
            try:
                topic_to_gauge[topic] = int(gauge_index)
                logging.info(f"Mapped {topic} → Gauge {gauge_index}")
            except ValueError:
                logging.warning(f"Invalid gauge index in {key}: {value}")
    
    if not topic_to_gauge:
        logging.warning("No topic mappings found in environment variables")
    
    return topic_to_gauge

TOPIC_TO_GAUGE = build_topic_mapping()

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

import paho.mqtt.client as mqtt
from gauges import Gauges
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)

# === MQTT broker config from environment variables ===
EMONPI_HOST = os.getenv("EMONPI_HOST", "emonpi.local")  # Default fallback
EMONPI_PORT = int(os.getenv("EMONPI_PORT", "1883"))     # Default fallback
MQTT_USERNAME = os.getenv("MQTT_USERNAME")              # Required
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")              # Required

# Validate required environment variables
if not MQTT_USERNAME or not MQTT_PASSWORD:
    raise ValueError("MQTT_USERNAME and MQTT_PASSWORD environment variables must be set")

# === Build topic-to-gauge mapping from environment variables ===
def build_topic_mapping():
    topic_to_gauge = {}
    
    # Get all environment variables that start with TOPIC_
    for key, value in os.environ.items():
        if key.startswith("TOPIC_") and ":" in value:
            topic, gauge_index = value.split(":", 1)
            try:
                topic_to_gauge[topic] = int(gauge_index)
                logging.info(f"Mapped {topic} → Gauge {gauge_index}")
            except ValueError:
                logging.warning(f"Invalid gauge index in {key}: {value}")
    
    if not topic_to_gauge:
        logging.warning("No topic mappings found in environment variables")
    
    return topic_to_gauge

TOPIC_TO_GAUGE = build_topic_mapping()

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

# === Main MQTT client setup ===
def main():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        logging.info(f"Connecting to MQTT broker at {EMONPI_HOST}:{EMONPI_PORT}")
        client.connect(EMONPI_HOST, EMONPI_PORT, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
    except Exception as e:
        logging.error(f"Connection error: {e}")
    finally:
        gauges.cleanup()
        client.disconnect()

if __name__ == "__main__":
    main()# === Main MQTT client setup ===
def main():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        logging.info(f"Connecting to MQTT broker at {EMONPI_HOST}:{EMONPI_PORT}")
        client.connect(EMONPI_HOST, EMONPI_PORT, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        logging.info("Interrupted by user")
    except Exception as e:
        logging.error(f"Connection error: {e}")
    finally:
        gauges.cleanup()
        client.disconnect()

if __name__ == "__main__":
    main()
