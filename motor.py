import sys
import time 
if 'unittest' not in sys.modules:
    import pigpio

class Motor:
    RESET = 26

    def __init__(self):
        self.wid = [0]*4
        self.pi = pigpio.pi()
        self.motors = [
            {"step_pin": 17, "dir_pin": 23, "wid": self.wid[0], "position": 0},
            {"step_pin": 18, "dir_pin": 24, "wid": self.wid[1], "position": 0},
            {"step_pin": 27, "dir_pin": 2, "wid": self.wid[2], "position": 0},
            {"step_pin": 22, "dir_pin": 5, "wid": self.wid[3], "position": 0}
        ]

        for motor in self.motors:
            self.pi.set_mode(motor["step_pin"], pigpio.OUTPUT)
            self.pi.set_mode(motor["dir_pin"], pigpio.OUTPUT)
            self.pi.write(motor["step_pin"], 0)  # Set initial state to low
            self.pi.write(motor["dir_pin"], 0)   # Set initial direction to forward

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
           # self.waveforms[motor] = waveform
            motor["wid"] = self.pi.wave_create();
    
    def move(self, motor_id, steps):
        if steps >= 0:
            self.pi.write(self.motors[motor_id]["dir_pin"], 0)  # Set direction pin low for forward
        else:
            self.pi.write(self.motors[motor_id]["dir_pin"], 1)

        num_loops = abs(steps // 256)
        remaining_steps = abs(steps % 256)
        self.pi.wave_chain([
            255, 0,                       # loop start
            self.wid[motor_id],     # transmit waveform
            255, num_loops, remaining_steps, 0  # loop end
        ])
        
        while self.pi.wave_tx_busy():
            time.sleep(0.1)
                # Update the position

        self.motors[motor_id]["position"] += steps

    def Finish(self):
        self.pi.stop()


    def get_position(self, motor_id):
        if motor_id < 0 or motor_id >= len(self.motors):
            raise ValueError("Invalid motor_id")
        return self.motors[motor_id]["position"]




