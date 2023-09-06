class mqtt:

     def __init__(self):
       pass    
         
           
     def Client(self):
          return self
          
     def subscribe(self,topic) :
          print(topic)

     def connect(self, p1, p2) :
         print(p1,p2)

     def loop_start(self) :
          print("loop start")

     def publish(self,topic, payload) :
         print(topic, payload)

     def disconnect(self) :
         print("disconnect")