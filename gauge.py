import time
from motor import *

class gaugeStepper:
     __current_val = 0
     __current_steps = 0
     __calibrated = False
     __m = 0
     __scale = 1.0
     __maxStep = 6000
        
     def __init__(self, name, min_val, max_val, dir_gpo, clk_gpo):
        self.name = name
        self.max_val = max_val
        self.min_val = min_val
        __current_val = min_val
        __step = 0
        __calibrated = False
        self.__m = motor(clk_gpo, dir_gpo)
        self.__m.Reset()
     
      
     # using the gauge's scaled units, work out where to move in steps and move 
     def MoveTo(self, position):
        if (position > self.max_val) :
           position = self.max_val
        elif (position < self.min_val) :
           position = self.min_val  
        delta = position - self.__current_val
        self.__m.Move(delta*self.__scale)   
        self.__current_val = position
   

     def GetPos(self):
       return(self.__current_val)
   
     def Calibrate(self):
        self.__m.Move(self.__maxStep)
        self.__m.Move(0)
        self.__current_val = self.min_val
        self.__scale = (self.__maxStep - 0)/(self.max_val - self.min_val)
        self.__calibrated = True
        print(self.__scale)
        
     def GetStatus(self):
        return(self.name, self.__current_val, self.__calibrated)
     
     def Finish(self):
        self.__m.Finish()
'''
l = gaugeStepper("consumer", -1000, 00, 3,4) 
l.Calibrate()
l.MoveTo(0)
l.MoveTo(-1000)
l.MoveTo(-250)
'''
motor_thread = MotorControlThread()
motor_thread.start()

# In other parts of your code:
motor_thread.queue.put(("calibrate", 1, {}))  # Calibrate motor 1
motor_thread.queue.put(("calibrate", 2, {}))  # Calibrate motor 2

# Move motor 1 to a specific position with parameters
move_params_motor1 = {"target_position": 100, "speed": 50}
motor_thread.queue.put(("move", 1, move_params_motor1))

# Move motor 2 to a specific position with parameters
move_params_motor2 = {"target_position": 200, "speed": 70}
motor_thread.queue.put(("move", 2, move_params_motor2))

# Don't forget to properly handle thread cleanup when your application exits.