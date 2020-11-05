# Single Color RGB565 Blob Tracking Example
import sensor, image, time
import time

from pyb import UART
from pyb import LED
uart = UART(3,9600, timeout_char = 3000)
led1 = LED(1)

threshold_index = 0 # 0 for red, 1 for green, 2 for blue
thresholds = [(30, 100, 15, 127, 15, 127), # generic_red_thresholds
              (30, 100, -64, -8, -32, 32), # generic_green_thresholds
              (0, 30, 0, 64, -128, 0)] # generic_blue_thresholds

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs([thresholds[threshold_index]], pixels_threshold=300, area_threshold=300, merge=True):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        uart.write("%d\n"%blob.cx())
        uart.write("\n")
        print("XXX")
#        led1.on()
#        time.sleep(300)
#        led1.off()
        #print("%d\n"%blob.cx(), end='')
