import time
import board
import pulseio
import servo

pwm1 = pulseio.PWMOut(board.D10, frequency=50) #leg1
legL = servo.ContinuousServo(pwm1)

pwm2 = pulseio.PWMOut(board.D11, frequency=50) #leg2
legR = servo.ContinuousServo(pwm2)

pwm3 = pulseio.PWMOut(board.D12, frequency=50)
footL = servo.ContinuousServo(pwm3)

pwm4 = pulseio.PWMOut(board.D13, frequency=50)
footR = servo.ContinuousServo(pwm4)

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


##############################################
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