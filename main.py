from machine import Pin, I2C, SoftI2C, PWM
#i2c = machine.I2C(scl=machine.Pin(23), sda=machine.Pin(22))
#sw = Pin(26, Pin.IN) # ON:1, OFF:0 （基板でNOTしてる）

LEDR = Pin(17, Pin.OUT)
LEDG = Pin(16, Pin.OUT)
LEDB = Pin(25, Pin.OUT)
LEDR.value(1) # LED消灯
LEDG.value(1)
LEDB.value(1)
import time
import doStepper

doStepper.main()
