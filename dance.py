import time
import board
import pulseio
import servo

###########################################
# pin assignments and initial setup

#buzzer setup
piezo = pulseio.PWMOut(board.A1 , duty_cycle=0, frequency=440, variable_frequency=True)

#servo setup
pwm1 = pulseio.PWMOut(board.D10, frequency=50) #leg1
legL = servo.ContinuousServo(pwm1)

pwm2 = pulseio.PWMOut(board.D11, frequency=50) #leg2
legR = servo.ContinuousServo(pwm2)

pwm3 = pulseio.PWMOut(board.D12, frequency=50)
footL = servo.ContinuousServo(pwm3)

pwm4 = pulseio.PWMOut(board.D13, frequency=50)
footR = servo.ContinuousServo(pwm4)



###################################
# define buzzer song functions

#Song 1: Russia national anthem
def USSR_anthem():
    for f in (196, 277, 196, 220, 247, 165, 165, 233, 196, 174, 208, 131, 131, 156, 147, 165, 185, 174, 196, 233, 123,
            262, 311, 311, 196, 330, 294, 261, 311, 247, 196, 277, 247, 220, 247, 165, 165, 233, 196, 131, 131, 277,
            247, 220, 207, 207, 207):
        piezo.frequency = f
        piezo.duty_cycle = 65536 // 2  # On 50%
        time.sleep(0.25)  # On for 1/4 second
        piezo.duty_cycle = 0  # Off
        time.sleep(0.05)  # Pause between notes
    time.sleep(0.5)

#Song 2: Mario main theme melody
#Source: https://www.princetronics.com/supermariothemesong/
def mario_theme():
    for f in (2637, 2637, 0, 2637, 0, 2093, 2637, 0, 3136, 0, 0,  0, 1568, 0, 0, 0,
            2093, 0, 0, 1568, 0, 0, 1319, 0, 0, 1760, 0, 1976, 0, 1865, 1760, 0,
            1568, 2637, 3136, 3520, 0, 2794, 3136, 0, 2637, 0, 2093, 2349, 1976, 0, 0,
            2093, 0, 0, 1568, 0, 0, 1319, 0, 0, 1760, 0, 1976, 0, 1865, 1760, 0,
            1568, 2637, 3136, 3520, 0, 2794, 3136, 0, 2637, 0, 2093, 2349, 1976, 0, 0):
        piezo.frequency = f
        piezo.duty_cycle = 65536 // 2  # On 50%
        time.sleep(0.25)  # On for 1/4 second
        piezo.duty_cycle = 0  # Off
        time.sleep(0.05)  # Pause between notes
    time.sleep(0.5)

#Song 3: all i want for christmas intro
def crimson():
    for f in (196, 247, 294, 370, 392, 370, 294, 247, 196, 262, 294, 392, 294):
        piezo.frequency = f
        piezo.duty_cycle = 65536 // 2  # On 50%
        time.sleep(0.25)  # On for 1/4 second
        piezo.duty_cycle = 0  # Off
        time.sleep(0.05)  # Pause between notes
    time.sleep(0.5)

#Song 4: pachebel Canon in C
def canon():
    for f in (131, 165, 196, 262, 98, 123, 147, 196, 110, 131, 165, 220, 82, 98, 123, 165, 87, 110, 131, 175, 
            131, 165, 196, 262, 87, 110, 131, 175, 98, 123, 147, 196, 110):
        piezo.frequency = f
        piezo.duty_cycle = 65536 // 2  # On 50%
        time.sleep(0.25)  # On for 1/4 second
        piezo.duty_cycle = 0  # Off
        time.sleep(0.05)  # Pause between notes
    time.sleep(0.5)




###################################
# define basic dance move functions 

# rotates right foot outwards and back in
def rightShuffle():
    footR.throttle = 0.0
    
    angle = -0.5
    while angle < 0.5:  # 0 - 180 degrees, 5 degrees at a time.
        legR.throttle = angle
        time.sleep(0.05)
        angle = angle + 0.1
    while angle >= -0.5:  # 0 - 180 degrees, 5 degrees at a time.
        legR.throttle = angle
        time.sleep(0.05)
        angle = angle - 0.1
    
    footR.throttle = 0.0
    

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
    USSR_anthem()

    for i in range(6):
        leftStep()
        time.sleep(0.5)
        rightStep()
        time.sleep(0.5)

#Dance 2: kick feet outwards one at a time
def shuffle():
    mario_theme()

    for i in range(4):
        leftShuffle()
        time.sleep(0.05)
        rightShuffle()
        time.sleep(0.05)

# Dance 3: kick both feet outwards at the same time then tippy toe
def ballerina():
    canon()

    butterfly()
    time.sleep(0.05)
    jump()
    time.sleep(0.05)

#Dance 4: line dancing move
def pigeon():
    leftShuffle()
    time.sleep(0.05)
    leftKick()
    time.sleep(0.2)
    rightShuffle()
    time.sleep(0.05)
    rightKick()
    time.sleep(1)

#Dance 5: up and down
def excite(): 
    crimson()

    for i in range(4):
        jump()
        time.sleep(0.1)

#Dance 6: left karate kick
def karate(): 
    leftShuffle()
    time.sleep(0.1)
    jump()
    time.sleep(0.1)
    leftKick()
    time.sleep(0.5)