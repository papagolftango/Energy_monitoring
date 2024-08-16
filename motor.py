import pigpio
import time

class Motor:
    MAX_MOTOR_STEPS = 6000  # Example value, replace with actual max steps

    def __init__(self, pi, motors):
        self.pi = pi
        self.motors = motors
        self.RESET = 17  # Example GPIO pin for reset
        self.wid = [None] * len(motors)  # Initialize waveform IDs

        self.pi.set_mode(self.RESET, pigpio.OUTPUT)
        self.pi.write(self.RESET, 1)  
        self.pi.write(self.RESET, 0) 
        time.sleep(0.01)    
        self.pi.write(self.RESET, 1)
        
        self.setup_waveforms()
        
    def setup_waveforms(self):
        for motor in self.motors:
            waveform = self.pi.wave_add_generic([
                pigpio.pulse(1 << motor["step_pin"], 0, 1000),  # Step on for 1000 microseconds
                pigpio.pulse(0, 1 << motor["step_pin"], 1000)   # Step off for 1000 microseconds
            ])
            motor["wid"] = self.pi.wave_create()
    
    def move(self, motor_id, steps):
        print("motor")
        if steps >= 0:
            self.pi.write(self.motors[motor_id]["dir_pin"], 0)  # Set direction pin low for forward
        else:
            self.pi.write(self.motors[motor_id]["dir_pin"], 1)

        num_loops = abs(steps // 256)
        remaining_steps = abs(steps % 256)
        self.pi.wave_chain([
            255, 0,                       # loop start
            self.wid[motor_id],           # transmit waveform
            255, num_loops, remaining_steps, 0  # loop end
        ])
        
        while self.pi.wave_tx_busy():
            time.sleep(0.01)  # Wait for the wave transmission to finish

    def get_max_steps(self):
        return self.MAX_MOTOR_STEPS

 


