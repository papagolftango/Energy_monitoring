import time
from motor import *

class gaugeStepper:
     __current_val = 0
     __steps = 0
     __calibrated = False
     __m = 0
        
     def __init__(self, name, min_val, max_val, dir_gpo, clk_gpo):
        self.name = name
        self.max_val = max_val
        self.min_val = min_val
        __current_val = min_val
        __step = 0
        __calibrated = False
        self.__m = motor(clk_gpo, dir_gpo)
        self.__m.Reset()
     
   
     def MoveTo(self, position):
        if (position > self.max_val) :
           position = self.max_val
        elif (position < self.min_val) :
           position = self.min_val  
        delta = position - self.__current_val
        self.__m.Move(delta)   
        self.__current_val = position

     def GetPos(self):
       return(self.__current_val)
   
     def Calibrate(self):
        self.MoveTo(self.max_val)
        self.MoveTo(self.min_val)
        self.__calibrated = True
        
     def GetStatus(self):
        return(self.name, self.__current_val, self.__calibrated)
     
     def Finish(self):
        self.__m.Finish()


