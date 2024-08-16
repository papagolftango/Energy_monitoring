import time
import paho.mqtt.client as mqtt
import argparse
import motor
from gauge import GaugeStepper

class MQTTGauge:
    def __init__(self, motorNumber, motorID, minGauge, maxGauge):
        self.motor = Motor()
        self.gauge_stepper = GaugeStepper(self.motor, motorName, motorID, minGauge, maxGauge)
        self.MQTT_BROKER = '192.168.68.96'
        self.MQTT_PORT = 1883
        self.MQTT_BASE_TOPIC = 'PowerGauge/Motors/{}'.format(motorID)
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe(self.MQTT_BASE_TOPIC + "/#")

    def on_message(self, client, userdata, msg):
        payload = msg.payload.decode()
        print(f"Received message: {payload}")
        # Handle the message based on the topic and payload

    def status(self, param):
        print("Status", param)
        self.gauge_stepper.GetStatus()

    def setup(self, param):
        print("Setup", param)
        self.gauge_stepper.Calibrate()

    def cal(self, param):
        print("Cal", param)
        # Implement calibration logic

    def version(self, param):
        print("Version", param)
        # Implement version logic

    def message(self, param):
        print("Message", param)
        # Implement message handling logic

def main(motorNumber, motorID, minGauge, maxGauge):
    mqtt_gauge = MQTTGauge(motorName, motorID, minGauge, maxGauge)
    mqtt_gauge.client.connect(mqtt_gauge.MQTT_BROKER, mqtt_gauge.MQTT_PORT, 60)
    mqtt_gauge.client.loop_forever()