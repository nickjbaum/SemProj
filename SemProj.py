#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import smtplib
import os

#setting up smtp
server = smtplib.SMTP('smtp.gmail.com',587)
server.ehlo()
server.starttls()
server.ehlo()
server.login("<user>","<pass>")
msg = 'The tank is half full. Please refill.'

#configure board pin numbering system for Pi
GPIO.setmode(GPIO.BOARD)

#Pin numbering
BUTTON = 7
TRIG = 38
ECHO = 40

#setting push button as a pull down resistor
GPIO.setup(BUTTON,GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

#setting sensor trigger pin as an output
GPIO.setup(TRIG,GPIO.OUT)
GPIO.output(TRIG,0)

#setting sensor echo pin as an input
GPIO.setup(ECHO,GPIO.IN)

#the device starts first measurement when button is pressed
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

#saving initial measurement as a variable
distance1 = (stop-start) * 170
string1 = str(distance1)
print('Tank height: ' + string1[0:4] + ' meters')

#continuous measurement begins when button is pressed a second time
while GPIO.input(BUTTON) == 0:
    pass

#storing subsequent measurements as a variable
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
    
#when tank is half full, send an email with the message
print('Magic Time!')
server.sendmail("sender","receiver",msg)
server.quit()

#reset and shut down Pi after email is sent
GPIO.cleanup()
os.system('sudo shutdown -h now')
