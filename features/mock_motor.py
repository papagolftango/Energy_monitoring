class MockMotor:

    MAX_MOTOR_STEPS = 6000

    def __init__(self):
        print("here in mock motor")
        self.position = 0
        self.calibrated = False

    def move(self, motor_id, position):
        print("here in mock motor")

        if position > MockMotor.MAX_MOTOR_STEPS:
            self.position = MockMotor.MAX_MOTOR_STEPS
        elif position < 0:
            self.position = 0
        else:
            self.position = position

    def get_position(self):
        return self.position
    
    def get_max_steps(self):
        print("MAX_STEPS", MockMotor.MAX_MOTOR_STEPS)
        return(MockMotor.MAX_MOTOR_STEPS)

    