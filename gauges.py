import time
import pigpio

class Gauges:
    MOTOR_MAX_STEPS = 200  # Example value, adjust as needed

    def __init__(self):
        self.pi = pigpio.pi()  # Initialize pigpio locally
        self.RESET_PIN = 17  # Example GPIO pin for reset

        self.motor_config = [
            {"motor_id": 0, "name": "Motor1", "max_val": 100.0, "min_val": -100.0, "scale_factor": None, "direction_pin": 5, "step_pin": 17, "pos": 0.0, "calibrated": False, "wid": None},
            {"motor_id": 1, "name": "Motor2", "max_val": 1.0, "min_val": 0.0, "scale_factor": None, "direction_pin": 6, "step_pin": 22, "pos": 10.0, "calibrated": False, "wid": None},
            {"motor_id": 2, "name": "Motor3", "max_val": 1.0, "min_val": -1.0, "scale_factor": None, "direction_pin": 13, "step_pin": 24, "pos": 5.0, "calibrated": False, "wid": None},
            {"motor_id": 3, "name": "Motor4", "max_val": 12000.0, "min_val": -6000.0, "scale_factor": None, "direction_pin": 19, "step_pin": 27, "pos": 20.0, "calibrated": False, "wid": None}
        ]
        self.initialize_gpio()
        self.reset_gpio()  # Reset the board

        # Calculate scale factors
        self.calcScaleFactors()

        self.calibrated = False  # Initialize calibrated flag

        self.setup_waveforms()
        self.calibrate_all_gauges()  # Calibrate all gauges during initialization

    def calcScaleFactors(self):
        # Calculate scale factors
        for motor in self.motor_config:
            motor["scale_factor"] = self.MOTOR_MAX_STEPS / (motor["max_val"] - motor["min_val"])
            print(motor["scale_factor"])

    def initialize_gpio(self):
        self.pi.set_mode(self.RESET_PIN, pigpio.OUTPUT)
        self.reset_gpio()

        # Set direction and step pins as output
        for motor in self.motor_config:
            self.pi.set_mode(motor["direction_pin"], pigpio.OUTPUT)
            self.pi.set_mode(motor["step_pin"], pigpio.OUTPUT)

    def reset_gpio(self):
        self.pi.write(self.RESET_PIN, 1)

    def setup_waveforms(self):
        try:
            for motor in self.motor_config:
                self.pi.wave_clear()  # Clear any existing waveforms
                self.pi.wave_add_generic([
                    pigpio.pulse(1 << motor["step_pin"], 0, 1000),  # Step on for 1000 microseconds
                    pigpio.pulse(0, 1 << motor["step_pin"], 1000)   # Step off for 1000 microseconds
                ])
                motor["wid"] = self.pi.wave_create()
                if motor["wid"] < 0:
                    raise pigpio.error(f"Failed to create waveform for motor {motor['motor_id']}")
                print(f"Waveform created for motor {motor['motor_id']} with ID {motor['wid']}")
        except pigpio.error as e:
            print(f"Pigpio error during waveform setup: {e}")
        except Exception as e:
            print(f"Unexpected error during waveform setup: {e}")

    def motor_steps(self, motor_id, steps):
        try:
            motor = self.motor_config[motor_id]
            direction = 1 if steps > 0 else 0
            steps = abs(steps)

            self.pi.write(motor["direction_pin"], direction)
            
            num_loops = abs(steps // 256)
            remaining_steps = abs(steps % 256)
            if motor["wid"] is None:
                raise pigpio.error(f"Waveform ID for motor {motor_id} is None")
            self.pi.wave_chain([
                255, 0,                       # loop start
                motor["wid"],                 # transmit waveform
                255, num_loops, remaining_steps, 0  # loop end
            ])
            
            while self.pi.wave_tx_busy() == True:
                time.sleep(0.01)  # Wait for the wave transmission to finish
        except pigpio.error as e:
            print(f"Pigpio error during motor steps: {e}")
        except Exception as e:
            print(f"Unexpected error during motor steps: {e}")

    def stop_all_motors(self):
        self.pi.wave_tx_stop()

    def scale_value(self, gauge_id, value):
        # Retrieve the gauge configuration using the gauge_id
        gauge_config = self.motor_config[gauge_id]
        
        # Debug prints to diagnose the issue
        print(f"Scaling value: {value}")
        print(f"min_val: {gauge_config['min_val']}, max_val: {gauge_config['max_val']}")

    def calibrate_gauge(self, motor_id):
        motor = self.motor_config[motor_id]
    
        self.motor_steps(motor_id, self.MOTOR_MAX_STEPS)
        self.motor_steps(motor_id, 0)
        motor["pos"] = 0.0
        motor["calibrated"] = True

    def calibrate_all_gauges(self):
        for motor in self.motor_config:
            self.calibrate_gauge(motor["motor_id"])
        self.calibrated = True

    # Setters and Getters
    def set_motor_position(self, motor_id, position):
        self.motor_config[motor_id]["pos"] = position

    def get_motor_position(self, motor_id):
        return self.motor_config[motor_id]["pos"]

    def get_motor_calibrated(self, motor_id):
        return self.motor_config[motor_id]["calibrated"]

    def set_motor_scale_factor(self, motor_id, scale_factor):
        self.motor_config[motor_id]["scale_factor"] = scale_factor

    def get_motor_scale_factor(self, motor_id):
        return self.motor_config[motor_id]["scale_factor"]