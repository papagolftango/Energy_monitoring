import pigpio
import time

# Constants
STEP_PIN = 17  # GPIO pin for the step signal
NUM_STEPS = 1000  # Number of steps to send

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    raise Exception("Could not connect to pigpio daemon")

# Set the step pin as output
pi.set_mode(STEP_PIN, pigpio.OUTPUT)

def send_steps(step_pin, num_steps):
    """
    Generate and send waveforms to step the motor.
    :param step_pin: GPIO pin for the step signal
    :param num_steps: Number of steps to send
    """
    try:
        # Clear any existing waveforms
        pi.wave_clear()

        # Create pulses for the waveform
        pulses = []
        for _ in range(num_steps):
            pulses.append(pigpio.pulse(1 << step_pin, 0, 1000))  # Step on for 1000 microseconds
            pulses.append(pigpio.pulse(0, 1 << step_pin, 1000))  # Step off for 1000 microseconds

        # Add the pulses to the waveform
        pi.wave_add_generic(pulses)

        # Create the waveform
        wave_id = pi.wave_create()
        if wave_id < 0:
            raise pigpio.error("Failed to create waveform")

        # Send the waveform
        pi.wave_send_once(wave_id)

        # Wait for the waveform to finish
        while pi.wave_tx_busy():
            time.sleep(0.1)

        # Clear the waveform
        pi.wave_clear()

        print(f"Sent {num_steps} steps to the motor on GPIO pin {step_pin}")

    except pigpio.error as e:
        print(f"Pigpio error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# Send the steps
send_steps(STEP_PIN, NUM_STEPS)

# Cleanup
pi.stop()