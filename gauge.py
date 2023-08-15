import time
from motor import *

class Gauge:
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
        
     def Calibrate(self):
        self.MoveTo(self.max_val)
        self.MoveTo(self.min_val)
        self.__calibrated = True
        
     def GetStatus(self):
        return(self.name, self.__current_val, self.__calibrated)
     
     def Finish(self):
        self.__m.Finish()

'''

l = Gauge("consumer", 0, 6000, 3,4)
m = Gauge("consumer", 0, 6000, 5,6)
n = Gauge("consumer", 0, 6000, 7,8)
o = Gauge("consumer", 0, 6000, 9,10)
l.Calibrate()
m.Calibrate()
n.Calibrate()
o.Calibrate()
x,y = l.GetStatus()
print(x,y)
l.MoveTo(2400)
l.MoveTo(2000)

 
(chip_id, chip_version) = bme280.readBME280ID()
print ("Chip ID :", chip_id)
print ("Version :", chip_version)
 
temperature,pressure,humidity = bme280.readBME280All()
 
print ("Temperature : ", temperature, "C")
print ("Pressure : ", pressure, "hPa")
print ("Humidity : ", humidity, "%")

'''