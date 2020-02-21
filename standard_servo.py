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

def rotate(limb, angle, delay, min, max, song):
    i = 0
    for x in range(min, max, angle):
        dance(limb, x)
        play_note(song[i % (len(song) - 1)])
        i += 1


def dance(limb, angle):
    limb.angle = angle

def play_note(freq, delay):
    piezo.frequency = freq
    piezo.duty_cycle = 65536 // 2  # On 50%
    time.sleep(delay)  # On
    piezo.duty_cycle = 0  # Off



###################################
# define basic dance move functions

ANTHEM = [196, 277, 196, 220, 247, 165, 165, 233, 196, 174, 208, 131, 131, 156, 147, 165, 185, 174, 196, 233, 123,
            262, 311, 311, 196, 330, 294, 261, 311, 247, 196, 277, 247, 220, 247, 165, 165, 233, 196, 131, 131, 277,
            247, 220, 207, 207, 207]

MARIO = [2637, 2637, 0, 2637, 0, 2093, 2637, 0, 3136, 0, 0,  0, 1568, 0, 0, 0,
            2093, 0, 0, 1568, 0, 0, 1319, 0, 0, 1760, 0, 1976, 0, 1865, 1760, 0,
            1568, 2637, 3136, 3520, 0, 2794, 3136, 0, 2637, 0, 2093, 2349, 1976, 0, 0,
            2093, 0, 0, 1568, 0, 0, 1319, 0, 0, 1760, 0, 1976, 0, 1865, 1760, 0,
            1568, 2637, 3136, 3520, 0, 2794, 3136, 0, 2637, 0, 2093, 2349, 1976, 0, 0]

CRIMSON = [196, 247, 294, 370, 392, 370, 294, 247, 196, 262, 294, 392, 294]

CANON = [131, 165, 196, 262, 98, 123, 147, 196, 110, 131, 165, 220, 82, 98, 123, 165, 87, 110, 131, 175,
            131, 165, 196, 262, 87, 110, 131, 175, 98, 123, 147, 196, 110]

TETRIS = [659, 494, 523, 587, 659, 587, 523, 494, 440, 440, 523, 659, 587, 523, 494, 494, 494, 523, 587, 523,
            494, 494, 494, 523, 587, 659, 523, 440, 440, 587, 587, 698, 880, 784, 698, 659, 659, 523, 659, 587,
            523, 494, 494, 523, 587, 659, 523, 440, 440, 659, 494, 523, 587, 659, 587, 523, 494, 440, 440, 523,
            659, 587, 523, 494, 494, 523, 587, 659, 523, 440, 440, 587, 587, 698, 880, 784, 698, 659, 659, 523,
            659, 587, 523, 587, 659, 523, 440, 440]

DEFAULT = [149, 149, 149, 446, 1485, 149, 149, 149, 446, 297, 297, 149, 595, 149, 149, 149, 149, 1931]

# rotates right foot outwards and back in
def rightShuffle():
    footR.throttle = 0.0

    for i in range (len(TETRIS) / 2):
        rotate(legL, 5, 0.05, 0, 90, 0.01, TETRIS[i])
        rotate(legR, -5, 0.05, 180, 90, 0.01, TETRIS[i+1])

def playMusic(song, delay):
    for i in range(len(song) - 1)
        piezo.frequency = song[i]
        piezo.duty_cycle = 65536 // 2  # On 50%
        time.sleep(delay)  # On
        piezo.duty_cycle = 0  # Off

'''
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
'''
rotate(legL, 1, 0.05, 0, 90, TETRIS)