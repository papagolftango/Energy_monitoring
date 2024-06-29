import time
from motor import Motor

class GaugeStepper:
   def __init__(self, name, min_val, max_val, id, motor):
      self.name = name
      self.max_val = max_val
      self.min_val = min_val
      self.id = id
      self.__motor = motor
      self.__current_val = min_val  # Initialize current value to min_val
      self.__current_steps = 0  # Initialize current steps to 0
      self.__calibrated = False  # Initialize calibration status to False
      self.__scale = 1.0  # Initialize scale to 1.0
      self.__max_step = 6000  # Initialize max steps to 6000

   def move_to(self, position):
      """Move the gauge to a specified position within its range."""
      if position > self.max_val:
         position = self.max_val
      elif position < self.min_val:
         position = self.min_val
      delta = position - self.__current_val
      self.__motor.move(self.id, delta * self.__scale)
      self.__current_val = position

   def get_pos(self):
      """Return the current position of the gauge."""
      return self.__current_val

   def calibrate(self):
      """Calibrate the gauge, setting its scale based on its range and max steps."""
      self.__motor.move(self.id, self.__max_step)
      self.__motor.move(self.id, 0)
      self.__current_val = self.min_val
      self.__scale = self.__max_step / (self.max_val - self.min_val)
      self.__calibrated = True
      print(f"Calibration scale set to: {self.__scale}")

   def get_status(self):
      """Return the current position and calibration status of the gauge."""
      return self.__current_val, self.__calibrated