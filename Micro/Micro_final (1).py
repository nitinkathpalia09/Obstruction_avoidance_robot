import RPi.GPIO as GPIO                    #Import GPIO library
import time
import pygame
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)                    # programming the GPIO by BCM pin numbers
TRIG = 17
ECHO = 27
led = 22
m11=16
m12=12
m21=21
m22=20
GPIO.setup(TRIG,GPIO.OUT)                  # initialize GPIO Pin as outputs
GPIO.setup(ECHO,GPIO.IN)                   # initialize GPIO Pin as input
GPIO.setup(led,GPIO.OUT)                  
GPIO.setup(m11,GPIO.OUT)
GPIO.setup(m12,GPIO.OUT)
GPIO.setup(m21,GPIO.OUT)
GPIO.setup(m22,GPIO.OUT)
GPIO.output(led, 1)
time.sleep(5)
pygame.init()
display_width=600
display_height=500
black =(0,0,0)
white=(255,255,255)
carImg=pygame.image.load('racecar.png')
gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('map')
x=(display_width*0.45)
y=(display_height*0.45)
x_change=0
y_change=0
exit=False
def car(x,y):
    gameDisplay.blit(carImg,(x,y))
def stop():
    print "stop"
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    x_change=0
    y_change=0
def forward():
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print "Forward"
    y_change=-5
    x_change=0
    return y_change
def back():
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 1)
    print "back"
    y_change=5
    x_change=5
def left():
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    print "left"
    x_change=-5
    y_change=0
def right():
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    print "right"
    x_change=5
    y_change=0
stop()
count=0
while True:
 i=0
 avgDistance=0
 y_change=forward()
 x+=x_change
 y+=y_change
 gameDisplay.fill(white)
 car(x,y)
 pygame.display.update()
 for i in range(5):
  GPIO.output(TRIG, False)                 #Set TRIG as LOW
  time.sleep(0.1)                                   #Delay
  GPIO.output(TRIG, True)                  #Set TRIG as HIGH
  time.sleep(0.00001)                           #Delay of 0.00001 seconds
  GPIO.output(TRIG, False)                 #Set TRIG as LOW
  while GPIO.input(ECHO)==0:              #Check whether the ECHO is LOW
       GPIO.output(led, False)             
  pulse_start = time.time()
  while GPIO.input(ECHO)==1:              #Check whether the ECHO is HIGH
       GPIO.output(led, False) 
  pulse_end = time.time()
  pulse_duration = pulse_end - pulse_start #time to get back the pulse to sensor
  distance = pulse_duration * 17150        #Multiply pulse duration by 17150 (34300/2) to get distance
  distance = round(distance,2)                 #Round to two decimal points
  avgDistance=avgDistance+distance
 avgDistance=avgDistance/5
 print avgDistance
 flag=0
 if avgDistance < 15:      #Check whether the distance is within 15 cm range
    count=count+1
    stop()
    time.sleep(1)
    back()
    time.sleep(1.5)
    if (count%3 ==1) & (flag==0):
     right()
     flag=1
    else:
     left()
     flag=0
    time.sleep(1.5)
    stop()
    time.sleep(1)
 else:
    forward()
    flag=0
