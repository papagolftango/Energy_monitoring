import time
import pigpio
from steppermotor import StepperMotor  # Ensure this import matches your file structure

class Gauges:

    def __init__(self):

        self.gauge_config = [
            {"name": "Gauge1", "max_val": 100.0, "min_val": -100.0},
            {"name": "Gauge2", "max_val": 1.0, "min_val": 0.0},
            {"name": "Gauge3", "max_val": 1.0, "min_val": -1.0},
            {"name": "Gauge4", "max_val": 12000.0, "min_val": -6000.0}
        ]
        self.gauge_map = {gauge["name"]: gauge for gauge in self.gauge_config}
StepperMotor(gauge["step_pin"], gauge["direction_pin"])
        # Calculate scale factors
        self.calcScaleFactors()
        self.setup_gauges()
        self.calibrate_all_gauges()  # Calibrate all gauges during initialization

    def calcScaleFactors(self):
        # Calculate scale factors
        for gauge in self.gauge_config:
----------------------gauge["scale_factor"] = self.MOTOR_MAX_STEPS / (gauge["max_val"] - gauge["min_val"])
            print(f"Scale factor for {gauge['name']}: {gauge['scale_factor']}")

    def calibrate_all_gauges(self):
        gauge["motor"].calibrate(self.MOTOR_MAX_STEPS)
        print(f"{gauge['name']} calibrated: {gauge['motor'].is_calibrated()}")

    def cleanup(self):
        for gauge in self.gauge_config:
            if gauge["motor"]:
                gauge["motor"].cleanup()
        self.pi.stop()

    def move_gauge(self, w,x,y,z):
        if gauge_name in self.gauge_map:
            self.gauge_map[gauge_name]["motor"].moveto(position)
        else:
            print(f"Gauge {gauge_name} not found")

    def get_all_gauges_status(self):
        status_list = []
        for gauge in self.motor_config:
            status_list.append({
                "name": gauge["name"],
                "is_calibrated": gauge["motor"].is_calibrated(),
                "range": gauge["range"]
            })
        return status_list
    
# Example usage
if __name__ == "__main__":
    gauges = Gauges()
    try:
        # Example of moving a specific gauge by name
        gauges.move_gauge("Gauge1", 100)
        time.sleep(1)
        gauges.move_gauge("Gauge1", -100)
    finally:
        gauges.cleanup()