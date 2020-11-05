# Template Matching Example - Normalized Cross Correlation (NCC)
#
# This example shows off how to use the NCC feature of your OpenMV Cam to match
# image patches to parts of an image... expect for extremely controlled enviorments
# NCC is not all to useful.
#
# WARNING: NCC supports needs to be reworked! As of right now this feature needs
# a lot of work to be made into somethin useful. This script will reamin to show
# that the functionality exists, but, in its current state is inadequate.

import time, sensor, image
from image import SEARCH_EX, SEARCH_DS
from pyb import UART
sensor.reset()
sensor.set_contrast(1)
sensor.set_gainceiling(16)
sensor.set_framesize(sensor.QQVGA)
sensor.set_pixformat(sensor.GRAYSCALE)
#template = image.Image("/template.pgm")
#template1=image.Image("/lefttemplate.pgm")
template = image.Image("/LA_32_32.pgm")
clock = time.clock()
uart = UART(3, 9600)
while (True):
    clock.tick()
    img = sensor.snapshot()
    r = img.find_template(template, 0.87, step=2, search=SEARCH_DS)
    #l = img.find_template(template1, 0.87, step=4, search=SEARCH_DS)
    if r:
        print ("r")
        uart.write("r")
    #elif l:
    #    uart.write("l")
    #else:
    #    uart.write("n")

    print(clock.fps())
