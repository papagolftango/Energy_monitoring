import time
import pigpio
import subprocess

class StepperMotor:
    MOTOR_MAX_STEPS = 200  # Example value, adjust as needed
    def __init__(self, step_pin, direction_pin):
        self.step_pin = step_pin
        self.direction_pin = direction_pin
        self.pi = pigpio.pi()
        self.is_calibrated_flag = False

        # Check if pigpio daemon is running
        if not self.pi.connected:
            print("pigpio daemon is not running. Starting it now...")
            subprocess.run(["sudo", "systemctl", "start", "pigpiod"])
            self.pi = pigpio.pi()
            if not self.pi.connected:
                raise Exception("Could not connect to pigpio daemon")

        # Set up the GPIO pins
        self.pi.set_mode(self.step_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.direction_pin, pigpio.OUTPUT)
        self.setup_waveform()
        self.pi.set_mode(26, pigpio.OUTPUT)
        self.pi.write(26, 1)
        time.sleep(0.1)
        self.pi.write(26, 0)
        time.sleep(0.1)
        self.pi.write(26, 1) 
        
    def setup_waveform(self):
        try:
            self.pi.wave_clear()  # Clear any existing waveforms
            self.pi.wave_add_generic([
                pigpio.pulse(1 << self.step_pin, 0, 1000),  # Step on for 1000 microseconds
                pigpio.pulse(0, 1 << self.step_pin, 1000)   # Step off for 1000 microseconds
            ])
            self.wid = self.pi.wave_create()
            if self.wid < 0:
                raise pigpio.error(f"Failed to create waveform for motor")
        except pigpio.error as e:
            print(f"Pigpio error during waveform setup: {e}")
        except Exception as e:
            print(f"Unexpected error during waveform setup: {e}")

    def moveto(self, steps):
        try:
            direction = 1 if steps > 0 else 0
            self.pi.write(self.direction_pin, direction)

            steps = abs(steps) 
            num_loops = abs(steps // 256)
            remaining_steps = abs(steps % 256)
            if self.wid is None:
                raise pigpio.error(f"Waveform ID for motor is None")
            self.pi.wave_chain([
                255, 0,                       # loop start
                self.wid,                     # transmit waveform
                255, 1, remaining_steps, num_loops, 0  # loop end
            ])
            while self.pi.wave_tx_busy():  # Wait for the wave to finish
                time.sleep(0.01)
        except pigpio.error as e:
            print(f"Pigpio error during movement: {e}")
        except Exception as e:
            print(f"Unexpected error during movement: {e}")

    def cleanup(self):
        self.pi.wave_clear()
        self.pi.stop()

# Example usage
if __name__ == "__main__":
    motor1 = StepperMotor(step_pin=17, direction_pin=4)
    motor2 = StepperMotor(step_pin=18, direction_pin=22)
    motor3 = StepperMotor(step_pin=23, direction_pin=24)
    motor4 = StepperMotor(step_pin=26, direction_pin=27)
    try:
        while True:
            motor1.moveto(512)  # Move 512 steps forward
            time.sleep(1)      # Wait for 1 second
            motor1.moveto(-512) # Move 512 steps backward
            time.sleep(1)      # Wait for 1 second
            motor2.moveto(512)  # Move 512 steps forward
            time.sleep(1)      # Wait for 1 second
            motor2.moveto(-512) # Move 512 steps backward
            time.sleep(1)      # Wait for 1 second
            motor3.moveto(512)  # Move 512 steps forward
            time.sleep(1)      # Wait for 1 second
            motor3.moveto(-512) # Move 512 steps backward
            time.sleep(1)      # Wait for 1 second
            motor4.moveto(512)  # Move 512 steps forward
            time.sleep(1)      # Wait for 1 second
            motor4.moveto(-512) # Move 512 steps backward
            time.sleep(1)      # Wait for 1 second

    except KeyboardInterrupt:
        pass
    finally:
        motor.cleanup()