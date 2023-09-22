import time
#import paho.mqtt.client as paho
from mqtt import mqtt
from gauge import gaugeStepper
from motor import Motor

# Simulated MQTT message payload
sample_message = {
    "topic": "PowerGauge/Power",
    "payload": "status",
    "qos": 0,
    "retain": False
}
sample_message1 = {
    "topic": "PowerGauge/Power",
    "payload": "move 1000",
    "qos": 1000,
    "retain": False
}

gauges = [
            {"name": "Power",    "min" : 0, "max": 6000, "instance" : None},
            {"name": "Solar",    "min" : 0, "max": 6000, "instance" : None}, 
            {"name": "MaxPower", "min" : 0, "max": 6000, "instance" : None},
            {"name": "Export",   "min" : 0, "max": 6000, "instance" : None}
         ]

# create a motor instance
m = Motor()
gauges[0]["instance"] = gaugeStepper(gauges[0]["name"], gauges[0]["min"], gauges[0]["max"], 0, m)
gauges[1]["instance"] = gaugeStepper(gauges[1]["name"], gauges[1]["min"], gauges[1]["max"], 1, m)
gauges[2]["instance"] = gaugeStepper(gauges[2]["name"], gauges[2]["min"], gauges[2]["max"], 2, m)
gauges[3]["instance"] = gaugeStepper(gauges[3]["name"], gauges[3]["min"], gauges[3]["max"], 3, m)

# MQTT settings
MQTT_BROKER = '192.168.1.53'
MQTT_PORT = 1883
MQTT_TOPIC_TEMPLATE = 'PowerGauge'  # Topic template with motor ID placeholder

def status(m):
  print( "Status") 
  client.publish('PowerGauge/'+ m["name"]+'/response/status', m['instance'].GetStatus())
  
def setup(m):
  print ( "Setup")
  m['instance'].Calibrate()
  status(m)

def getpos(m):
   print ("GetPos")
   client.publish('PowerGauge/'+ m["name"]+'/response/position', m['instance'].GetPos())

def move(param, m):
   # add check for no paramter
   print ("Move", int(param),m)
   m['instance'].MoveTo(int(param))
   status(m) 

def find_motor_by_name(name_to_find, motor_list):
  for motor in motor_list:
    if motor.get("name") == name_to_find:
      return motor
  return None

Cmds = {
        "status" : status,
        "setup" : setup,
        "getpos": getpos,
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
        

def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)
    client.subscribe(MQTT_TOPIC_TEMPLATE.format(gauges[0]["name"]))    
    client.subscribe(MQTT_TOPIC_TEMPLATE.format(gauges[1]["name"]))    
    client.subscribe(MQTT_TOPIC_TEMPLATE.format(gauges[2]["name"]))
    client.subscribe(MQTT_TOPIC_TEMPLATE.format(gauges[3]["name"]))
    
# with this callback you can see if your publish was successful
def on_publish(client, userdata, mid, properties=None):
    print("mid: " + str(mid))

# print which topic was subscribed to
def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

#client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
c = mqtt()
client = mqtt.Client(c)

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

# a single publish, this can also be done in loops, etc.
#client.publish(topic, payload="setup, ", qos=1)
#client.publish(topic, payload="status, ", qos=1)
# loop_forever for simplicity, here you need to stop the loop manually
# you can also use loop_start and loop_stop
#client.loop_forever()

client.loop_start()
# Main loop (can be replaced with event-driven mechanisms)
try:
    while True:
        time.sleep(3)
     #   client.publish('PowerGauge/Power', "move -42")
        on_message(client, 'PowerGauge', sample_message)
        on_message(client, 'PowerGauge', sample_message1)
except KeyboardInterrupt:
    pass

client.disconnect()
m.Finish()


'''
client = mqtt.Client()
client.connect("192.168.1.32",1883,60)

client._connect = on_connect
client.on_message = on_message
client.loop_forever()
'''

'''
l = gaugeStepper("consumer", -600, 600, 0) 
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
