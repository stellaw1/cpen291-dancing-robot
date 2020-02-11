#------------------------------------------------------------------------------------------------------#  
# Authors: Manek, Sanjeev, Parsa, Amir, Stella, Arnold, Rain
#
# Function: Dancing Robot
# 
# Date: 10/02/2020    
#------------------------------------------------------------------------------------------------------#    
import time
import board
import displayio
import terminalio
import label
from adafruit_st7735r import ST7735R
import digitalio
import adafruit_matrixkeypad
from enum import Enum, auto
import pulseio
import servo
import adafruit_hcsr04

#------------------------------------------------------------------------------------------------------#
# 
# display code  
#    
#------------------------------------------------------------------------------------------------------#    
class states(Enum):
    LOADING = auto()
    PASSCODE = auto()
    HOME = auto()
    DANCE = auto()
    MUSIC = auto()
    ABOUT = auto()
    EXIT = auto()
    REQUEST = auto()

def reset():
    displayio.release_displays()
    spi = board.SPI()
    tft_cs = board.D5
    tft_dc = board.D9
    display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D7)
    display = ST7735R(display_bus, width=128, height=128, colstart=2, rowstart=1)
    global splash
    display.show(splash)
    color_bitmap = displayio.Bitmap(128, 128, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF # White
    bg_white = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_white)

def textshow(textin, bgcolor, xc, yc, timein)
    text_area = label.Label(terminalio.FONT, text=textin, color=bgcolor, x=xc, y=yc)
    splash.append(text_area)
    for i in range(timein):
        pass
        time.sleep(1)

 def textout(textin, bgcolor, xc, yc)
    text_area = label.Label(terminalio.FONT, text=textin, color=bgcolor, x=xc, y=yc)
    splash.append(text_area)
    While(True):
        pass

#------------------------------------------------------------------------------------------------------#
# 
# keypad code   
#  
#------------------------------------------------------------------------------------------------------#    

# Setting up input pins
# Board D13 to keypad pin 1
row0 = digitalio.DigitalInOut(board.A4)
row0.direction = digitalio.Direction.INPUT
row0.pull = digitalio.Pull.UP
#Board D12 to keypad pin 2a
row1 = digitalio.DigitalInOut(board.A5)
row1.direction = digitalio.Direction.INPUT
row1.pull = digitalio.Pull.UP
#Board D11 to keypad pin 3
# row2 = digitalio.DigitalInOut(board.D11)
# row2.direction = digitalio.Direction.INPUT
# row2.pull = digitalio.Pull.UP
# #Board D10 to keypad pin 4
# row3 = digitalio.DigitalInOut(board.D10)
# row3.direction = digitalio.Direction.INPUT
# row3.pull = digitalio.Pull.UP

out1 = digitalio.DigitalInOut(board.D9)
out1.direction = digitalio.Direction.OUTPUT
out1.value = False

out2 = digitalio.DigitalInOut(board.D9)
out2.direction = digitalio.Direction.OUTPUT
out2.value = False

# #Board D9 to keypad pin 5
# col0 = digitalio.DigitalInOut(board.D9)
# col0.direction = digitalio.Direction.OUTPUT
# col0.value = False;
# #Board D6 to keypad pin 6
# col1 = digitalio.DigitalInOut(board.D6)
# col1.direction = digitalio.Direction.OUTPUT
# # col1.pull = digitalio.Pull.UP
# col1.value = False;
# #Board D5 to keypad pin 7
# col2 = digitalio.DigitalInOut(board.D5)
# col2.direction = digitalio.Direction.OUTPUT
# col2.value = False;

# col0 = (out1 && !out2)
# col1 = (out2 && !out1)
# col2 = (out1 && out2)

# Membrane 3x4 matrix keypad 
# cols = [digitalio.DigitalInOut(x) for x in (col0, col1, col2)]
rows = [digitalio.DigitalInOut(x) for x in (board.A4, board.A5)]
 
# define key values using a tuple
keys = ((1, 2, 3),
        (4, 5, 6)#,
        # (7, 8, 9),
        # ('*', 0, '#')
        )
 
# keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

def kypadDecode():
    key = 0
    for i in range(1,4):
        time.sleep(.1)
        if i == 1:
            out1.value = True
            out2.value = False
        if i == 2:
            out2.value = True
            out1.value = False
        if i == 3:
            out1.value = True
            out2.value = True
        key = keypadHelper(i)
        if key != 0:
            return key
    return key

def keypadHelper(col):
    count = 0
    for x in (rows):
        if not x.value:
            return col + count
        count += 3
    return 0

def checkPass():
    seq = []
    pwd = [1, 3, 5, '*']
    i = 0

    while True: 
        # keys = keypad.pressed_keys
        keys = keypadDecode()
        if keys: 
            seq.append(keys)
            i = i + 1
            time.sleep(0.4)

        if i >= 4: 
            if seq == pwd: 
                seq = []
                i = 0
                return True
            else: 
                seq = []
                return False

        time.sleep(0.1)
               
