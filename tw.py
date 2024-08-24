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

		# Maximum number of steps per waveform
		MAX_STEPS_PER_WAVEFORM = 256

		# Create pulses for the waveform
		pulses = []
		for _ in range(MAX_STEPS_PER_WAVEFORM):
			pulses.append(pigpio.pulse(1 << step_pin, 0, 1000))  # Step on for 1000 microseconds
			pulses.append(pigpio.pulse(0, 1 << step_pin, 1000))  # Step off for 1000 microseconds

		# Add the pulses to the waveform
		pi.wave_add_generic(pulses)
		wave_id = pi.wave_create()
		if wave_id < 0:
			raise pigpio.error("Failed to create waveform")

		# Calculate the number of full waveforms and remaining steps
		full_waveforms = num_steps // MAX_STEPS_PER_WAVEFORM
		remaining_steps = num_steps % MAX_STEPS_PER_WAVEFORM

		# Create the wave chain
		wave_chain = [255, 0]  # Loop start
		wave_chain += [wave_id] * full_waveforms  # Add full waveforms
		if remaining_steps > 0:
			# Create a waveform for the remaining steps
			remaining_pulses = []
			for _ in range(remaining_steps):
				remaining_pulses.append(pigpio.pulse(1 << step_pin, 0, 1000))  # Step on for 1000 microseconds
				remaining_pulses.append(pigpio.pulse(0, 1 << step_pin, 1000))  # Step off for 1000 microseconds
			pi.wave_add_generic(remaining_pulses)
			remaining_wave_id = pi.wave_create()
			if remaining_wave_id < 0:
				raise pigpio.error("Failed to create remaining waveform")
			wave_chain.append(remaining_wave_id)
		wave_chain += [255, 1, 0]  # Loop end

		# Send the wave chain
		pi.wave_chain(wave_chain)

		# Wait for the wave transmission to finish
		while pi.wave_tx_busy():
			time.sleep(0.01)

		# Clear the waveforms
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
