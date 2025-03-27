import time
from machine import Pin, PWM

#Xiao RP2040
pinNotEnable = Pin(1, Pin.OUT) # D0
pinStep = PWM(Pin(2, Pin.OUT))  # D8
pinDir = Pin(3, Pin.OUT)  # D10

#step_freq = 2000 # 2000Hz
#step_duty = int(65536 * 0.5) # 50%

class Stepper:
    def __init__(self):
        self.unlock()

    def enable(self):
        pinNotEnable.value(False)

    def disable(self):
        pinNotEnable.value(True)
        
    def lock(self):
        self.enable()
        
    def unlock(self):
        self.disable()
    
    def step(self, step_freq = 2000, dir=0, duty = 0.5):
        pinDir.value(dir)
        pinStep.duty_u16(int(65536 * duty))
        pinStep.freq(step_freq)

    def sweep(self, to_freq=1000, dir = 0):
        from_freq=400
        self.step(from_freq, dir)
        for i in range(20):
            freq = from_freq + int((to_freq - from_freq)/20) * (i+1)
            self.step(freq, dir)
            time.sleep(0.1)
        


