import time
import paho.mqtt.client as mqtt

# MQTT broker details
broker_address = "192.168.68.53"
port = 1883

# Motor details
motor_id = "motortest"

# Callback when connected to MQTT broker
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    # Subscribe to status topic
    client.subscribe(f"/PowerGauge/{motor_id}/status")

# Callback when a message is received from MQTT broker
def on_message(client, userdata, msg):
    print(f"Received message: {msg.topic} - {msg.payload}")

# Create MQTT client instance
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT broker
#client.connect(broker_address, port, 60)

# Start MQTT loop in the background
#client.loop_start()

try:
    # Setup motor
  #  client.publish(f"/PowerGauge/{motor_id}/setup", payload="setup_command_here", qos=0, retain=False)
    time.sleep(2)  # Wait for setup to complete

    # Get status
  #  client.publish(f"/PowerGauge/{motor_id}/status", payload="get_status_command_here", qos=0, retain=False)
    time.sleep(1)  # Wait for status response

    # Perform movement
    while True:
        for position in range(-40, 100, 10):
            print(f"/PowerGauge/{motor_id}/move",str(position))
            time.sleep(0.5)

        for position in range(100, -40, -10):
            print(f"/PowerGauge/{motor_id}/move",str(position))
 #           client.publish(f"/PowerGauge/{motor_id}/move", payload=str(position), qos=0, retain=False)
            time.sleep(0.5)

except KeyboardInterrupt:
    print("Program stopped by user.")

finally:
    # Stop MQTT loop and disconnect
    client.loop_stop()
    client.disconnect()
