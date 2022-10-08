
class pigpio :

  OUTPUT = 0

  def __init__(self) :  
    print("PIGPIO")

  def set_mode(self, x,y) :
    print("pigpio ",x,y)

  def pi(self) :
    print("PI")

  def write(self,x,y) :
    print("pigpio write", x,y)
 
  def pulse( gpio_on, gpio_off, delay) :  
    print("pigpio pulse", gpio_on, gpio_off, delay)  

  def wave_clear(self) :
    print("pigpio wave clear")
       
  def wave_add_generic(self,x) :
    print("pigpio wave add generic", x)  

  def wave_create(self) :
    print("pigpio wave create")
    return(1)

  def write(self,x,y) :
    print("pigpio write", x,y)

  def wave_chain(self,x) :
    print("pigpio wave chain", x)

  def wave_tx_busy(self) :
    print("pigpio tx busy")
    return(False)

def wave_tx_stop(self) :
    print("PIGPIO TX STOP")

def stop(self
) :
    print("PIGPIO STOP") 