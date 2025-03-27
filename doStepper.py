from machine import Pin, I2C, SoftI2C, PWM, reset
import time
import stepper
import freqconfig
freq = freqconfig.Freqconf()
OldFreq = freq.get_freq()
st = stepper.Stepper()
st.enable()

Alt = True

def switchon(e):
    global Alt
    global OldFreq
    if Freq == OldFreq and Freq != -10 and Alt:
        st.disable()
        Alt = False
        return
    elif Freq == 0:
        st.disable()
    elif Freq <= 500:
        st.enable()
        st.step(Freq)
    else:
        st.enable()
        st.sweep(Freq)
    Alt = True
    OldFreq = Freq


import seg74
i2c = SoftI2C(scl=7, sda=6, freq=500000) # RP2040
seg = seg74.Seg74(i2c, 112)
seg.seg74ada("   0")


sw = Pin(26, Pin.IN) # RP2040  ON:1, OFF:0 （基板でNOTしてる）


def main():
    print(OldFreq)
    seg.seg74ada(f"{OldFreq:4d}")
    st.sweep(OldFreq)

    sw.irq(trigger = Pin.IRQ_RISING, handler = switchon)

    from rotary_irq_esp import RotaryIRQ

    r = RotaryIRQ(pin_num_clk=29,  # RP2040
              pin_num_dt=27, 
              min_val=0, 
              max_val=200, 
              reverse=False, 
              range_mode=RotaryIRQ.RANGE_WRAP)
    
    r.set(int(OldFreq / 10))
    val_old = r.value()

    nagaoshiCnt = 0
    while True:
        global Freq
        val_new = r.value()
    
        if val_old != val_new:
            val_old = val_new
            #print('result =', val_new)
            seg.seg74ada(f"{val_new * 10:4d}")
        if sw.value() == 1:
            nagaoshiCnt += 1
        else:
            nagaoshiCnt = 0
        if nagaoshiCnt > 20:
                seg.blink()
                seg.seg74ada(f"{OldFreq:4d}")
                time.sleep(2)
                freq.set_freq(OldFreq)
                st.disable()
                seg.seg74ada(" . . . .")
                time.sleep(2)
                reset()
        time.sleep_ms(50)
        Freq = val_new * 10


