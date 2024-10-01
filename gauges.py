import time
import pigpio
from steppermotor import StepperMotor  # Ensure this import matches your file structure

class Gauges:
 
    def __init__(self):
        self.stepper = StepperMotor()
        self.MOTOR_MAX_STEPS = self.stepper.get_max_steps()
        self.stepper.calibrate_all()

        self.gauge_config = [
                {"name": "Gauge1", "min_val": -100.0, "max_val": 100.0,  "scale": 1.0, "pos": 0.0},
                {"name": "Gauge2", "min_val": 0.0,    "max_val": 1.0,    "scale": 1.0, "pos": 0.0},
                {"name": "Gauge3", "min_val": 0,      "max_val": 100.0,  "scale": 1.0, "pos": 0.0},
                {"name": "Gauge4", "min_val": -2000.0,"max_val": 1000.0, "scale": 1.0, "pos": 0.0}
        ]
        self.gauge_map = {gauge["name"]: gauge for gauge in self.gauge_config}
        # Calculate scale factors
        self.calcScaleFactors()

    def calcScaleFactors(self):
        # Calculate scale factors
        for gauge in self.gauge_config:
            gauge["scale_factor"] = self.MOTOR_MAX_STEPS / (gauge["max_val"] - gauge["min_val"])
            gauge["pos:"] = gauge["min_val"]    
            print(f"Scale factor for {gauge['name']}: {gauge['scale_factor']}")

    def cleanup(self):
        self.stepper.cleanup()

   
    def move_gauge(self, gauge_index, value):
        """
        Move a single gauge to the specified value.
        :param gauge_index: Index of the gauge to move (0 to 3)
        :param value: Value to move the gauge to
        """
        if gauge_index < 0 or gauge_index >= len(self.gauge_config):
            raise ValueError("Invalid gauge index")

        gauge = self.gauge_config[gauge_index]
        scale_factor = gauge["scale_factor"]
        # Apply scaling to convert value to steps
        steps = int((value - gauge["min_val"]) * scale_factor)

        # Update current position in steps
        gauge["pos"] = steps
        print(gauge_index, value)
        print(*[steps if i == gauge_index else gauge["pos"] for i, gauge in enumerate(self.gauge_config)])
        # Move the stepper motor to the new position
        self.stepper.moveto(*[steps if i == gauge_index else gauge["pos"] for i, gauge in enumerate(self.gauge_config)])

    def get_all_gauges_status(self):
        status_list = []
        for gauge in self.gauge_config:
            status_list.append({
                "name":     gauge["name"],
                "position": gauge["pos"]
            })
        return status_list
    
# Example usage
if __name__ == "__main__":
    gauges = Gauges()
    try:
        while True:
            gauge_id = int(input("Enter gauge ID (0-3): "))
            pos = float(input("Enter position: "))
            gauges.move_gauge(gauge_id, pos)
            print(f"Moved gauge {gauge_id} to position {pos}")
            print("Current gauge statuses:")
            for status in gauges.get_all_gauges_status():
                print(status)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        gauges.cleanup()