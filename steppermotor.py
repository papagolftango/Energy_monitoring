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
            pigpio.pulse(1 << pin, 0, 250),  # Step on for 500 microseconds
            pigpio.pulse(0, 1 << pin, 250)   # Step off for 500 microseconds
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
            target_positions = [target_motor_0, target_motor_1, target_motor_2, target_motor_3]
            steps_list = []

            # Calculate relative movement for each motor ie demand - curren_position
            for i, target in enumerate(target_positions):
                current_position = self.current_positions[i]
                steps = target - current_position
                steps_list.append(steps)

            # Sort motors by steps (lowest 1st) and discard those with no steps required
            motors_steps = sorted([(i, steps) for i, steps in enumerate(steps_list) if steps != 0], key=lambda x: abs(x[1]))

            wave_chain = []    
            previous_steps = 0
            for i, (motor_id, steps) in enumerate(motors_steps):
                motor = self.MOTOR_CONFIGS[motor_id]
                direction = 1 if steps > 0 else 0
                self.pi.write(motor['direction_pin'], direction)
    
                steps = abs(steps)
                move_steps = steps - previous_steps
                previous_steps = steps
    
                num_loops = move_steps // 256
                remaining_steps = move_steps % 256
                wave_id = self.wave_ids[motor_id]
                if wave_id is None:
                    raise pigpio.error(f"Waveform ID for motor {motor_id} is None")
    
                # Add the waveforms for the current motor and all subsequent motors
                if move_steps > 0:
                    wave_chain.extend([255, 0])
                    for j, (mid, _) in enumerate(motors_steps[i:]):
                        wave_chain.append(self.wave_ids[mid])
                    wave_chain.extend([255, 1, remaining_steps, num_loops, 0])
    
                # Update the motor position
                self.positions[motor_id] += move_steps if direction == 1 else -move_steps
    
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

    

    def get_positions(self):
        """
        Get the current positions of all motors.
        :return: List of current positions for each motor.
        """
        return self.positions

    # Existing methods...
    def cleanup(self):
        self.pi.stop()

    def get_max_steps(self):
        return self.MOTOR_MAX_STEPS
    
    def get_num_motors(self):
        return len(self.MOTOR_CONFIGS)

# Test code
if __name__ == "__main__":
     
    stepper_motor = StepperMotor()

    # Calibrate all motors
    stepper_motor.calibrate_all()

    while True:
        try:
            # Prompt the user for input of four numbers
            user_input = input("Enter four numbers separated by spaces (e.g., 100 200 300 400): ")
            steps = list(map(int, user_input.split()))

            if len(steps) != 4:
                print("Please enter exactly four numbers.")
                continue

            # Move motors to the specified positions
            stepper_motor.moveto(*steps)

            # Print current positions
            print(f"Current positions: {stepper_motor.get_positions()}")

            # Add a delay between iterations if needed
            time.sleep(1)

        except ValueError:
            print("Invalid input. Please enter four valid integers.")
        except KeyboardInterrupt:
            print("Exiting...")
            break