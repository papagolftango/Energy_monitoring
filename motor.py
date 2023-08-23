import time 
from pigpio import *

class motor :
  RESET = 26
  onTime = 400
  offTime = 600
  wid=0
  pi1=0
  clk =0
  diection=0
  wf=[]

  def __init__(self, Clk, Direction) :  
    self.clk = Clk
    self.direction = Direction
    self.pi1 = pigpio()
    self.pi1.set_mode(self.clk, pigpio.OUTPUT)
    self.pi1.set_mode(self.direction, pigpio.OUTPUT)
    self.pi1.set_mode(self.RESET, pigpio.OUTPUT)
    self.pi1.write(self.direction, 1)  
 
    self.wf.append(pigpio.pulse(gpio_on=(1<<self.clk), gpio_off=0, delay=self.onTime))     # get required timings
    self.wf.append(pigpio.pulse(gpio_on=0, gpio_off=(1<<self.clk), delay=self.offTime))

    self.pi1.wave_clear()
    self.pi1.wave_add_generic(self.wf)
    self.wid = self.pi1.wave_create()
    # pi1.wave_send_once(wid)
  
  def Move(self, pos):
    p = abs(pos)
    x,y = divmod(p,256)
    d = (pos > 0)
    self.pi1.write(self.direction, d)  
  #  print(p,d,x,y)
    self.pi1.wave_chain([
     255, 0,                       # loop start
        self.wid,     # transmit waves 0+0+0
     255, 1, y, x,                 # loop end (repeat 5 times)
     ])
    while self.pi1.wave_tx_busy():
       time.sleep(0.01);    # add loop until done


  def Finish(self):
    self.pi1.wave_tx_stop()
    self.pi1.stop()

  def Reset(self):
    self.pi1.write(self.RESET, 1)  
    self.pi1.write(self.RESET, 0) 
    time.sleep(0.01)    
    self.pi1.write(self.RESET, 1)     


