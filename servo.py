#Standard Sevo Code (-90 to 90)
import time
import board
import pulseio
from adafruit_motor import servo
 
# create a PWMOut object on Pin A2.
pwm = pulseio.PWMOut(board.A5, duty_cycle=2 ** 15, frequency=50)
 
# Create a servo object, my_servo.
my_servo = servo.Servo(pwm)
 
while True:
    for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
        my_servo.angle = angle
        time.sleep(0.05)
    for angle in range(180, 0, -5): # 180 - 0 degrees, 5 degrees at a time.
        my_servo.angle = angle
        time.sleep(0.05)

#############################################

#Continuous Servo Code
import time
import board
import pulseio
from adafruit_motor import servo
 
# create a PWMOut object on Pin A2.
pwm = pulseio.PWMOut(board.A5, frequency=50)
 
# Create a servo object, my_servo.
my_servo = servo.ContinuousServo(pwm)
 
while True:
    print("forward")
    my_servo.throttle = 1.0
    time.sleep(2.0)
    print("stop")
    my_servo.throttle = 0.0
    time.sleep(2.0)
    print("reverse")
    my_servo.throttle = -1.0
    time.sleep(2.0)
    print("stop")
    my_servo.throttle = 0.0
    time.sleep(4.0)
#Working code use A1
#Continuous Servo Code
import time
import board
import pulseio
from adafruit_motor import servo
 
# create a PWMOut object on Pin A2.
pwm = pulseio.PWMOut(board.A1, frequency=50)
 
# Create a servo object, my_servo.
my_servo = servo.ContinuousServo(pwm)
 
while True:
    print("forward")
    my_servo.throttle = 1.0
    time.sleep(2.0)
    print("stop")
    my_servo.throttle = 0.1
    time.sleep(2.0)
    print("reverse")
    my_servo.throttle = -1.0
    time.sleep(2.0)
    print("stop")
    my_servo.throttle = 0.1
    time.sleep(4.0)

########################################################################################
    
import time
import board
import pulseio
from adafruit_motor import servo
 
pwm1 = pulseio.PWMOut(board.A1, frequency=50) #leg1
my_servo1 = servo.ContinuousServo(pwm1)

pwm2 = pulseio.PWMOut(board.A3, frequency=50) #leg2
my_servo2 = servo.ContinuousServo(pwm2)

pwm3 = pulseio.PWMOut(board.A4, frequency=50)
my_servo3 = servo.ContinuousServo(pwm3)

pwm4 = pulseio.PWMOut(board.A5, frequency=50)
my_servo4 = servo.ContinuousServo(pwm4)
 
while True:
    my_servo1.throttle = 1.0
    my_servo2.throttle = 1.0
    time.sleep(1.0)
    my_servo3.throttle = 0.1
    my_servo1.throttle = 0.1
    my_servo2.throttle = 0.1
    my_servo3.throttle = 0.3
    time.sleep(1.0)
    my_servo4.throttle = 0.1
    my_servo1.throttle = 0.1
    my_servo2.throttle = 0.0
    my_servo4.throttle = 0.3
    my_servo1.throttle = -1.0
    my_servo2.throttle = -1.0
    time.sleep(1.0)
    my_servo1.throttle = 0.1
    time.sleep(3.0)
