import pigpio
import time

# Constants
STEP_PIN = 17  # GPIO pin for the step signal
DIRECTION_PIN = 4  # GPIO pin for the direction signal
RESET_PIN = 26  # GPIO pin for the reset signal
STEP_DELAY = 0.01  # Delay in seconds for step pulse (10ms)
RESET_DELAY = 0.01  # Delay in seconds for reset pulse (10ms)
DIRECTION = 1  # Set direction to forward (1) or backward (0)
MICROSTEPS = 8  # Microstepping setting (e.g., 1/8 microstepping)
DEGREES_PER_STEP = 0.6  # Each full step corresponds to 0.6 degree
MICROSTEPS_PER_DEGREE = (1 / DEGREES_PER_STEP) * MICROSTEPS  # Microsteps per degree
MAX_STEPS = int(300 * MICROSTEPS_PER_DEGREE)  # Maximum microsteps for 300-degree travel

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    raise Exception("Could not connect to pigpio daemon")

# Set the step, direction, and reset pins as output
pi.set_mode(STEP_PIN, pigpio.OUTPUT)
pi.set_mode(DIRECTION_PIN, pigpio.OUTPUT)
pi.set_mode(RESET_PIN, pigpio.OUTPUT)

def reset_motor():
    # Pulse the reset pin
    pi.write(RESET_PIN, 1)
    time.sleep(RESET_DELAY)
    pi.write(RESET_PIN, 0)
    time.sleep(RESET_DELAY)
    pi.write(RESET_PIN, 1)

# Initial reset
reset_motor()

def moveto(steps):
    # Set the direction based on the sign of steps
    if steps >= 0:
        pi.write(DIRECTION_PIN, 1)  # Forward
    else:
        pi.write(DIRECTION_PIN, 0)  # Backward
    
    # Create a wave for the step pulses
    pi.wave_clear()  # Clear any existing waves

    pulses = []
    for _ in range(abs(steps)):
        pulses.append(pigpio.pulse(1 << STEP_PIN, 0, int(STEP_DELAY * 1e6)))  # Step pin high
        pulses.append(pigpio.pulse(0, 1 << STEP_PIN, int(STEP_DELAY * 1e6)))  # Step pin low

    pi.wave_add_generic(pulses)  # Add the pulses to the wave
    wave_id = pi.wave_create()  # Create the wave

    if wave_id >= 0:
        pi.wave_send_once(wave_id)  # Transmit the wave
        while pi.wave_tx_busy():  # Wait for the wave to finish
            time.sleep(0.01)
        pi.wave_delete(wave_id)  # Delete the wave after transmission

try:
    # Move MAX_STEPS forward and then MAX_STEPS backward
    moveto(MAX_STEPS)
    time.sleep(1)  # Wait for 1 second
    moveto(-MAX_STEPS)
    time.sleep(1)  # Wait for 1 second
except KeyboardInterrupt:
    pass
finally:
    # Clean up on exit
    pi.write(STEP_PIN, 0)
    pi.write(DIRECTION_PIN, 0)
    pi.write(RESET_PIN, 0)
    pi.stop()