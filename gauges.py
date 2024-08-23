import pigpio
import time

class Gauges:
    MOTOR_MAX_STEPS = 6000  # Constant for motor max step

    def __init__(self):
        self.pi = pigpio.pi()  # Initialize pigpio locally
        self.RESET_PIN = 17  # Example GPIO pin for reset

        self.reset_gpio()  # Reset the board

        self.initialize_gpio()
        
        self.motor_config = [
            {"motor_id": 0, "name": "Motor 1", "max_val": 100.0, "min_val": -100.0, "scale_factor": None, "direction_pin": 5, "step_pin": 17, "pos": 0.0},
            {"motor_id": 1, "name": "Motor 2", "max_val": 1.0, "min_val": 0.0, "scale_factor": None, "direction_pin": 6, "step_pin": 22, "pos": 10.0},
            {"motor_id": 2, "name": "Motor 3", "max_val": 1.0, "min_val": -1.0, "scale_factor": None, "direction_pin": 13, "step_pin": 24, "pos": 5.0},
            {"motor_id": 3, "name": "Motor 4", "max_val": 12000.0, "min_val": -6000.0, "scale_factor": None, "direction_pin": 19, "step_pin": 27, "pos": 20.0}
        ]

        # Calculate scale factors
        self.calcScaleFactors()

        self.wid = [None] * len(self.motor_config)  # Initialize waveform IDs
        self.calibrated = False  # Initialize calibrated flag

     
        self.setup_waveforms()

    def calcScaleFactors(self):
        # Calculate scale factors
        for motor in self.motor_config:
            motor["scale_factor"] = self.MOTOR_MAX_STEPS / (motor["max_val"] - motor["min_val"])
            print( motor["scale_factor"])

    def initialize_gpio(self):
        self.pi.set_mode(self.RESET_PIN, pigpio.OUTPUT)
        self.reset_gpio()

        # Set direction and step pins as output
        for motor in self.motor_config:
            self.pi.set_mode(motor["direction_pin"], pigpio.OUTPUT)
            self.pi.set_mode(motor["step_pin"], pigpio.OUTPUT)

    def reset_gpio(self):
        self.pi.write(self.RESET_PIN, 1)
        self.pi.write(self.RESET_PIN, 0)
        time.sleep(0.01)
        self.pi.write(self.RESET_PIN, 1)

    def setup_waveforms(self):
        for motor in self.motor_config:
            waveform = self.pi.wave_add_generic([
                pigpio.pulse(1 << motor["step_pin"], 0, 1000),  # Step on for 1000 microseconds
                pigpio.pulse(0, 1 << motor["step_pin"], 1000)   # Step off for 1000 microseconds
            ])
            motor["wid"] = self.pi.wave_create()
    

    def motor_steps(self, motor_id, steps):
        
        motor = self.motor_config[motor_id]
        direction = 1 if steps > 0 else 0
        steps = abs(steps)

        self.pi.write(motor["direction_pin"], direction)
        
        num_loops = abs(steps // 256)
        remaining_steps = abs(steps % 256)
        self.pi.wave_chain([
            255, 0,                       # loop start
            self.wid[motor_id],           # transmit waveform
            255, num_loops, remaining_steps, 0  # loop end
        ])
        
        while self.pi.wave_tx_busy() == True:
            time.sleep(0.01)  # Wait for the wave transmission to finish
       

    def stop_all_motors(self):
        self.pi.wave_tx_stop()

    def scale_value(self, gauge_id, value):
        # Retrieve the gauge configuration using the gauge_id
        gauge_config = self.motor_config[gauge_id]
        
        # Debug prints to diagnose the issue
        print(f"Scaling value: {value}")
        print(f"min_val: {gauge_config['min_val']}, max_val: {gauge_config['max_val']}")
        
        # Check for division by zero
        if gauge_config['max_val'] == gauge_config['min_val']:
            raise ValueError("max_val and min_val cannot be the same value.")
        
        # Scale the value to the range of 0 to max_steps using the pre-calculated scale factor
        scaled_value = int((value - gauge_config['min_val']) * gauge_config['scale_factor'])
        print(f"Scaled value: {scaled_value}")
        return scaled_value

    def move_to(self, gauge_id, target_position):
        # Retrieve the gauge configuration using the gauge_id
        gauge_config = self.motor_config[gauge_id]
    
        print(f"Moving gauge {gauge_id} to target position: {target_position}")
    
        # Clamp target_position within min_val and max_val
        if target_position > gauge_config['max_val']:
            target_position = gauge_config['max_val']
        elif target_position < gauge_config['min_val']:
            target_position = gauge_config['min_val']
        
        scaled_target = self.scale_value(gauge_id, target_position)
        print(f"Scaled target: {scaled_target}")
        steps = scaled_target 
        self.motor_steps(gauge_config['motor_id'], steps) 
        gauge_config['pos'] = target_position  # Update position to the new target
        
        print(f"Gauge {gauge_id} current position after move: {gauge_config['pos']}")

    def get_position(self, gauge_id):
         return self.motor_config[gauge_id]["pos"]
    
    def calibrate(self, motor_id):
        # Move to max steps
        self.motor_steps(motor_id, self.MOTOR_MAX_STEPS)
        # Move back to 0
        self.motor_steps(motor_id, -self.MOTOR_MAX_STEPS)
        self.motor_config[motor_id]["pos"] = 0  # Reset position to 0
        self.motor_config[motor_id]["calibrated"] = True  # Set calibrated flag
        print(f"Calibration complete for motor {motor_id}.")

    def set_min_value(self, gauge_id, val):
        self.motor_config[gauge_id]["min_val"] = val
        self.calcScaleFactors()

    def get_min_value(self, gauge_id):
        return self.motor_config[gauge_id]["min_val"]

    def set_max_value(self, gauge_id, val):
        self.motor_config[gauge_id]["max_val"] = val
        self.calcScaleFactors()
          
          

    def get_max_value(self, gauge_id):
        return self.motor_config[gauge_id]["max_val"]
    
    def is_calibrated(self, gauge_id):
        return self.motor_config[gauge_id]["calibrated"]
    
    def get_name(self, gauge_id):
        return self.motor_config[gauge_id]["name"]

    def set_name(self, gauge_id, name):
        self.motor_config[gauge_id]["name"] = name