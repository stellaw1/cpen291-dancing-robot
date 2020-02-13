import time
import board
import pulseio
import servo

import adafruit_hcsr04

piezo = pulseio.PWMOut(board.A1 , duty_cycle=0, frequency=440, variable_frequency=True)

#servo setup
pwm1 = pulseio.PWMOut(board.D10, frequency=50) #leg1
legL = servo.Servo(pwm1)

pwm2 = pulseio.PWMOut(board.D11, frequency=50) #leg2
legR = servo.Servo(pwm2)

pwm3 = pulseio.PWMOut(board.D12, frequency=50)
footL = servo.Servo(pwm3)

pwm4 = pulseio.PWMOut(board.D13, frequency=50)
footR = servo.Servo(pwm4)

def rotate(limb, angle, delay, min, max):
    for x in range(angle, min, max, angle):
        limb.angle = x
        time.sleep(delay)

###################################
# define basic dance move functions 

# rotates right foot outwards and back in
def rightShuffle():
    footR.throttle = 0.0

    rotate(legL, 0.1, 0.05, 0, 90)
    rotate(legR, -0.1, 0.05, 180, 90)
    

# rotates left foot outwards and back in
def leftShuffle():
    footL.throttle = 0.1
    
    angle = -0.3
    while angle < 0.8:  # 0 - 180 degrees, 5 degrees at a time.
        legL.throttle = angle
        time.sleep(0.05)
        angle = angle + 0.1
    while angle >= -0.3:  # 0 - 180 degrees, 5 degrees at a time.
        legL.throttle = angle
        time.sleep(0.05)
        angle = angle - 0.1
    
    footL.throttle = 0.1


# rotate both feet outwards at the same time (simultaneous leftShuffle and rightShuffle)
def butterfly(): 
    footR.throttle = 0.0
    footL.throttle = 0.1

    angle = -0.5
    while angle < 0.5:  # 0 - 180 degrees, 5 degrees at a time.
        legR.throttle = angle
        legL.throttle = angle + 0.2
        time.sleep(0.05)
        angle = angle + 0.1
    while angle >= -0.5:  # 0 - 180 degrees, 5 degrees at a time.
        legR.throttle = angle
        legL.throttle = angle + 0.2
        time.sleep(0.05)
        angle = angle - 0.1
    
    footR.throttle = 0.0
    footL.throttle = 0.1


# lift upwards by pointing both feet
def jump():
    legR.throttle = 0.1
    legL.throttle = 0.1
    footR.throttle = 0.1
    footL.throttle = 0.1
    time.sleep(2)
    
    angle = 0.1
    while angle < 0.4:  # 0 - 180 degrees, 5 degrees at a time.
        footL.throttle = angle
        footR.throttle = 0.1  - angle
        time.sleep(0.1)
        angle = angle + 0.05
    time.sleep(1)
    while angle >= 0.1:  # 0 - 180 degrees, 5 degrees at a time.
        footL.throttle = angle
        footR.throttle = 0.1 - angle
        time.sleep(0.1)
        angle = angle - 0.05


# moves right leg forward and back down
def rightKick():
    legR.throttle = -0.8
    
    angle = 0.0
    while angle < 0.7:  # 0 - 180 degrees, 5 degrees at a time.
        footR.throttle = angle
        time.sleep(0.05)
        angle = angle + 0.1
    while angle >= -0.1:  # 0 - 180 degrees, 5 degrees at a time.
        footR.throttle = angle
        time.sleep(0.05)
        angle = angle - 0.1
    
    legR.throttle = -0.8


# moves left leg forward and back down
def leftKick():
    legL.throttle = 0.9
    
    angle = 0.3
    while angle > -0.7:  # 0 - 180 degrees, 5 degrees at a time.
        footL.throttle = angle
        time.sleep(0.05)
        angle = angle - 0.1
    while angle <= 0.3:  # 0 - 180 degrees, 5 degrees at a time.
        footL.throttle = angle
        time.sleep(0.05)
        angle = angle + 0.1
    
    legL.throttle = 0.9


# takes a step forward by lifting right foot
def rightStep():
    footL.throttle = 0.1
    legL.throttle = 0.0
    
    footR.throttle = 0.1
    legR.throttle = 0.1
    time.sleep(3)
    
    angleL = 0.1
    while angleL >= -0.2:  # 0 - 180 degrees, 5 degrees at a time.
        footR.throttle = angleL
        time.sleep(0.05)
        angleL = angleL - 0.05
        
    angleF = 0.1
    while angleF >= -0.4:  # 0 - 180 degrees, 5 degrees at a time.
        legR.throttle = angleF
        time.sleep(0.05)
        angleF = angleF - 0.1


#TODO debug/ test this move
# takes a step forward by lifting left foot
def leftStep():
    footL.throttle = 0.1
    legL.throttle = 0.0
    
    footR.throttle = 0.1
    legR.throttle = 0.1
    time.sleep(3)
    
    angleL = 0.1
    while angleL <= 0.3:  # 0 - 180 degrees, 5 degrees at a time.
        footL.throttle = angleL
        time.sleep(0.05)
        angleL = angleL - 0.05
        
    angleF = 0.1
    while angleF >= -0.4:  # 0 - 180 degrees, 5 degrees at a time.
        legL.throttle = angleF
        time.sleep(0.05)
        angleF = angleF - 0.1



##############################################
# define dance moves as sequences of basic moves

#Dance 1: walk forward
def walk():
    if (not check_distance):
        return

    for i in range(6):
        leftStep()
        play_note(DEFAULT[i * 2])
        time.sleep(0.5)
        rightStep()
        play_note(DEFAULT[i * 2 + 1])
        time.sleep(0.5)

#Dance 2: kick feet outwards one at a time
def shuffle():
    if (not check_distance):
        return

    for i in range(4):
        leftShuffle()
        play_note(CANON[i * 2])
        time.sleep(0.05)
        rightShuffle()
        play_note(CANON[i * 2 + 1])
        time.sleep(0.05)

# Dance 3: kick both feet outwards at the same time then tippy toe
def ballerina():
    if (not check_distance):
        return

    butterfly()
    play_note(CRIMSON[i * 2])
    time.sleep(0.05)
    jump()
    play_note(CRIMSON[i * 2 + 1])
    time.sleep(0.05)

#Dance 4: line dancing move
def pigeon():
    if (not check_distance):
        return

    leftShuffle()
    play_note(TETRIS[i * 4])
    time.sleep(0.05)
    leftKick()
    play_note(TETRIS[i * 4 + 1])
    time.sleep(0.2)
    rightShuffle()
    play_note(TETRIS[i * 4 + 2])
    time.sleep(0.05)
    rightKick()
    play_note(TETRIS[i * 4 + 3])
    time.sleep(1)

#Dance 5: up and down
def excite():
    if (not check_distance):
        return

    for i in range(4):
        jump()
        play_note(ANTHEM[i])
        time.sleep(0.1)

#Dance 6: left karate kick
def karate():
    if (not check_distance):
        return
        
    for i in range(4):
        leftShuffle()
        play_note(MARIO[i * 3])
        time.sleep(0.1)
        jump()
        play_note(MARIO[i * 3 + 1])
        time.sleep(0.1)
        leftKick()
        play_note(MARIO[i * 3 + 2])
        time.sleep(0.5)

# function for checking if robot is close to an object
def check_distance():
    try:
        if sonar.distance < THRESHOLD:
            return 0
    except RuntimeError:
        return 0
    return 1