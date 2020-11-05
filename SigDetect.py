# Signal Detect RED/GREEN and Arrow Detection.
# Using Template maching.
# Template Matching Example - Normalized Cross Correlation (NCC)
#
import sys
import time, sensor, image
import utime
from pyb import Pin, Timer, LED
from image import SEARCH_EX, SEARCH_DS

# template match
#tL = image.Image("/LA_64_64.pgm")
#tR = image.Image("/RA_64_64.pgm")
tL = image.Image("/LA_32_32_1.pgm")
tR = image.Image("/RA_32_32_1.pgm")
tU = image.Image("/UA_32_32.pgm")
#template = image.Image("/H.pgm")

# Color
# PWM OUT
tim = Timer(4, freq=1000) # Frequency in Hz
tim.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent=5)
thresholds = [(30, 100, 15, 127, 15, 127), # generic_red_thresholds
              (30, 100, -64, -8, -32, 32)] # generic_green_thresholds
loopTime = 800
clock = time.clock()

#timled = Timer(2)
#timled.init(freq=2)         # trigger at 2Hz
#timled.callback(lambda t:LED(1).toggle())

def findArrow():
    print("Arrow")
    roi = [72, 10, 90, 90]
    start = utime.ticks_ms()
    while(True):
        #clock.tick()
        fRect = False
        parcent = 2
        tim.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent=parcent)
        if utime.ticks_diff(utime.ticks_ms(), start) > loopTime *1.2:
            return
        fRect = True
        img = sensor.snapshot()
        l = img.find_template(tL, 0.42, roi, step=6, search=SEARCH_EX)
        #l = img.find_template(tL, 0.3, step=4, search=SEARCH_EX)
        if l and fRect:
            parcent = 45
            #img.draw_rectangle(l)
            tim.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent=parcent)
            print ("L")
        r = img.find_template(tR, 0.42, roi, step=6, search=SEARCH_EX)
        #r = img.find_template(tR, 0.3, step=4, search=SEARCH_EX)
        if r and fRect:
            parcent = 65
            #img.draw_rectangle(r)
            tim.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent=parcent)
            print ("R")

def checkSignal():
    print("Signal")
    start = utime.ticks_ms()
    while(True):
        if utime.ticks_diff(utime.ticks_ms(), start) > loopTime:
            return

        #clock.tick()
        parcent = 2
        LED(1).on()
        img = sensor.snapshot()
        tim.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent=parcent)
        #for blob in img.find_blobs([thresholds], pixels_threshold=450, area_threshold=400, merge=True):
        for blob in img.find_blobs(thresholds, pixels_threshold=450, area_threshold=400, merge=True):
            #print(blob.code())
            ratio = blob.w() / blob.h()
            if (ratio >= 0.5) and (ratio <= 1.5): # filter out non-squarish blobs
                if blob.code() == 1: # red
                    LED(1).on()
                    parcent = 20
                    print("RED")
                elif blob.code() == 2: # green
                    parcent = 90
                    LED(2).on()
                    print("GREEN")
                else:
                    print("OTHER")
                img.draw_rectangle(blob.rect())
                img.draw_cross(blob.cx(), blob.cy())

                for i in range(1, 10):
                    tim.channel(1, Timer.PWM, pin=Pin("P7"), pulse_width_percent=parcent)
                    time.sleep(5)
def run(argv):
    mode = argv
    if (mode == 0):
        #check Arrow
        sensor.reset()
        '''sensor.set_auto_gain(False)
        sensor.set_contrast(1)
        sensor.set_gainceiling(16)
        #sensor.set_windowing((200, 200)) # 240x240 center pixels of VGA
        sensor.set_framesize(sensor.QQVGA)
        sensor.set_pixformat(sensor.GRAYSCALE)
        sensor.set_auto_whitebal(False)
        '''
        sensor.set_pixformat(sensor.GRAYSCALE)
        sensor.set_framesize(sensor.QQVGA)
        sensor.set_vflip(True)
        sensor.set_hmirror(True)
        sensor.skip_frames(time = 2000)

        findArrow()
    else:
        #check signal mode
        sensor.reset()
        sensor.set_auto_gain(False)
        sensor.set_auto_whitebal(True)
        sensor.set_contrast(-3)
        sensor.set_brightness(-3)
        sensor.set_gainceiling(8)
        sensor.set_pixformat(sensor.RGB565)
        sensor.set_vflip(True)
        sensor.set_framesize(sensor.VGA)
        sensor.set_windowing((240, 240)) # 240x240 center pixels of VGA
        #sensor.set_windowing((200, 200)) # 200x200 center pixels of VGA
        sensor.skip_frames(time = 800)
        checkSignal()

if __name__ == "__main__":
    while(True):
#        run(0)
        run(1)

