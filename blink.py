import pigpio
import time

# Constants
LED_PIN_1 = 5  # GPIO pin for the first LED
LED_PIN_2 = 6  # GPIO pin for the second LED
BLINK_DELAY = 1  # Delay in seconds

# Initialize pigpio
pi = pigpio.pi()
if not pi.connected:
    raise Exception("Could not connect to pigpio daemon")

# Set the LED pins as output
pi.set_mode(LED_PIN_1, pigpio.OUTPUT)
pi.set_mode(LED_PIN_2, pigpio.OUTPUT)

try:
    while True:
        # Turn the first LED on and the second LED off
        pi.write(LED_PIN_1, 1)
        pi.write(LED_PIN_2, 0)
        time.sleep(BLINK_DELAY)
        
        # Turn the first LED off and the second LED on
        pi.write(LED_PIN_1, 0)
        pi.write(LED_PIN_2, 1)
        time.sleep(BLINK_DELAY)
except KeyboardInterrupt:
    # Clean up on exit
    pi.write(LED_PIN_1, 0)
    pi.write(LED_PIN_2, 0)
    pi.stop()