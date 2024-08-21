class Gauge:
    def __init__(self, motor, motor_id, min_val, max_val):
        self.motor = motor
  
        self.motor_id = motor_id
        self.min_val = float(min_val)
        self.max_val = float(max_val)
        self.pos = 0  # Ensure position is initialized as an integer
        self.max_steps = self.motor.get_max_steps()
        if not isinstance(self.max_steps, (int, float)):
            raise TypeError("max_steps must be a numeric value.")
        self.calibrated = False

    def scale_value(self, value):
        # Debug prints to diagnose the issue
        print(f"Scaling value: {value}")
        print(f"min_val: {self.min_val}, max_val: {self.max_val}, max_steps: {self.max_steps}")
        
        # Check for division by zero
        if self.max_val == self.min_val:
            raise ValueError("max_val and min_val cannot be the same value.")
        
        # Scale the value to the range of 0 to max_steps
        scaled_value = int((value - self.min_val) / (self.max_val - self.min_val) * float(self.max_steps))
        print(f"Scaled value: {scaled_value}")
        return scaled_value

    def move_to(self, target_position):
        print(f"Moving to target position: {target_position}")
        
        # Clamp target_position within min_val and max_val
        if target_position > self.max_val:
            target_position = self.max_val
        elif target_position < self.min_val:
            target_position = self.min_val
        scaled_target = self.scale_value(target_position)
        steps = scaled_target - self.pos
        self.motor.move(self.motor_id, steps)
        self.pos = target_position  # Update position to the new target
        print(f"Current position after move: {self.pos}")

    def get_position(self):
        return self.pos

    def calibrate(self):
        # Move to max position
        max_steps = self.scale_value(self.max_val)
        self.motor.move(self.motor_id, max_steps)
        # Move back to min position (0)
        self.motor.move(self.motor_id, -max_steps)
        self.pos = 0  # Reset position to min value
        self.calibrated = True
        print("Calibration complete. Current position reset to 0.")

    def is_calibrated(self):
        return self.calibrated

    def max_value(self):
        return self.max_val

    def min_value(self):
        return self.min_val  