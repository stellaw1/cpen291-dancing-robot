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
 
# define basic functions 
def rightShuffle():
    print("shuffling")
    for i in range(3):
        for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
            my_servo.angle = angle
            time.sleep(0.05)

def leftShuffle():
    print("shuffling")
    for i in range(3):
        for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
            my_servo.angle = angle
            time.sleep(0.05)

def rightKick():
    print("right kick")
    for i in range(3):
        for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
            my_servo.angle = angle
            time.sleep(0.05)

def leftKick():
    print("right kick")
    for i in range(3):
        for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
            my_servo.angle = angle
            time.sleep(0.05)

def rightStep():
    print("right kick")
    for i in range(3):
        for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
            my_servo.angle = angle
            time.sleep(0.05)

def leftStep():
    print("right kick")
    for i in range(3):
        for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
            my_servo.angle = angle
            time.sleep(0.05)

def tiltLeft():
    print("right kick")
    for i in range(3):
        for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
            my_servo.angle = angle
            time.sleep(0.05)

def tiltright():
    print("right kick")
    for i in range(3):
        for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
            my_servo.angle = angle
            time.sleep(0.05)

# define dance moves as sequences of basic moves
def walk():
    for i in range(6):
        tiltLeft()
        time.sleep(0.05)
        tiltRight()
        time.sleep(0.05)

def shuffle():
    for i in range(6):
        shuffleLeft()
        time.sleep(0.05)
        shuffleRight()
        time.sleep(0.05)