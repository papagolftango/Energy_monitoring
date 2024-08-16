class Gauge:
    def __init__(self, motor, motor_name, motor_id, min_val, max_val):
        self.motor = motor
        self.name = motor_name
        self.motor_id = motor_id
        self.min_val = min_val
        self.max_val = max_val
        self.pos = 0  # Ensure position is initialized as an integer

    def move_to(self, target_position):
        print(target_position)
        steps = target_position - self.pos
        self.motor.move(self.motor_id, steps)
        self.pos = target_position  # Update position to the new target

    def get_position(self):
        return self.pos

    def calibrate(self):
        # Move to max position
        self.motor.move(self.motor_id, self.max_val)
  
        # Move back to min position (0)
        self.motor.move(self.motor_id, self.min_val)
        self.calibrated = True

    def is_calibrated(self):
        return self.calibrated
    
    def min_value(self):
        return self.min_val 
       
    def max_value(self):
        return self.max_val