import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import time

leds = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(leds, GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(dac, GPIO.OUT)
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
        GPIO.output(leds, bin)
        time.sleep(0.001)
        if GPIO.input(comp) == 0:
            bin[i] = 0

    dec = bin2dec(bin)
    return dec


try:
    values = []
    time_start = time.time() # начало эксперимента
    
    voltage = (3.3 * adc()) / 256
    GPIO.output(troyka, 1) # подаём 3,3 вольта на вход тройки модуля
    while voltage < (0.97 * 3.3):
        values.append(voltage)
        print(f"{voltage} V")
        time.sleep(0.05)
        voltage = (3.3 * adc()) / 256

    GPIO.output(troyka, 0) # подаём 0 вольт на вход тройки модуля
    while voltage > (0.02 * 3.3):
        values.append(voltage)
        print(f"{voltage} V")
        time.sleep(0.05)
        voltage = (3.3 * adc()) / 256

    time_end = time.time() # конец эксперимента
    duration = time_end - time_start
    str_values = [str(item) for item in values] # считаем параметры эксперимента
    frq = len(values) / duration
    period = duration / len(values)
    step = (max(values) - min(values)) / 256
    frq_st = [frq, step]

    with open("data.txt", "w") as file: # записываем в файл
        file.write("\n".join(str_values))

    with open("settings.txt", "w") as file:
        file.write("\n".join([str(item) for item in frq_st]))

    print(f"Duration: {duration}\nPeriod: {period}\nFrequency: {frq}\nStep: {step}") # выводим в терминал

    plt.plot(values) # строим график
    plt.show()
finally:
    GPIO.cleanup()