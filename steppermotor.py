import time
import pigpio
import subprocess
import sys
import select

class StepperMotor:
    MOTOR_MAX_STEPS = 3600  # Example value, adjust as needed
    MOTOR_CONFIGS = [
        {"direction_pin": 4, "step_pin": 17},
        {"direction_pin": 22, "step_pin": 18},
        {"direction_pin": 23, "step_pin": 24},
        {"direction_pin": 27, "step_pin": 25}
    ]

    def __init__(self):
        self.pi = pigpio.pi()
        self.is_calibrated_flag = False
        self.reset_pin = 26  # Global reset pin
        self.positions = [0] * len(self.MOTOR_CONFIGS)  # Initialize motor positions

        # Check if pigpio daemon is running
        if not self.pi.connected:
            print("pigpio daemon is not running. Starting it now...")
            subprocess.run(["sudo", "systemctl", "start", "pigpiod"])
            self.pi = pigpio.pi()
            if not self.pi.connected:
                raise Exception("Could not connect to pigpio daemon")

        # Set up the GPIO pins for each motor
        for motor in self.MOTOR_CONFIGS:
            self.pi.set_mode(motor['step_pin'], pigpio.OUTPUT)
            self.pi.set_mode(motor['direction_pin'], pigpio.OUTPUT)

        # Set up the reset pin
        self.pi.set_mode(self.reset_pin, pigpio.OUTPUT)
        self.reset()

        self.setup_waveform()

    def reset(self):
        """
        Pulse the /reset line (active low) to reset the motor driver.
        """
        self.pi.write(self.reset_pin, 1)  # Set /reset line to high
        time.sleep(0.1)  # Wait for 100 milliseconds
        self.pi.write(self.reset_pin, 0)  # Set /reset line to low
        time.sleep(0.1)  # Wait for 100 milliseconds
        self.pi.write(self.reset_pin, 1)  # Set /reset line to high
        time.sleep(0.1)  # Wait for 100 milliseconds

    def setup_waveform(self):
        try:
            self.pi.wave_clear()  # Clear any existing waveforms

            # Create waveforms for each motor
            self.wave_ids = []
            for motor in self.MOTOR_CONFIGS:
                wave_id = self.create_waveform(motor['step_pin'])
                self.wave_ids.append(wave_id)

            if any(wave_id < 0 for wave_id in self.wave_ids):
                raise pigpio.error("Failed to create one or more waveforms")

        except pigpio.error as e:
            print(f"Pigpio error during waveform setup: {e}")
        except Exception as e:
            print(f"Unexpected error during waveform setup: {e}")

    def create_waveform(self, pin):
        self.pi.wave_add_generic([
            pigpio.pulse(1 << pin, 0, 100),  # Step on for 500 microseconds
            pigpio.pulse(0, 1 << pin, 100)   # Step off for 500 microseconds
        ])
        return self.pi.wave_create()

    def moveto(self, steps_motor_0, steps_motor_1, steps_motor_2, steps_motor_3):
        """
        Move all motors simultaneously based on the provided steps for each motor.
        :param steps_motor_0: Steps for motor 0
        :param steps_motor_1: Steps for motor 1
        :param steps_motor_2: Steps for motor 2
        :param steps_motor_3: Steps for motor 3
        """
        try:
            steps_list = [steps_motor_0, steps_motor_1, steps_motor_2, steps_motor_3]
    
            wave_chain = []
    
            for motor_id, steps in enumerate(steps_list):
                if steps == 0:
                    continue  # Skip motors with zero steps
    
                motor = self.MOTOR_CONFIGS[motor_id]
                direction = 1 if steps > 0 else 0
                self.pi.write(motor['direction_pin'], direction)
    
                steps = abs(steps)
                num_loops = steps // 256
                remaining_steps = steps % 256
                wave_id = self.wave_ids[motor_id]
                if wave_id is None:
                    raise pigpio.error(f"Waveform ID for motor {motor_id} is None")
    
                # Add the waveforms for the motor
                wave_chain.extend([255, 0, wave_id, 255, 1, remaining_steps, num_loops, 0])
    
                # Update the motor position
                self.positions[motor_id] += steps if direction == 1 else -steps
    
            print(f"Wave chain: {wave_chain}")
            self.pi.wave_chain(wave_chain)
    
            while self.pi.wave_tx_busy():  # Wait for the wave to finish
                time.sleep(0.01)
        except pigpio.error as e:
            print(f"Pigpio error during movement: {e}")
        except Exception as e:
            print(f"Unexpected error during movement: {e}")
            
    def calibrate_all(self):
        """
        Calibrate all motors simultaneously by moving them to the maximum steps and then back to zero.
        """
        try:
            # Move all motors to the maximum steps
            self.moveto(self.MOTOR_MAX_STEPS, self.MOTOR_MAX_STEPS, self.MOTOR_MAX_STEPS, self.MOTOR_MAX_STEPS)
            # Wait for the movement to complete
            while self.pi.wave_tx_busy():
                time.sleep(0.01)

            # Move all motors back to zero
            self.moveto(-self.MOTOR_MAX_STEPS, -self.MOTOR_MAX_STEPS, -self.MOTOR_MAX_STEPS, -self.MOTOR_MAX_STEPS)
            # Wait for the movement to complete
            while self.pi.wave_tx_busy():
                time.sleep(0.01)

            # Set all motor positions to zero
            self.positions = [0] * len(self.MOTOR_CONFIGS)
            self.is_calibrated_flag = True
            print("Calibration complete for all motors. All positions set to zero.")
        except pigpio.error as e:
            print(f"Pigpio error during calibration of all motors: {e}")
        except Exception as e:
            print(f"Unexpected error during calibration of all motors: {e}")

    def cleanup(self):
        self.pi.stop()

    def get_max_steps(self):
        return self.MOTOR_MAX_STEPS
    
    def get_num_motors(self):
        return len(self.MOTOR_CONFIGS)

# Test code
if __name__ == "__main__":
    stepper_motor = StepperMotor()

    while True:
        # Calibrate all motors
        stepper_motor.calibrate_all()

        # Move all motors to position 0
        stepper_motor.moveto(0, 0, 0, 0)

        # Individually move each motor 360 steps at a time until max steps is reached
        num_motors = stepper_motor.get_num_motors()
        for i in range(num_motors):
            current_position = 0
            while current_position < stepper_motor.get_max_steps():
                # List comprehension to generate positions
                # Move motor i to 360 steps, others to 0
                positions = [360 if j == i else 0 for j in range(num_motors)]
                stepper_motor.moveto(*positions)
                current_position += 360
            # Move motor back to 0 after reaching max steps
            stepper_motor.moveto(0, 0, 0, 0)

        # Add a delay between iterations if needed
        time.sleep(1)