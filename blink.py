import pigpio
import time

# Constants
STEP_PIN = 17  # GPIO pin for the step signal
DIRECTION_PIN = 5  # GPIO pin for the direction signal
RESET_PIN = 26  # GPIO pin for the reset signal
STEP_DELAY = 0.1  # Delay in seconds for step pulse (100ms)
RESET_DELAY = 0.01  # Delay in seconds for reset pulse (10ms)
DIRECTION = 1  # Set direction to forward (1) or backward (0)

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    raise Exception("Could not connect to pigpio daemon")

# Set the step, direction, and reset pins as output
pi.set_mode(STEP_PIN, pigpio.OUTPUT)
pi.set_mode(DIRECTION_PIN, pigpio.OUTPUT)
pi.set_mode(RESET_PIN, pigpio.OUTPUT)

# Pulse the reset pin
pi.write(RESET_PIN, 1)
time.sleep(RESET_DELAY)
pi.write(RESET_PIN, 0)

# Set the direction pin
pi.write(DIRECTION_PIN, DIRECTION)

def moveto(steps):
    # Set the direction based on the sign of steps
    if steps >= 0:
        pi.write(DIRECTION_PIN, 1)  # Forward
    else:
        pi.write(DIRECTION_PIN, 0)  # Backward
    
    # Move the absolute value of steps
    for _ in range(abs(steps)):
        # Generate a step pulse
        pi.write(STEP_PIN, 1)
        time.sleep(STEP_DELAY)
        pi.write(STEP_PIN, 0)
        time.sleep(STEP_DELAY)

try:
    # Example usage: move 500 steps forward and 500 steps backward
    moveto(500)
    time.sleep(1)  # Wait for 1 second
    moveto(-500)
except KeyboardInterrupt:
    pass
finally:
    # Clean up on exit
    pi.write(STEP_PIN, 0)
    pi.write(DIRECTION_PIN, 0)
    pi.write(RESET_PIN, 0)
    pi.stop()