#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import smtplib
import os

server = smtplib.SMTP('smtp.gmail.com',587)
server.ehlo()
server.starttls()
server.ehlo()
server.login("<user>","<pass>")
msg = 'The tank is half full. Please refill.'

GPIO.setmode(GPIO.BOARD)

#Pin numbering
BUTTON = 7
TRIG = 38
ECHO = 40

GPIO.setup(BUTTON,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(TRIG,GPIO.OUT)
GPIO.output(TRIG,0)

GPIO.setup(ECHO,GPIO.IN)

while GPIO.input(BUTTON) == 0:
    pass

time.sleep(2)

GPIO.output(TRIG,1)
time.sleep(0.00001)
GPIO.output(TRIG,0)

while GPIO.input(ECHO) == 0:
    pass
start = time.time()

while GPIO.input(ECHO) == 1:
    pass
stop = time.time()

distance1 = (stop-start) * 170
string1 = str(distance1)
print('Tank height: ' + string1[0:4] + ' meters')

while GPIO.input(BUTTON) == 0:
    pass

distance2 = 0

while distance2 < (distance1 / 2):
    GPIO.setup(TRIG,GPIO.OUT)
    GPIO.output(TRIG,0)

    GPIO.setup(ECHO,GPIO.IN)

    time.sleep(1)

    GPIO.output(TRIG,1)
    time.sleep(0.00001)
    GPIO.output(TRIG,0)
    while GPIO.input(ECHO) == 0:
        pass
    start = time.time()

    while GPIO.input(ECHO) == 1:
        pass
    stop = time.time()

    distance2 = (stop-start) * 170
    string2 = str(distance2)
    print('Current water height: '+ string2[0:4] +' meters')
    
print('Magic Time!')
server.sendmail("sender","receiver",msg)
server.quit()

GPIO.cleanup()
os.system('sudo shutdown -h now')