#------------------------------------------------------------------------------------------------------#
# 
# gui code
#     
#------------------------------------------------------------------------------------------------------#    

state = states.PASSCODE
while True:

    if state == states.LOADING:
        splash = displayio.Group(max_size=10)
        reset()
        time.sleep(0.5)
        textshow("Loading.....", 0x000000, 30, 64, 3)
        reset()
        time.sleep(0.3)
        textshow("Welcome", 0x000000, 30, 64, 3)
        reset()
        time.sleep(0.5)
        textshow("CPEN 291", 0x000000, 30, 64, 3)
        reset()
        time.sleep(0.5)
        state = states.PASSCODE

    if state == states.PASSCODE:
        textout("enter the passcode", 0x000000, 10, 60)
        boolean = False
        boolean = checkPass()
        if boolean:
            boolean = False
            state = states.HOME
            reset()
        else:
            state = state.PASSCODE
        
    elif state == states.HOME:
        textout("Press a key: \n 1) Dance Menu \n 2) Music \n 3) Exit \n 4) About ", 0x000000, 10, 60)

        keys = 0
        while keys == 0:
            keys = keypadDecode()

        if keys == [1]:
            state = states.DANCE
            reset()
        elif keys == [2]:
            state = states.MUSIC
            reset()
        elif keys == [3]:
            state = states.EXIT
            reset()
        elif keys == [4]:
            state = states.ABOUT
        else
            state = states.HOME
        
    elif state == states.DANCE:
        textout("Press a key: \n 1) Shuffle \n 2) Kick \n 3) Moonwalk \n 5) Wobble \n 5) Squat \n 6) Spin", 0x000000, 10, 60)

        keys =0
        while keys == 0:
            keys = keypadDecode()

        if keys == [1]:
            dance1()
            state = states.REQUEST
            reset()
        elif keys == [2]:
            dance2()
            state = states.REQUEST
            reset()
        elif keys == [3]:
            dance3()
            state = states.REQUEST
            reset()
        elif keys == [4]:
            dance4()
            state = states.REQUEST
            reset()
        elif keys == [5]:
            dance5()
            state = states.REQUEST
            reset()
        elif keys == [6]:
            dance6()
            state = states.REQUEST
            reset()
        else:
            state = states.DANCE

    elif state == states.ABOUT:
        textout("About: \n Dancing Robot GUI \n Components: \n 1)Itsy Bitsy \n 2)TFT LCD \n 3)Servos \n 4)Ultrasonic sensor \n 5)Buzzer \n6)Keypad \n 7)RGB module/Shifter with LEDS \n Steps:\n 1)Power up: Welcome Menu that requests password\n 2)If password accepted a new window opens with a menu that has 6 dance moves to choose from If declined request for password again \n3)Press one of the first six buttons to do a dance (with particular music) move for a certain amount of time \n4)Come back to main menu\n 5)Might be able to display temperature as well (default lib / DHT11)", 0x000000, 10, 10)
        time.sleep(5)
        textshow("press any button to return", 0x000000, 10, 60, 3)
       
        keys =0
        while keys == 0:
            keys = keypadDecode()

        if keys == [1]:
            state = states.HOME
            reset()
            textshow("Created By: \n 1)Manek \n  2)Sanjeev \n 3)Parsa \n 4)Amir \n 5)Stella \n 6)Arnold \n 7)Rain", 0x000000, 10, 60, 3)
            time.sleep(1)
            reset()
        elif keys == [2]:
            state = states.HOME
            reset()
            textshow("Created By: \n 1)Manek \n  2)Sanjeev \n 3)Parsa \n 4)Amir \n 5)Stella \n 6)Arnold \n 7)Rain", 0x000000, 10, 60, 3)
            time.sleep(1)
            reset()
        elif keys == [3]:
            state = states.HOME
            reset()
            textshow("Created By: \n 1)Manek \n  2)Sanjeev \n 3)Parsa \n 4)Amir \n 5)Stella \n 6)Arnold \n 7)Rain", 0x000000, 10, 60, 3)
            time.sleep(1)
            reset()
        elif keys == [4]:
            state = states.HOME
            reset()
            textshow("Created By: \n 1)Manek \n  2)Sanjeev \n 3)Parsa \n 4)Amir \n 5)Stella \n 6)Arnold \n 7)Rain", 0x000000, 10, 60, 3)
            time.sleep(1)
            reset()
        elif keys == [5]:
            state = states.HOME
            reset()
            textshow("Created By: \n 1)Manek \n  2)Sanjeev \n 3)Parsa \n 4)Amir \n 5)Stella \n 6)Arnold \n 7)Rain", 0x000000, 10, 60, 3)
            time.sleep(1)
            reset()
        elif keys == [6]:
            state = states.HOME
            reset()
            textshow("Created By: \n 1)Manek \n  2)Sanjeev \n 3)Parsa \n 4)Amir \n 5)Stella \n 6)Arnold \n 7)Rain", 0x000000, 10, 60, 3)
            time.sleep(1)
            reset()
        else:
            state = states.ABOUT

    elif state == states.EXIT:
        textshow("Exiting.....", 0x000000, 30, 64, 3)
        time.sleep(0.5)
        state = states.PASSCODE
        reset()

    elif state == states.REQUEST:
        textout("Press a key: \n 1) Dance  \n 2) Play Music \n 3) Home", 0x000000, 10, 60)
        
        keys = 0
        while keys == 0:
            keys = keypadDecode()

        if keys == [1]:
            state = states.DANCE
            reset()
        elif keys == [2]:
            state = states.MUSIC
            reset()
        elif keys == [3]:
            state = states.HOME
            reset()
        else:
            state = states.REQUEST

    elif state == states.MUSIC:
        textout("Press a key: \n 1) song1 \n 2) song2 \n 3) song3 \n 5) song4 \n 5) song5 \n 6) song6", 0x000000, 10, 60)

        keys = 0
        while keys == 0:
            keys = keypadDecode()

        if keys == [1]:
            song1()
            state = states.REQUEST
            reset()
        elif keys == [2]:
            song2()
            state = states.REQUEST
            reset()
        elif keys == [3]:
            song3()
            state = states.REQUEST
            reset()
        elif keys == [4]:
            song4()
            state = states.REQUEST
            reset()
        elif keys == [5]:
            song5()
            state = states.REQUEST
            reset()
        elif keys == [6]:
            song6()
            state = states.REQUEST
            reset()
        else:
            state = states.MUSIC

