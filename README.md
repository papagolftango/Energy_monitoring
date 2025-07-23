
# Energy_monitoring
Home Energy Monitor

Scrape weather from the web  - feed the AI model to provide sunlight prediction
Modify usage of key consumers based on the model

Uses 4 x27.168 stepper motors via a stepper driver connected to a pi zero w.

Each stepper is independently controlled by 2 gpio lines for step and direction. Note some PCB errors to be corrected


![image](https://github.com/papagolftango/Energy_monitoring/assets/42871083/b512709b-9e31-4cd2-9a4d-da13cd991817)


This board is a 'hat' for a RPI zero W. This uses some simple python code to drive the motors. 
It in turn uses the PIGPIO library to provide a more real-time step experience. 
This library is not rerentrant and I wanted to be able to move the 4 motors simultaneously, if required. 

The Stepper driver requies a reset  - provided by a GPIO at initalisation. Then, for each motor its a case of 
setting the direction pin and then providing the appropriate number of steps. The motors require 12 step per degree and travel over 300 degs.

Th main code is based on Gauges.py. This manages all 4 gauges and is currently configured by a hardcoded table which sets the direction and step pins.

The constructor pulses th Reset, setsup the PIGPIO waveforms and then performs a gauge reset by moving full scale in one direction followed by full scale in the opposite direction.
The waves are setup to move all motors simultaeously.

The API is then largely built arround the move command: move(m0,m1,m2,m3) which performs a move relative to the last position.

The current use case is to interface to the existing emonpi energy monitoring system. This sstem have been configured to publish various MQTTP topics that can be configured to be displayed on 
the gauges.

The file emongauge.py is configured by the .env file. This contains the username/password and MQTT broker address. The intent is to use the broker built into the emonpi.
The code creates and instance of the gauges class (which will initialise it and set gauges to physical zero). Each gauges is associated and scaled in the .env file. That is 
the file contains the topic for eg m2. The code will subscribe to this topic (once connected to the broker). The scale is provided for the gauge in gauge units and a scale factor is
calculated for convert into physcal step units. The range can incorporate + and - values. eg to represent mains volts of nominal 240V, the scale is set 0 to 300V. 
