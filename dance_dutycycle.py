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
# define basic functions
def reset(): 
    legR.angle = 94
    legL.angle = 90
    footR.angle = 90
    footL.angle = 91

def rotate(limb, min, max, step):
    for x in range(min, max, step):
        limb.angle = x

# define single dance move functions 
def leftFootOut():
    reset()
    rotate(legL, 90, 180, 5)
    rotate(legL, 180, 90, -5)
    reset()

def rightFootOut():
    reset()
    rotate(legR, 90, 10, -5)
    rotate(legR, 10, 90, 5)
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
    rotate(footR, 90, 130, 4)
    rotate(footR, 130, 90, -4)
    reset()

def leftKick():
    legL.angle = 160
    rotate(footL, 90, 60, -3)
    rotate(footL, 60, 90, 3)
    reset()

def shuffle():
    for angle in range(90, 60, -5):  # 0 - 180 degrees, 5 degrees at a time.
        legL.angle = angle
        legR.angle = 90 + (angle - 60)
    for angle in range(60, 90, 5): # 180 - 0 degrees, 5 degrees at a time.
        legL.angle = angle
        legR.angle = 90 + (angle - 60)
    reset()    

def wiggle():
    rotate(footL, 90, 130, 5)
    rotate(footR, 90, 60, -5)
    rotate(footL, 130, 90, -5)
    rotate(footR, 60, 90, 5)


def tapLeftFoot():
    reset()
    rotate(footL, 90, 60, -3)
    rotate(footL, 60, 90, 3)
    reset()
    
def tapRightFoot():
    reset()
    rotate(footR, 90, 120, 3)
    rotate(footR, 120, 90, -3)
    reset()
 
def tapBothFeet():
    reset()
    for angle in range(90, 130, 8):  # 0 - 180 degrees, 5 degrees at a time.
        footL.angle = 90 - (angle - 90)
        footR.angle = angle
    for angle in range(130, 90, -8): # 180 - 0 degrees, 5 degrees at a time.
        footL.angle = 90 - (angle - 90)
        footR.angle = angle
    reset()



# define 6 main dance moves

#1: slide
def dance1():
    reset()
    for i in range(8):
        wiggle()
    reset()

#2: line dance
def dance2():
    for i  in range(2):
        leftFootOut()
        rightFootOut()
        twist()

#3: karate kick
def dance3():
    leftFootOut()
    tapLeftFoot()
    leftKick()

    rightFootOut()
    tapRightFoot()
    rightKick()

#4: tap feet to the beat
def dance4():
    for i in range(4):       
        tapLeftFoot()
    for i in range(4):       
        tapRightFoot()
    for i in range(4):       
        tapBothFeet()

#5: walk
def dance5():
    for i in range(5):
        leftKick()
        rightKick()

#6: 
def dance6():
    for i in range(8):
        shuffle()
