import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
led = [24, 25, 8, 7, 12, 16, 20, 21]
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)

def dec2bin(value):
    return [int(element) for element in bin(value)[2:].zfill(8)]

def bin2dec(value):
    dec = 0
    deg = 0
    for i in range(7, -1, -1):       
        dec += (2*value[i])**deg
        deg += 1

    return dec

def adc():
    bin = dec2bin(0)
    for i in range(7):
        bin[i] = 1
        GPIO.output(dac, bin)
        time.sleep(0.001)
        if GPIO.input(comp) == 0:
            bin[i] = 0

    dec = bin2dec(bin)
    return dec

def leds(voltage):
    GPIO.output(led, 0)
    i = int(((voltage + 0.1) / 3.3) * 8)
    for j in range(i):
        GPIO.output(led[j], 1)

try:
    while True:
        dec = adc()
        voltage = (3.3 * dec) / 256
        print(f"{dec2bin(dec)} -> {dec} -> {voltage} V")
        leds(voltage)
finally:
    GPIO.cleanup()