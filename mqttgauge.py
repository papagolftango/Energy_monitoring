import time
import paho.mqtt.client as mqtt
import argparse
from gauge import *


# Parse command-line arguments for GPIO pins and motor ID
parser = argparse.ArgumentParser()
parser.add_argument('motorID', type=str, help='Unique motor identifier')
parser.add_argument('minGauge', type=int, help='min value for gauge position')
parser.add_argument('maxGauge', type=int, help='max value for gauge position')
args = parser.parse_args()

# Create a gauge instance
g = GaugeStepper(args.motorID, args.minGauge, args.maxGauge)

# MQTT settings
MQTT_BROKER = '192.168.68.96'
MQTT_PORT = 1883
MQTT_BASE_TOPIC = 'PowerGauge/Motors/{}'.format(args.motorID)  # Base topic with motor ID

def status(param, motor_instance):
    print("Status", param)
    motor_instance.GetStatus()
  
def setup(param, motor_instance):
    print("Setup", param)
    motor_instance.Calibrate()

def getpos(param, motor_instance):
    print("GetPos", param)
    print(motor_instance.getpos())

def move(param, motor_instance):
    print("Move", param)
    motor_instance.MoveTo(param)

Cmds = {
    "status": status,
    "setup": setup,
    "getPosition": getpos,
    "moveTo": move,
}


#
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    topic_parts = msg.topic.split('/')
    if len(topic_parts) == 4 and topic_parts[2] == args.motorID:
        command = topic_parts[3]
        payload = msg.payload.decode('utf-8')
        if command in Cmds:
            Cmds[command](payload, g)
        else:
            print("Unknown command")

# MQTT Client Setup
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Subscribe to all commands for this motor
client.subscribe(MQTT_BASE_TOPIC + '/#')
client.loop_forever()