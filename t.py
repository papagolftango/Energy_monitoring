
import time 
import pigpio


class motor:
   constant onTime = 400
   constant offTime = 600
   ClkA=4
   DiaA=5
   NONE=0
   wid=0
   pi1=0
   clk =0
   diection=0
   wf=[]


  def Init(Clk, Direction) :  
    self.clk = Clk
    self.direction = Direction
    self.pi1 = pigpio()
    self.pi1.set_mode(self.clk, pigpio.OUTPUT)
    self.pi1.set_mode(self.direction, pigpio.OUTPUT)
    self.pi1.write(self.direction, 1)  
 
    self.wf.append(pigpio.pulse(gpio_on=(1<<self.Clk), gpio_off=NONE, delay=self.onTime400))     # get required timings
    self.wf.append(pigpio.pulse(gpio_on=NONE, gpio_off=(1<<self.Clk), delay=self.offTime))

    self.pi1.wave_clear()
    self.pi1.wave_add_generic(wf)
    self.wid = pi1.wave_create()
    # pi1.wave_send_once(wid)
  
  def Move(pos, direction):
    self.pi1.wave_chain([
     255, 0,                       # loop start
        self.wid,     # transmit waves 0+0+0
     255, 1, 25, 0,                 # loop end (repeat 5 times)
     ])
    time.sleep(0.01)    # add loop until done


  def Finish():
    self.pi1.wave_tx_stop()
    self.pi1.stop()


pi1 = pigpio.pi()
Init(4,5)
Move(200, 1)
Move(200,1)
Finish()
