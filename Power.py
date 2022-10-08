import time
import paho.mqtt.client as mqtt
import gauge

p = Gauge("Power",-3000, 3000 , 1, 2)


def cal(param):
  print "cal",param


def status(param):
  print "Status", param #  powerGauge.get_data(), consumerGauge.get_data()

def setup(param):
  print "Setup", param

def version(param):
  print "version", param

def message(param):
  print "Message", param

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


# Initial state for LEDs:

client = mqtt.Client()
client.connect("192.168.1.32",1883,60)

client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()


