import time
import board
import pulseio
import servo

import adafruit_hcsr04

# piezo buzzer setup
piezo = pulseio.PWMOut(board.A1 , duty_cycle=0, frequency=440, variable_frequency=True)

# servo setup
pwm1 = pulseio.PWMOut(board.D10, frequency=50)
legL = servo.Servo(pwm1)

pwm2 = pulseio.PWMOut(board.D11, frequency=50)
legR = servo.Servo(pwm2)

pwm3 = pulseio.PWMOut(board.D12, frequency=50)
footR = servo.Servo(pwm3)

pwm4 = pulseio.PWMOut(board.D13, frequency=50)
footL = servo.Servo(pwm4)


###################################
# frequency lists for the six songs

ANTHEM = [196, 277, 196, 220, 247, 165, 165, 233, 196, 174, 208, 131, 131, 156, 147, 165, 185, 174, 196, 233, 123,
            262, 311, 311, 196, 330, 294, 261, 311, 247, 196, 277, 247, 220, 247, 165, 165, 233, 196, 131, 131, 277,
            247, 220, 207, 207, 207]

MARIO = [659, 659, 659, 523, 659, 784, 392, 523, 392, 330, 440, 494, 466, 440, 392, 659, 784, 880, 698, 784, 659, 
            523, 587, 494, 523, 392, 330, 440, 494, 466, 440, 392, 659, 784, 880, 698, 784, 659, 523, 587, 494]

STRANGER = [131, 165, 196, 247, 262, 247, 196, 165]

CRIMSON = [523, 659, 784, 494]

CANON = [131, 165, 196, 262, 98, 123, 147, 196, 110, 131, 165, 220, 82, 98, 123, 165, 87, 110, 131, 175,
            131, 165, 196, 262, 87, 110, 131, 175, 98, 123, 147, 196, 110]

TETRIS = [659, 494, 523, 587, 659, 587, 523, 494, 440, 440, 523, 659, 587, 523, 494, 494, 494, 523, 587, 523,
            494, 494, 494, 523, 587, 659, 523, 440, 440, 587, 587, 698, 880, 784, 698, 659, 659, 523, 659, 587,
            523, 494, 494, 523, 587, 659, 523, 440, 440, 659, 494, 523, 587, 659, 587, 523, 494, 440, 440, 523,
            659, 587, 523, 494, 494, 523, 587, 659, 523, 440, 440, 587, 587, 698, 880, 784, 698, 659, 659, 523,
            659, 587, 523, 587, 659, 523, 440, 440]

DEFAULT = [149, 149, 149, 446, 1485, 149, 149, 149, 446, 297, 297, 149, 595, 149, 149, 149, 149, 1931]


def playSong(song, delay):
    for i in range (len(song)):
        piezo.frequency = song[i]
        piezo.duty_cycle = 65536 // 2  # On 50%
        time.sleep(delay)  # On


############################
# basic dance move functions

def rotate(limb, min, max, step, start, song):
    i = start
    for x in range(min, max + step, step):
        limb.angle = x
        play_note(song[i % len(song)], 0.3)
        i += 1
    return i

def double_rotate(limb1, limb2, min, max, step, start, song):
    i = start
    for x in range(min, max + step, step):
        limb1.angle = x
        limb2.angle = x
        play_note(song[i % len(song)], 0.3)
        i += 1
    return i

def tapLeftFoot(start, song):
    start = rotate(footL, 90, 60, -10, start, song)
    start = rotate(footL, 60, 90, 10, start, song)
    return start
    
def tapRightFoot(start, song):
    start = rotate(footR, 100, 130, 10, start, song)
    start = rotate(footR, 130, 100, -10, start, song)
    return start

def rightKick(start, song):
    legR.angle = 160
    start = rotate(footR, 100, 60, -10, start, song)
    start = rotate(footR, 60, 100, 10, start, song)
    legR.angle = 90
    return start

def leftKick(start, song):
    legL.angle = 20
    start = rotate(footL, 90, 130, 10, start, song)
    start = rotate(footL, 130, 90, -10, start, song)
    legL.angle = 90
    return start

def leftFootIn(start, song):
    start = rotate(legL, 90, 170, 10, start, song)
    start = rotate(legL, 170, 90, -10, start, song)
    return start

def rightFootIn(start, song):
    start = rotate(legR, 90, 10, -10, start, song)
    start = rotate(legR, 10, 90, 10, start, song)
    return start
    
def leftFootOut(start, song):
    start = rotate(legL, 90, 20, -10, start, song)
    start = rotate(legL, 20, 90, 10, start, song)
    return start

def rightFootOut(start, song):
    start = rotate(legR, 90, 160, 10, start, song)
    start = rotate(legR, 160, 90, -10, start, song)
    return start

def wiggle(start, song):
    start = rotate(footL, 90, 130, 10, start, song)
    start = rotate(footR, 100, 60, -10, start, song)
    start = rotate(footL, 130, 90, -10, start, song)
    start = rotate(footR, 60, 100, 10, start, song)
    return start

def shuffle(start, song):
    for angle in range(90, 30, -15):  # 0 - 180 degrees, 5 degrees at a time.
        start = double_rotate(legL, legR, angle, angle, -15, start, song)
    for angle in range(30, 90, 15): # 180 - 0 degrees, 5 degrees at a time.
        start = double_rotate(legL, legR, angle, angle, 15, start, song)
    for angle in range(90, 120, 15):  # 0 - 180 degrees, 5 degrees at a time.
        start = double_rotate(legL, legR, angle, angle, -15, start, song)
    for angle in range(120, 90, -15): # 180 - 0 degrees, 5 degrees at a time.
        start = double_rotate(legL, legR, angle, angle, 15, start, song)
    return start


###################################################################
# 6 dance moves created as a combination of the smaller moves above

def dance1():
    start = 0
    reset()
    for i in range(3):
        start = wiggle(start, STRANGER)
    reset()

def dance2():
    start = 0
    for i in range(2):
        start = leftFootOut(start, MARIO)
        start = leftFootIn(start, MARIO)
        start = rightFootOut(start, MARIO)
        start = rightFootIn(start, MARIO)

def dance3():
    start = 0
    start = leftFootOut(start, ANTHEM)
    start = tapLeftFoot(start, ANTHEM)
    start = leftKick(start, ANTHEM)

    start = rightFootOut(start, ANTHEM)
    start = tapRightFoot(start, ANTHEM)
    start = rightKick(start, ANTHEM)

def dance4():
    start = 0
    for j in range(3):
        start = tapLeftFoot(start, TETRIS)
    for j in range(3):
        start = tapRightFoot(start, TETRIS)

def dance5():
    start = 0
    for i in range(3):
        start = leftKick(start, CANON)
        start = rightKick(start, CANON)

def dance6():
    start = 0
    for i in range(3):
        start = shuffle(start, DEFAULT)