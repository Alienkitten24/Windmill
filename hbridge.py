import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.out)
GPIO.setup(27, GPIO.out)


def cw():
    GPIO.output(17, 1)
    GPIO.output(27, 0)

def ccw():
    GPIO.output(17, 0)
    GPIO.output(27, 1)

def off():
    GPIO.output(17, 0)
    GPIO.output(27, 0)

cw()
sleep(2)
off()
sleep(1)
ccw()
sleep(2)

GPIO.cleanup()