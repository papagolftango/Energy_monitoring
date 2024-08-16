
class GaugeStepper:
    def __init__(self, motor, motorName, motor_id, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val
        self.motor = motor
        self.motor_id = motor_id
        self.position = self.motor.get_position(motor_id)
        self.calibrated = False

    def move_to(self, value):
        if value < self.min_val:
            target_position = self.min_val
        elif value > self.max_val:
            target_position = self.max_val
        else:
            target_position = value

        steps = target_position - self.position
        self.motor.move(self.motor_id, steps)
        self.position = self.motor.get_position(self.motor_id)

    def get_position(self):
        return self.motor.get_position(self.motor_id)

    def calibrate(self):
        # Move to max position
        steps_to_max = self.max_val - self.position
        self.motor.move(self.motor_id, steps_to_max)
        self.position = self.motor.get_position(self.motor_id)

        # Move back to min position (0)
        steps_to_min = self.min_val - self.position
        self.motor.move(self.motor_id, steps_to_min)
        self.position = self.motor.get_position(self.motor_id)

        self.calibrated = True