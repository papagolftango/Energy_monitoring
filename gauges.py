import time
import pigpio
from steppermotor import StepperMotor  # Ensure this import matches your file structure

class Gauges:

    def __init__(self):
        self.stepper = StepperMotor()
        self.Max_Motor_Steps = self.stepper.get_max_steps()
 
        self.gauge_config = [
            {"name": "Gauge1", "max_val": 100.0, "min_val": -100.0,  "scale": 1.0, "pos" : min_val},
            {"name": "Gauge2", "max_val": 1.0,   "min_val": 0.0,     "scale": 1.0, "pos" : min_val},
            {"name": "Gauge3", "max_val": 1.0,    "min_val": -1.0,   "scale": 1.0, "pos" : min_val},
            {"name": "Gauge4", "max_val": 12000.0,"min_val": -6000.0,"scale": 1.0, "pos" : min_val}
        ]
        self.gauge_map = {gauge["name"]: gauge for gauge in self.gauge_config}

        # Calculate scale factors
        self.calcScaleFactors()
        self.setup_gauges()
        self.calibrate_all_gauges()  # Calibrate all gauges during initialization

    def calcScaleFactors(self):
        # Calculate scale factors
        for gauge in self.gauge_config:
            gauge["scale_factor"] = self.MOTOR_MAX_STEPS / (gauge["max_val"] - gauge["min_val"])
            print(f"Scale factor for {gauge['name']}: {gauge['scale_factor']}")

    def calibrate_all_gauges:
        self.stepper.calibrate_all()

    def cleanup(self):
        self.stepper.cleanup()

    def move_gauge(self, w,x,y,z):
        values = [w, x, y, z]
        scaled_values = []

        for i, value in enumerate(values):
            gauge = self.gauge_config[i]
            scale_factor = gauge["scale_factor"]
            # Apply scaling
            scaled_value = value * scale_factor
            # Set to limits if out of range
            scaled_value = max(min(scaled_value, gauge["max_val"]), gauge["min_val"])
            # Append scaled value to list
            scaled_values.append(scaled_value)
            # Update current position
            gauge["current_position"] = scaled_value    # set to limits if out of range

        self.stepper.moveto(*scaled_values)


    def get_all_gauges_status(self):
        status_list = []
        for gauge in self.motor_config:
            status_list.append({
                "name":     gauge["name"],
                "position": gauge["current_position"],
                "range":    gauge["range"]
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