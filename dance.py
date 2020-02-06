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
 

def shuffle():
    