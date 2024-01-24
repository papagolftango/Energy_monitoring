import time
import paho.mqtt.client as mqtt
import gauge


def status(param):
  print( "Status", param) 
def setup(param):
  print ( "Setup", param)

def version(param):
  print ("version", param)

def message(param):
  print ("Message", param)

Cmds = {
        "cal" : cal,
        "status" : status,
        "setup" : setup,
        "version": version,
        "message" :  message,
      }

def on_message(client, userdata, msg):
    p,s = msg.payload.decode().split(",")
    print("p " + p)
    print("s " + s)
    Cmds[p](s)


def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))
  client.subscribe("topic/iopi")

client = mqtt.Client()
client.username_pw_set("pgt", "2906")
client.connect("192.168.68.96",1883,60)

client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()

'''
l = Gauge("consumer", 0, 6000, 3,4)
m = Gauge("consumer", 0, 6000, 5,6)
n = Gauge("consumer", 0, 6000, 7,8)
o = Gauge("consumer", 0, 6000, 9,10)
l.Calibrate()
m.Calibrate()
n.Calibrate()
o.Calibrate()
x,y = l.GetStatus()
print(x,y)
l.MoveTo(2400)
l.MoveTo(2000)

 
(chip_id, chip_version) = bme280.readBME280ID()
print ("Chip ID :", chip_id)
print ("Version :", chip_version)
 
temperature,pressure,humidity = bme280.readBME280All()
 
print ("Temperature : ", temperature, "C")
print ("Pressure : ", pressure, "hPa")
print ("Humidity : ", humidity, "%")

'''