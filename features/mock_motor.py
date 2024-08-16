class MockMotor:
    def __init__(self):
        self.position = 0
        self.calibrated = False

    def initialize(self):
        self.calibrated = False

    def calibrate(self):
        self.calibrated = True

    def move(self, motor_id, position):
        print("here in mock motor")

        if position > 6000:
            self.position = 6000
        elif position < 0:
            self.position = 0
        else:
            self.position = position

    def get_position(self):
        return self.position