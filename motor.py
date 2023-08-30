import time 
from pigpio import *
import threading


class MotorController:
    RESET = 26
    
    def __init__(self):
        self.pi = pigpio.pi()
        self.motor_pins = {
            1: 17,  # Motor 1: Step on GPIO 17
            2: 22,  # Motor 2: Step on GPIO 22
            3: 24,  # Motor 3: Step on GPIO 24
            4: 27   # Motor 4: Step on GPIO 27
        }
        self.pi.set_mode(self.RESET, pigpio.OUTPUT)
        self.pi1.write(self.RESET, 1)  
        self.pi1.write(self.RESET, 0) 
        time.sleep(0.01)    
        self.pi1.write(self.RESET, 1)
        
        self.setup_waveforms()
        
    def setup_waveforms(self):
        self.waveforms = {}
        for motor_id, step_pin in self.motor_pins.items():
            waveform = self.pi.wave_add_generic([
                pigpio.pulse(1 << step_pin, 0, 1000),  # Step on for 1000 microseconds
                pigpio.pulse(0, 1 << step_pin, 1000)   # Step off for 1000 microseconds
            ])
            self.waveforms[motor_id] = waveform
    
    def move_motor(self, motor_id, steps):
        num_loops = steps // 256
        remaining_steps = steps % 256
        
        self.pi.wave_chain([
            255, 0,                       # loop start
            self.waveforms[motor_id],     # transmit waveform
            255, num_loops, remaining_steps, 0  # loop end
        ])
        
        while self.pi.wave_tx_busy():
            time.sleep(0.1)
        
    def cleanup(self):
        self.pi.stop()






# Example: Move each motor by the specified number of steps using loop and wave_chain
try:
    controller = MotorController()

    controller.move_motor(motor_id=1, steps=50)
    time.sleep(0.5)

    controller.move_motor(motor_id=2, steps=100)
    time.sleep(0.5)

    controller.move_motor(motor_id=3, steps=200)
    time.sleep(0.5)

    controller.move_motor(motor_id=4, steps=2000)
    time.sleep(0.5)

except KeyboardInterrupt:
    pass

finally:
    controller.cleanup()



