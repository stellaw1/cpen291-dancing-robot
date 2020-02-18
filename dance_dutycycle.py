import time
import board
import pulseio
import servo

###########################################
# pin assignments and initial setup
pwm1 = pulseio.PWMOut(board.D10, duty_cycle=2 ** 15, frequency=50)
legR = servo.Servo(pwm1)

pwm2 = pulseio.PWMOut(board.D11, duty_cycle=2 ** 15, frequency=50) #leg2
legL = servo.Servo(pwm2)

pwm3 = pulseio.PWMOut(board.D12, duty_cycle=2 ** 15, frequency=50)
footL = servo.Servo(pwm3)

pwm4 = pulseio.PWMOut(board.D13, duty_cycle=2 ** 15, frequency=50)
footR = servo.Servo(pwm4)


###################################
# define basic dance move functions 
def reset(): 
    legR.angle = 94
    legL.angle = 90
    footR.angle = 90
    footL.angle = 91

def leftFootOut():
    reset()
    for angle in range(180, 0, -5): # 180 - 0 degrees, 5 degrees at a time.
        legL.angle = angle
    for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
        legL.angle = angle
    reset()

def rightFootOut():
    reset()
    for angle in range(180, 0, -5): # 180 - 0 degrees, 5 degrees at a time.
        legR.angle = angle
    for angle in range(0, 180, 5):  # 0 - 180 degrees, 5 degrees at a time.
        legR.angle = angle
    reset()

def twist(): 
    reset()
    for angle in range(10, 180, 10):  # 0 - 180 degrees, 5 degrees at a time.
        legL.angle = angle
        legR.angle = angle
    for angle in range(180, 10, -10): # 180 - 0 degrees, 5 degrees at a time.
        legL.angle = angle
        legR.angle = angle
    reset()

def jump():
    reset()
    for angle in range(90, 130, 5):  # 0 - 180 degrees, 5 degrees at a time.
        footL.angle = angle
        footR.angle = 90 - (angle - 90)
    for angle in range(130, 90, -5): # 180 - 0 degrees, 5 degrees at a time.
        footL.angle = angle
        footR.angle = 90 - (angle - 90)
    reset()

def rightKick():
    legR.angle = 20
    for angle in range(90, 140, 4):  # 0 - 180 degrees, 5 degrees at a time.
        footR.angle = angle
    for angle in range(140, 90, -4): # 180 - 0 degrees, 5 degrees at a time.
        footR.angle = angle
    reset()

def leftKick():
    legL.angle = 160
    for angle in range(90, 60, -3):  # 0 - 180 degrees, 5 degrees at a time.
        footL.angle = angle
    for angle in range(60, 90, 3): # 180 - 0 degrees, 5 degrees at a time.
        footL.angle = angle
    reset()

def shuffle():
    reset()
    for i in range(8):
        for angle in range(90, 60, -5):  # 0 - 180 degrees, 5 degrees at a time.
            legL.angle = angle
            legR.angle = 90 + (angle - 60)
        for angle in range(60, 90, 5): # 180 - 0 degrees, 5 degrees at a time.
            legL.angle = angle
            legR.angle = 90 + (angle - 60)
    reset()    

def slide():
    reset()
    for i in range(8):
        for angle in range(90, 130, 5):  # 0 - 180 degrees, 5 degrees at a time.
            footL.angle = angle
        for angle in range(90, 60, -5):
            footR.angle = angle
        for angle in range(130, 90, -5): # 180 - 0 degrees, 5 degrees at a time.
            footL.angle = angle
        for angle in range(60, 90, 5):
            footR.angle = angle
    reset() 

