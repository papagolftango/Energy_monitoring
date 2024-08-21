import json

class Gauges:
    def __init__(self, motor_class, config_file):
        self.motor_class = motor_class
        self.config_file = config_file
        self.gauges = []
        self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as file:
            config = json.load(file)
            for motor_config in config['motors']:
                motor = self.motor_class()
                gauge = Gauge(
                    motor,
                    motor_config['name'],
                    motor_config['id'],
                    motor_config['min_val'],
                    motor_config['max_val']
                )
                self.gauges.append(gauge)

    def get_gauges(self):
        return self.gauges

    def get_gauge_names(self):
        return [gauge.name for gauge in self.gauges]

    def get_gauge_details(self):
        return [gauge.get_details() for gauge in self.gauges]