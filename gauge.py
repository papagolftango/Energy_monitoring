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
        self.__scale = (self.__maxStep - 0)/(self.max_val - self.min_val)
        self.__calibrated = True
        
     def GetStatus(self):
        return(self.name, self.__current_val, self.__calibrated)
     
     def Finish(self):
        self.__m.Finish()


