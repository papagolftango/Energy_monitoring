import time
import paho.mqtt.client as mqtt
import argparse
from gauge import gaugeStepper

# Parse command-line arguments for GPIO pins and motor ID

parser = argparse.ArgumentParser()
parser.add_argument('stepGpio', type= int, help='GPIO pin for step signal')
parser.add_argument('dirGpio', type=int,  help='GPIO pin for direction signal')
parser.add_argument('motorID', type=str,  help='Unique motor identifier')
parser.add_argument('minGauge', type=int,  help='min value for gauge position')
parser.add_argument('maxGauge', type=int,  help='max value for gauge position')
args = parser.parse_args()


# create a gauge instance
g = gaugeStepper(args.motorID, args.minGauge, args.maxGauge , args.dirGpio, args.stepGpio)

# MQTT settings
MQTT_BROKER = '192.168.68.96'
MQTT_PORT = 1883
MQTT_TOPIC_TEMPLATE = 'PowerGauge/{}  '  # Topic template with motor ID placeholder

topic = MQTT_TOPIC_TEMPLATE.format(args.motorID)
print(topic)

def status(param):
  print( "Status", param) 
  g.GetStatus()
  
def setup(param):
  print ( "Setup", param)
  g.Calibrate()

def getpos(param):
   print ("GetPos", param)
   print(g.getpos())

def move(param):
  print ("Move", param)
  g.MoveTo(param)

Cmds = {
        "cal" : cal,
        "status" : status,
        "setup" : setup,
        "version": getpos,
        "move" :  move,
      }

def on_message(client, userdata, msg):
    print(msg)
    topic_parts = msg['topic'].split('/')
    if len(topic_parts) == 2 and topic_parts[0] == MQTT_TOPIC_TEMPLATE:
       motor_name = topic_parts[1]
       # Perform the reverse lookup to get the motor instance
       motor_instance = find_motor_by_name(motor_name, gauges)
       if motor_instance is not None:
         parts = msg["payload"].split(" ")
         if len(parts) >= 2:
            Cmds[parts[0]](parts[1], motor_instance)
         elif len(parts) == 1:
        # Handle the case where there's only one item
            Cmds[parts[0]](motor_instance)
         else:
           pass
       else:
         print(f"No motor instance found for '{motor_name}'")
    else:
        print("Invalid MQTT topic format")
        

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
 # client.subscribe(topic)


# Connect to MQTT broker and subscribe to topic
client = mqtt.Client()
client.username_pw_set("pgt", "2906")
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT)

client.loop_start()
# Main loop (can be replaced with event-driven mechanisms)
try:
    while True:
        pass  # Keep the program running
except KeyboardInterrupt:
    # Clean up
    client.disconnect()
    g.Finish()


