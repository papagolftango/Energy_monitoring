import time
from motor import *
<<<<<<< HEAD
import bme280

class Gauge:
=======

class gaugeStepper:
>>>>>>> 47adc234579e7703c6a6b156c1ed253359da6c65
     __current_val = 0
     __current_steps = 0
     __calibrated = False
     __m = 0
     __scale = 1.0
     __maxStep = 6000
        
     def __init__(self, name, min_val, max_val, id, m):
        self.name = name
        self.max_val = max_val
        self.min_val = min_val
        self.id = id
        self.__m = m
        __current_val = min_val
        __step = 0
        __calibrated = False
       # self.__m.Reset()
     
      
     # using the gauge's scaled units, work out where to move in steps and move 
     def MoveTo(self, position):
        if (position > self.max_val) :
           position = self.max_val
        elif (position < self.min_val) :
           position = self.min_val  
        delta = position - self.__current_val
        self.__m.move(self.id,delta*self.__scale)   
        self.__current_val = position
<<<<<<< HEAD
<<<<<<< HEAD
        
=======
=======
   
>>>>>>> 0ec8422ec555921e3e20431fd9697bd117686bdf

     def GetPos(self):
       return(self.__current_val)
   
>>>>>>> 47adc234579e7703c6a6b156c1ed253359da6c65
     def Calibrate(self):
        self.__m.move(self.id, self.__maxStep)
        self.__m.move(self.id, 0)
        self.__current_val = self.min_val
        self.__scale = (self.__maxStep - 0)/(self.max_val - self.min_val)
        self.__calibrated = True
        print(self.__scale)
        
     def GetStatus(self):
<<<<<<< HEAD
        return(self.__current_val, self.__calibrated)



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
=======
        return(self.name, self.__current_val, self.__calibrated)
     
     def Finish(self):
        self.__m.Finish()

<<<<<<< HEAD
>>>>>>> 47adc234579e7703c6a6b156c1ed253359da6c65
=======
m = Motor()
l = gaugeStepper("consumer", -1000, 00, 0, m) 
l.MoveTo(0)
l.MoveTo(-1000)
l.MoveTo(-250)



>>>>>>> 0ec8422ec555921e3e20431fd9697bd117686bdf