#------------------------------------------------------------------------------------------------------#
#
# songs code 
#     
#------------------------------------------------------------------------------------------------------#    

def song1():

    timeout = time.time() + 30 
    while True:

        if time.time() > timeout:
            break

        for f in (196, 277, 196, 220, 247, 165, 165, 233, 196, 174, 208, 131, 131, 156, 147, 165, 185, 174, 196, 233, 123,
                262, 311, 311, 196, 330, 294, 261, 311, 247, 196, 277, 247, 220, 247, 165, 165, 233, 196, 131, 131, 277,
                247, 220, 207, 207, 207):
            piezo.frequency = f
            piezo.duty_cycle = 65536 // 2  # On 50%
            time.sleep(0.25)  # On for 1/4 second
            piezo.duty_cycle = 0  # Off
            time.sleep(0.05)  # Pause between notes
        time.sleep(0.5) 

def song2():
    
    timeout = time.time() + 30 
    while True:
        
        if time.time() > timeout:
            break

        for f in ():
            piezo.frequency = f
            piezo.duty_cycle = 65536 // 2  # On 50%
            time.sleep(0.25)  # On for 1/4 second
            piezo.duty_cycle = 0  # Off
            time.sleep(0.05)  # Pause between notes
        time.sleep(0.5) 

def song3():

    timeout = time.time() + 30 
    while True:
        
        if time.time() > timeout:
            break

        for f in (): #enter the song frequency here):
            piezo.frequency = f
            piezo.duty_cycle = 65536 // 2  # On 50%
            time.sleep(0.25)  # On for 1/4 second
            piezo.duty_cycle = 0  # Off
            time.sleep(0.05)  # Pause between notes
        time.sleep(0.5) 

def song4():

    timeout = time.time() + 30 
    while True:
        
        if time.time() > timeout:
            break

        for f in (): #enter the song frequency here):
            piezo.frequency = f
            piezo.duty_cycle = 65536 // 2  # On 50%
            time.sleep(0.25)  # On for 1/4 second
            piezo.duty_cycle = 0  # Off
            time.sleep(0.05)  # Pause between notes
        time.sleep(0.5)  

def song5():

    timeout = time.time() + 30 
    while True:
        
        if time.time() > timeout:
            break

        for f in (): #enter the song frequency here):
            piezo.frequency = f
            piezo.duty_cycle = 65536 // 2  # On 50%
            time.sleep(0.25)  # On for 1/4 second
            piezo.duty_cycle = 0  # Off
            time.sleep(0.05)  # Pause between notes
        time.sleep(0.5)  

def song6():

    timeout = time.time() + 30 
    while True:
        
        if time.time() > timeout:
            break

        for f in (): #enter the song frequency here):
            piezo.frequency = f
            piezo.duty_cycle = 65536 // 2  # On 50%
            time.sleep(0.25)  # On for 1/4 second
            piezo.duty_cycle = 0  # Off
            time.sleep(0.05)  # Pause between notes
        time.sleep(0.5)    

#------------------------------------------------------------------------------------------------------#
# 
# dance code
#     
#------------------------------------------------------------------------------------------------------#        

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

def dance1():
    pass
def dance2():
    pass
def dance3():
    pass
def dance4():
    pass
def dance5():
    pass
def dance6():
    pass

#------------------------------------------------------------------------------------------------------#
#
# ultrasonic sensor code
#      
#------------------------------------------------------------------------------------------------------#    

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D4, echo_pin=board.D3)
threshold = 0.3


while True:
    try:
        print((sonar.distance,))
        if sonar.distance < threshold:
            print("Detected")
    except RuntimeError:
        print("Retrying!")
    time.sleep(0.1)