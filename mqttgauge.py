import time
import paho.mqtt.client as paho
from paho import mqtt
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

def status(param):
  print( "Status", param) 
  print(g.GetStatus())
  
def setup(param):
  print ( "Setup", param)
  g.Calibrate()

def getpos(param):
   print ("GetPos", param)
   print(g.getpos())

def move(param):
  print ("Move", int(param))
  g.MoveTo(int(param))

Cmds = {
        "status" : status,
        "setup" : setup,
        "version": getpos,
        "move" :  move,
      }

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    p,s = msg.payload.decode().split(",")
    Cmds[p](s)
  

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

#client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client = mqtt.Client()

client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_publish = on_publish

# enable TLS for secure connection
#client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
#client.username_pw_set("paul@thetindalls.co.uk", "")
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
#client.connect("8c86aacfce7d4aa8881cea67188295ab.s2.eu.hivemq.cloud", 8883)

# Connect to MQTT broker and subscribe to topic

client.connect(MQTT_BROKER, MQTT_PORT)
client.subscribe(topic, qos=1)

# a single publish, this can also be done in loops, etc.
client.publish(topic, payload="setup, ", qos=1)
client.publish(topic, payload="status, ", qos=1)
# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
#client.loop_forever()

client.loop_start()
# Main loop (can be replaced with event-driven mechanisms)
try:
    while True:
        time.sleep(1)
        client.publish(topic, payload="move, -42", qos=1)
except KeyboardInterrupt:
    pass


client.disconnect()
g.Finish()


'''
client = mqtt.Client()
client.connect("192.168.1.32",1883,60)

client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()
'''
'''

l = gaugeStepper("consumer", -600, 600, 3,4) 
#m = gaugeStepper("power", 0, 6000, 5,6)
#n = gaugeStepper("temp", 0, 6000, 7,8)
#o = gaugeStepper("humidity", 0, 6000, 9,10)
l.Calibrate()
#m.Calibrate()
#n.Calibrate()
#o.Calibrate()
#x,y,z = l.GetStatus()
l.MoveTo(-40)
l.MoveTo(0)
#print(".....................................................................................")
#x,y,z = l.GetStatus()
#print(x,y,z)
#print(l.GetPos())
#l.MoveTo(2000)
'''
'''
#(chip_id, chip_version) = bme280.readBME280ID()
#print ("Chip ID :", chip_id)
#print ("Version :", chip_version)
 
#temperature,pressure,humidity = bme280.readBME280All()
 
#print ("Temperature : ", temperature, "C")
#print ("Pressure : ", pressure, "hPa")
#print ("Humidity : ", humidity, "%")

'''
