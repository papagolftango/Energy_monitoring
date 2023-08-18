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
MQTT_BROKER = '192.168.1.53'
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

def getpos():
   print ("GetPos", param)
   print(g.getpos())

def move(param):
  print ("Move", param)
  g.MoveTo(param)

Cmds = {
        "status" : status,
        "setup" : setup,
        "version": getpos,
        "move" :  move,
      }

def on_message(client, userdata, msg):
    p,s = msg.payload.decode().split(",")
    print("p " + p)
    print("s " + s)
    Cmds[p](s)


def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe(topic)


# Connect to MQTT broker and subscribe to topic
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT)

client.loop_start()
# Main loop (can be replaced with event-driven mechanisms)
try:
    while True:
        pass  # Keep the program running
except KeyboardInterrupt:
    pass

# Clean up
client.disconnect()
g.Finish()


'''
client = mqtt.Client()
client.connect("192.168.1.32",1883,60)

client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()



l = gaugeStepper("consumer", 0, 6000, 3,4)
#m = gaugeStepper("consumer", 0, 6000, 5,6)
#n = gaugeStepper("consumer", 0, 6000, 7,8)
#o = gaugeStepper("consumer", 0, 6000, 9,10)
l.Calibrate()
#m.Calibrate()
#n.Calibrate()
#o.Calibrate()
x,y,z = l.GetStatus()
print(x,y)
l.MoveTo(2400)
l.MoveTo(2000)

 
#(chip_id, chip_version) = bme280.readBME280ID()
#print ("Chip ID :", chip_id)
#print ("Version :", chip_version)
 
#temperature,pressure,humidity = bme280.readBME280All()
 
#print ("Temperature : ", temperature, "C")
#print ("Pressure : ", pressure, "hPa")
#print ("Humidity : ", humidity, "%")

'''