import time
import pigpio
import subprocess

class StepperMotor:
    MOTOR_MAX_STEPS = 6000  # Example value, adjust as needed
    MOTOR_CONFIGS = [
        {"direction_pin": 5, "step_pin": 17},
        {"direction_pin": 6, "step_pin": 23},
        {"direction_pin": 13, "step_pin": 24},
        {"direction_pin": 19, "step_pin": 27}
    ]

    def __init__(self):
        self.pi = pigpio.pi()
        self.is_calibrated_flag = False
        self.reset_pin = 26  # Global reset pin

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

        # Accessing the waveform ID for the second motor (index 1)
        second_motor_waveform_id = self.wave_ids[1]
        print(f"Waveform ID for the second motor: {second_motor_waveform_id}")

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
            pigpio.pulse(1 << pin, 0, 500),  # Step on for 500 microseconds
            pigpio.pulse(0, 1 << pin, 500)   # Step off for 500 microseconds
        ])
        return self.pi.wave_create()

    def moveto(self, steps_list):
        """
        Move all motors simultaneously based on the provided steps list.
        :param steps_list: List of steps for each motor [steps_motor_0, steps_motor_1, steps_motor_2, steps_motor_3]
        """
        try:
            if len(steps_list) != len(self.MOTOR_CONFIGS):
                raise ValueError("The steps_list must have the same length as the number of motors")

            wave_chain = []

            for motor_id, steps in enumerate(steps_list):
                motor = self.MOTOR_CONFIGS[motor_id]
                direction = 1 if steps > 0 else 0
                self.pi.write(motor['direction_pin'], direction)

                steps = abs(steps)
                num_loops = steps // 256
                remaining_steps = steps % 256
                wave_id = self.wave_ids[motor_id]
                if wave_id is None:
                    raise pigpio.error(f"Waveform ID for motor {motor_id} is None")

                wave_chain.extend([
                    255, 0,                       # loop start
                    wave_id,                      # transmit waveform
                    255, 1, remaining_steps, num_loops, 0  # loop end
                ])

            self.pi.wave_chain(wave_chain)

            while self.pi.wave_tx_busy():  # Wait for the wave to finish
                time.sleep(0.01)
        except pigpio.error as e:
            print(f"Pigpio error during movement: {e}")
        except Exception as e:
            print(f"Unexpected error during movement: {e}")

# Test code
if __name__ == "__main__":
    stepper_motor = StepperMotor()
    
    # Move all motors to MOTOR_MAX_STEPS
    steps_list = [
        StepperMotor.MOTOR_MAX_STEPS,  # Motor 0
        StepperMotor.MOTOR_MAX_STEPS,  # Motor 1
        StepperMotor.MOTOR_MAX_STEPS,  # Motor 2
        StepperMotor.MOTOR_MAX_STEPS   # Motor 3
    ]
    print("Moving all motors to MOTOR_MAX_STEPS...")
    stepper_motor.moveto(steps_list)
    
    # Move all motors to -MOTOR_MAX_STEPS
    steps_list = [
        -StepperMotor.MOTOR_MAX_STEPS,  # Motor 0
        -StepperMotor.MOTOR_MAX_STEPS,  # Motor 1
        -StepperMotor.MOTOR_MAX_STEPS,  # Motor 2
        -StepperMotor.MOTOR_MAX_STEPS   # Motor 3
    ]
    print("Moving all motors to -MOTOR_MAX_STEPS...")
    stepper_motor.moveto(steps_list)