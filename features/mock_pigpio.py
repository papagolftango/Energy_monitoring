import time
    
    class MockPigpio:
        OUTPUT = 0
        INPUT = 1
    
        def __init__(self):
            self.pins = {}
            self.waveforms = []
            self.wave_tx_busy_flag = False
    
        def set_mode(self, pin, mode):
            self.pins[pin] = {"mode": mode, "state": 0}
    
        def write(self, pin, state):
            if pin in self.pins:
                self.pins[pin]["state"] = state
    
        def wave_add_generic(self, pulses):
            self.waveforms.append(pulses)
            return len(self.waveforms) - 1
    
        def wave_create(self):
            return len(self.waveforms) - 1
    
        def wave_chain(self, chain):
            self.wave_tx_busy_flag = True
            time.sleep(0.1)  # Simulate some delay
            self.wave_tx_busy_flag = False
    
        def wave_tx_busy(self):
            return False
    
        def wave_tx_stop(self):
            self.wave_tx_busy_flag = False
    
        def pulse(self, on_pins, off_pins, delay):
            return {"on_pins": on_pins, "off_pins": off_pins, "delay": delay}