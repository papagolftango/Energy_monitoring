import pigpio
import time

# Constants
LED_PIN = 4  # GPIO pin for the LED
BLINK_DELAY = 1  # Delay in seconds

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    raise Exception("Could not connect to pigpio daemon")

# Set the LED pin as output
pi.set_mode(LED_PIN, pigpio.OUTPUT)

try:
    while True:
        # Turn the LED on
        pi.write(LED_PIN, 1)
        time.sleep(BLINK_DELAY)
        
        # Turn the LED off
        pi.write(LED_PIN, 0)
        time.sleep(BLINK_DELAY)
except KeyboardInterrupt:
    # Clean up on exit
    pi.write(LED_PIN, 0)
    pi.stop()