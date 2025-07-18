import time
import pigpio
from steppermotor import StepperMotor  # Ensure this import matches your file structure
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Gauges:
 
    def __init__(self):
        self.stepper = StepperMotor()
        self.MOTOR_MAX_STEPS = self.stepper.get_max_steps()
        self.stepper.calibrate_all()

        # Build gauge configuration from environment variables
        self.gauge_config = self.build_gauge_config()
        
        # Calculate scale factors
        self.calcScaleFactors()
 def build_gauge_config(self):
        """Build gauge configuration from environment variables"""
        gauge_config = []
        
        # Look for GAUGE_0, GAUGE_1, GAUGE_2, GAUGE_3
        for i in range(4):
            gauge_key = f"GAUGE_{i}"
            gauge_value = os.getenv(gauge_key)
            
            if gauge_value:
                try:
                    # Parse format: name,min_val,max_val
                    parts = gauge_value.split(',')
                    if len(parts) == 3:
                        name = parts[0].strip()
                        min_val = float(parts[1].strip())
                        max_val = float(parts[2].strip())
                        
                        gauge_config.append({
                            "name": name,
                            "min_val": min_val,
                            "max_val": max_val,
                            "scale": 1.0,
                            "pos": 0.0
                        })
                        logging.info(f"Loaded gauge {i}: {name} ({min_val} to {max_val})")
                    else:
                        logging.warning(f"Invalid format for {gauge_key}: {gauge_value}")
                except ValueError as e:
                    logging.error(f"Error parsing {gauge_key}: {e}")
            else:
                logging.warning(f"No configuration found for gauge {i}")
                
        # Fallback to default configuration if no env vars found
        if not gauge_config:
            logging.warning("No gauge configuration found in environment variables, using defaults")
            gauge_config = [
                {"name": "Energy", "min_val": -6000.0, "max_val": 6000.0,  "scale": 1.0, "pos": 0.0},
                {"name": "Solar", "min_val": 0.0,    "max_val": 3000,    "scale": 1.0, "pos": 0.0},
                {"name": "mains", "min_val": 0.0,      "max_val": 300.0,  "scale": 1.0, "pos": 0.0},
                {"name": "Use", "min_val": 0.0,"max_val": 10000.0, "scale": 1.0, "pos": 0.0}
            ]
        
        return gauge_config
   
    def calcScaleFactors(self):
        # Calculate scale factors
        for gauge in self.gauge_config:
            gauge["scale_factor"] = self.MOTOR_MAX_STEPS / (gauge["max_val"] - gauge["min_val"])
            gauge["pos"] = gauge["min_val"]    
            logging.debug(f"Scale factor for {gauge['name']}: {gauge['scale_factor']}")

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

        # Saturate the value between min_val and max_val
        value = max(gauge["min_val"], min(value, gauge["max_val"]))

        # Apply scaling to convert value to steps
        steps = int((value - gauge["pos"]) * scale_factor)
        logging.debug(f"Gauge {gauge_index}: Value={value}, Steps={steps}, Current position={gauge['pos']}")
        # Update current position in steps
        gauge["pos"] = value
    
        logging.debug(f"Steps for all gauges: {[steps if i == gauge_index else 0 for i, gauge in enumerate(self.gauge_config)]}")
        # Move the stepper motor to the new position
        self.stepper.move(*[steps if i == gauge_index else 0 for i, gauge in enumerate(self.gauge_config)])

    def get_all_gauges_status(self):
        status_list = []
        for i, gauge in enumerate(self.gauge_config):
            status_list.append({
                "name":     gauge["name"],
                "position": gauge["pos"],
                "steps":    self.stepper.get_steps(i)  # Get steps using motor index
            })
        return status_list
    
# Example usage
if __name__ == "__main__":
    gauges = Gauges()
    try:
        for gauge_id in range(4):  # Iterate through gauge IDs 0 to 3
            min_val = gauge_config[gauge_id]["min_val"]
            max_val = gauge_config[gauge_id]["max_val"]
            step_size = (max_val - min_val) / 10

            for s in range(12):
                pos = min_val + i * step_size
                gauges.move_gauge(gauge_id, pos)

        for gauge_id in range(4):  # Iterate through gauge IDs 0 to 3
            min_val = gauge_config[gauge_id]["min_val"]
            max_val = gauge_config[gauge_id]["max_val"]
            step_size = (min_val - max_val) / 10

            for s in range(12):
                pos = min_val + i * step_size
                gauges.move_gauge(gauge_id, pos)
                
        print(gauges.get_all_gauges_status())
    finally:
        gauges.cleanup()