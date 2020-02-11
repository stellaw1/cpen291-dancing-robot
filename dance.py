import time
import board
import pulseio
from adafruit_motor import servo
 
pwm1 = pulseio.PWMOut(board.D10, frequency=50)
right_leg = servo.ContinuousServo(pwm1)

pwm2 = pulseio.PWMOut(board.D11, frequency=50)
left_leg = servo.ContinuousServo(pwm2)

pwm3 = pulseio.PWMOut(board.D12, frequency=50)
right_foot = servo.ContinuousServo(pwm3)

pwm4 = pulseio.PWMOut(board.D13, frequency=50)
left_foot = servo.ContinuousServo(pwm4)
 
# define basic functions 
def rightShuffle():
    print("shuffling")
    for i in range(3):
        for angle in range(0, 90, 5):  # 0 - 180 degrees, 5 degrees at a time.
            right_leg.angle = angle
            time.sleep(0.05)

def leftShuffle():
    print("shuffling")
    for i in range(3):
        for angle in range(90, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
            left_leg.angle = angle
            time.sleep(0.05)

def rightKick():
    print("right kick")
    for i in range(3):
        for angle in range(0, 90, 5):  # 0 - 180 degrees, 5 degrees at a time.
            right_foot.angle = angle
            time.sleep(0.05)
        time.sleep(1)
        for angle in range(0, 90, 5):
            right_foot.angle = 90 - angle
            time.sleep(0.05)

def leftKick():
    print("right kick")
    for i in range(3):
        for angle in range(0, 90, 5):  # 0 - 180 degrees, 5 degrees at a time.
            left_foot.angle = angle
            time.sleep(0.05)
        time.sleep(1)
        for angle in range(0, 90, 5):
            left_foot.angle = 90 - angle
            time.sleep(0.05)

def tiptoes():
    for i in range(3):
        for angle in range(0, 20, 5):
            left_foot.angle = angle
            right_foot.angle = angle + 90
            time.sleep(0.05)
        time.sleep(1)
        for angle in range(0, 20, 5):
            left_foot.angle = 20 - angle
            right_foot.angle = 110 - angle
            time.sleep(0.05)

def rightStep():
    print("right kick")
    for i in range(3):
        for angle in range(90, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
            right_foot.angle = angle
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