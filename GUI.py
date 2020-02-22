#------------------------------------------------------------------------------------------------------#  
# Authors: Manek, Sanjeev, Parsa, Amir, Stella, Arnold, Rain
#
# Function: Dancing Robot
# 
# Date: 10/02/2020    
#------------------------------------------------------------------------------------------------------#    

import time
import sys
import board
import displayio
import terminalio
import label
from adafruit_st7735r import ST7735R
import digitalio
import adafruit_matrixkeypad
import pulseio
import servo
from analogio import AnalogIn
import adafruit_hcsr04


#------------------------------------------------------------------------------------------------------#
# 
# sonar code
#     
#------------------------------------------------------------------------------------------------------#    
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D4, echo_pin=board.D3)
threshold = 5

# while True:
#     try:
#         print((sonar.distance,))
#         if sonar.distance < threshold:
#             print("Detected")
#     except RuntimeError:
#         print("Retrying!")
#     time.sleep(0.1)

def checkSonar():
    try:
        distance = sonar.distance
        return distance < threshold
    except RuntimeError:
        return False

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

row1 = digitalio.DigitalInOut(board.A5)
row1.direction = digitalio.Direction.INPUT
row1.pull = digitalio.Pull.UP

out1 = digitalio.DigitalInOut(board.A2)
out1.direction = digitalio.Direction.OUTPUT
out1.value = False

out2 = digitalio.DigitalInOut(board.A3)
out2.direction = digitalio.Direction.OUTPUT
out2.value = False

keys = ((1, 2, 3),
        (4, 5, 6))

def keypadDecode():
    key = 0
    for i in range(1,4):
        time.sleep(.1)
        if i == 1:
            out2.value = True
            out1.value = False
        if i == 2:
            out1.value = True
            out2.value = False
        if i == 3:
            out1.value = True
            out2.value = True
        key = keypadHelper(i)
        if key != 0:
            setColor("white")
            time.sleep(0.1)
            setColor("off")
            return key
    return key

def keypadHelper(col):
    if not row0.value:
        return col
    if not row1.value:
        return col+3
    return 0

def checkPass():
    seq = []
    pwd = [1, 1, 1, 1]
    i = 0

    while True:
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

def interrupt():
    keys = 0
    keys = keypadDecode()
    if keys != 0 or checkSonar():
        setColor("red")
        time.sleep(0.1)
        setColor("off")
        time.sleep(0.1)
        setColor("red")
        time.sleep(0.1)
        setColor("off")
        time.sleep(0.1)
        setColor("red")
        time.sleep(0.1)
        setColor("off")
        time.sleep(0.1)
        return True
    else:
        return False
               

#------------------------------------------------------------------------------------------------------#
# 
# dance code
#     
#------------------------------------------------------------------------------------------------------#        

# pin assignments and initial setup
pwm1 = pulseio.PWMOut(board.D10, duty_cycle=2 ** 15, frequency=50)
legR = servo.Servo(pwm1)

pwm2 = pulseio.PWMOut(board.D11, duty_cycle=2 ** 15, frequency=50) #leg2
legL = servo.Servo(pwm2)

pwm3 = pulseio.PWMOut(board.D12, duty_cycle=2 ** 15, frequency=50)
footL = servo.Servo(pwm3)

pwm4 = pulseio.PWMOut(board.D13, duty_cycle=2 ** 15, frequency=50)
footR = servo.Servo(pwm4)

#buzzer setup
piezo = pulseio.PWMOut(board.A1 , duty_cycle=0, frequency=440, variable_frequency=True)


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
    rotate(legL, 90, 180, 5)
    rotate(legL, 180, 90, -5)

def rightFootOut():
    rotate(legR, 90, 10, -5)
    rotate(legR, 10, 90, 5)
    
def leftFootIn():
    rotate(legL, 90, 20, -5)
    rotate(legL, 20, 90, 5)

def rightFootIn():
    rotate(legR, 90, 160, 5)
    rotate(legR, 160, 90, -5)

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


# song frequency arrays
ANTHEM = [196, 277, 196, 220, 247, 165, 165, 233, 196, 174, 208, 131, 131, 156, 147, 165, 185, 174, 196, 233, 123,
            262, 311, 311, 196, 330, 294, 261, 311, 247, 196, 277, 247, 220, 247, 165, 165, 233, 196, 131, 131, 277,
            247, 220, 207, 207, 207]

MARIO = [330, 330, 330, 262, 330, 392, 196, 262, 196, 165, 220, 247, 233, 220, 196, 330, 392, 440, 349, 392, 330, 
            262, 294, 247]

CRIMSON = [196, 247, 294, 370, 392, 370, 294, 247, 196, 262, 294, 392, 294]

CANON = [131, 165, 196, 262, 98, 123, 147, 196, 110, 131, 165, 220, 82, 98, 123, 165, 87, 110, 131, 175, 
            131, 165, 196, 262, 87, 110, 131, 175, 98, 123, 147, 196, 110]

TETRIS = [659, 494, 523, 587, 659, 587, 523, 494, 440, 440, 523, 659, 587, 523, 494, 494, 494, 523, 587, 523,
            494, 494, 494, 523, 587, 659, 523, 440, 440, 587, 587, 698, 880, 784, 698, 659, 659, 523, 659, 587, 
            523, 494, 494, 523, 587, 659, 523, 440, 440, 659, 494, 523, 587, 659, 587, 523, 494, 440, 440, 523, 
            659, 587, 523, 494, 494, 523, 587, 659, 523, 440, 440, 587, 587, 698, 880, 784, 698, 659, 659, 523,
            659, 587, 523, 587, 659, 523, 440, 440]

DEFAULT = [149, 149, 149, 446, 1485, 149, 149, 149, 446, 297, 297, 149, 595, 149, 149, 149, 149, 1931]


# define buzzer song functions
def play_note(freq):
    piezo.frequency = freq
    piezo.duty_cycle = 65536 // 2  # On 50%
    time.sleep(0.3) # On for 1/4 second
    piezo.duty_cycle = 0 # Off


# define 6 main dance moves

#1: slide to intro to All I Want for Christmas is You - Mariah Carey
def dance1():
    #reset()
    for i in range(0, 12, 1):
        play_note(CRIMSON[i])
        wiggle()
    #reset()


#2: line dance to the MARIO THEME song
def dance2():
    for i in range(0, len(MARIO) - 4, 4):
        play_note(MARIO[i])
        leftFootOut()
        play_note(MARIO[i+1])
        leftFootIn()
        play_note(MARIO[i+2])
        rightFootOut()
        play_note(MARIO[i+3])
        rightFootIn()


#3: karate kick to the USSR ANTHEM
def dance3():
    for i in range(0, len(ANTHEM) - 6, 6):
        play_note(ANTHEM[i])
        leftFootOut()
        play_note(ANTHEM[i+1])
        tapLeftFoot()
        play_note(ANTHEM[i + 2])
        leftKick()

        play_note(ANTHEM[i + 3])
        rightFootOut()
        play_note(ANTHEM[i + 4])
        tapRightFoot()
        play_note(ANTHEM[i + 5])
        rightKick()

#4: tap feet to the beat of Tetris background music
def dance4():
    for i in range(0, len(TETRIS) - 12, 12):
        for j in range(0, 3, 1):
            play_note(TETRIS[i + j])
            tapLeftFoot()
        for j in range(0, 3, 1):  
            play_note(TETRIS[i + 4 + j])
            tapRightFoot()
        for j in range(0, 3, 1):
            play_note(TETRIS[i + 8 + j])
            tapBothFeet()

#5: walk to Pachebel Canon in C
def dance5():
    for i in range(0, len(CANON) - 2, 2):
        play_note(CANON[i])
        leftKick()
        play_note(CANON[i + 1])
        rightKick()

#6: wiggle to the fortnite default song
def dance6():
    for i in range(0, len(DEFAULT) - 2, 2):
        play_note(DEFAULT[i])
        shuffle()

#------------------------------------------------------------------------------------------------------#
#
# songs code 
#     
#------------------------------------------------------------------------------------------------------#    

# setting up the piezo buzzer
#piezo = pulseio.PWMOut(board.A1 , duty_cycle=0, frequency=440, variable_frequency=True)

# define 6 songs

# USSR anthem
def song1():

    timeout = time.time() + 10 
    while True:

        if time.time() > timeout:
            break

        temp = False

        for f in (196, 277, 196, 220, 247, 165, 165, 233, 196, 174, 208, 131, 131, 156, 147, 165, 185, 174, 196, 233, 123,
            262, 311, 311, 196, 330, 294, 261, 311, 247, 196, 277, 247, 220, 247, 165, 165, 233, 196, 131, 131, 277,
            247, 220, 207, 207, 207):
            if interrupt():
                temp = True
                break
            piezo.frequency = f
            piezo.duty_cycle = 65536 // 2  # On 50%
            time.sleep(0.25)  # On for 1/4 second
            piezo.duty_cycle = 0  # Off
            time.sleep(0.05)  # Pause between notes
        if temp != False:
            break
        time.sleep(0.5)


# mario theme song
def song2():
    
    timeout = time.time() + 10 
    while True:
        
        if time.time() > timeout:
            break

        for f in (330, 330, 330, 262, 330, 392, 196, 262, 196, 165, 220, 247, 233, 220, 196, 330, 392, 440, 349, 392, 330, 
            262, 294, 247):
            if interrupt():
                temp = True
                break
            piezo.frequency = f
            piezo.duty_cycle = 65536 // 2  # On 50%
            time.sleep(0.25)  # On for 1/4 second
            piezo.duty_cycle = 0  # Off
            time.sleep(0.05)  # Pause between notes
        if temp != False:
            break
        time.sleep(0.5)

# crimson
def song3():

    timeout = time.time() + 10 
    while True:
        
        if time.time() > timeout:
            break

        for f in (196, 247, 294, 370, 392, 370, 294, 247, 196, 262, 294, 392, 294):
            if interrupt():
                temp = True
                break
            piezo.frequency = f
            piezo.duty_cycle = 65536 // 2  # On 50%
            time.sleep(0.25)  # On for 1/4 second
            piezo.duty_cycle = 0  # Off
            time.sleep(0.05)  # Pause between notes
        if temp != False:
            break
        time.sleep(0.5)

# canon
def song4():

    timeout = time.time() + 10 
    while True:
        
        if time.time() > timeout:
            break

        for f in (131, 165, 196, 262, 98, 123, 147, 196, 110, 131, 165, 220, 82, 98, 123, 165, 87, 110, 131, 175, 
            131, 165, 196, 262, 87, 110, 131, 175, 98, 123, 147, 196, 110):
            if interrupt():
                temp = True
                break
            piezo.frequency = f
            piezo.duty_cycle = 65536 // 2  # On 50%
            time.sleep(0.25)  # On for 1/4 second
            piezo.duty_cycle = 0  # Off
            time.sleep(0.05)  # Pause between notes
        if temp != False:
            break
        time.sleep(0.5)

# tetris
def song5():

    timeout = time.time() + 10 
    while True:
        
        if time.time() > timeout:
            break
        freq = [659, 494, 523, 587, 659, 587, 523, 494, 440, 440, 523, 659, 587, 523, 494, 494, 494, 523, 587, 659,
                523, 494, 494, 494, 523, 587, 659, 523, 440, 440, 587, 587, 698, 880, 784, 698, 659, 659, 523, 659,
                587, 523, 494, 494, 523, 587, 659, 523, 440, 440, 659, 494, 523, 587, 659, 587, 523, 494, 440, 440,
                523, 659, 587, 523, 494, 494, 523, 587, 659, 523, 440, 440, 587, 587, 698, 880, 784, 698, 659, 659,
                523, 659, 587, 523, 587, 659, 523, 440, 440]
        for f in range(0, len(freq) - 1):
            if interrupt():
                temp = True
                break
            piezo.frequency = freq[f]
            piezo.duty_cycle = 65536 // 2  # On 50%
            time.sleep(0.25)  # On for 1/4 second
            piezo.duty_cycle = 0  # Off
            time.sleep(0.05)  # Pause between notes
        if temp != False:
            break
        time.sleep(0.5)

# fortnite
def song6():

    timeout = time.time() + 10 
    while True:
        
        if time.time() > timeout:
            break

        delay = [149, 149, 149, 446, 1485, 149, 149, 149, 446, 297, 297, 149, 595, 149, 149, 149, 149, 1931]
        duration = [149, 149, 149, 446, 297, 149, 149, 149, 446, 297, 297, 149, 149, 149, 149, 149, 149, 149]
        freq = [349, 415, 466, 466, 415, 349, 415, 466, 466, 415, 349, 311, 349, 466, 415, 349, 311, 349]
        for f in range(0, len(freq)):
            if interrupt():
                temp = True
                break
            piezo.frequency = freq[f]
            piezo.duty_cycle = 65536 // 2  # On 50%
            time.sleep(duration[f] / 1000)  # On
            piezo.duty_cycle = 0  # Off
            time.sleep(delay[f] / 1000)  # Pause between notes
        if temp != False:
            break
        time.sleep(0.5)
        

#------------------------------------------------------------------------------------------------------#
# 
# display code  
#    
#------------------------------------------------------------------------------------------------------# 


def reset():
    displayio.release_displays()
    spi = board.SPI()
    tft_cs = board.D5
    tft_dc = board.D9
    display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=board.D7)
    global display
    display = ST7735R(display_bus, width=128, height=128, colstart=2, rowstart=1)
    global splash
    splash = displayio.Group(max_size=100)
    display.show(splash)
    color_bitmap = displayio.Bitmap(128, 128, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF # White
    bg_white = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_white)
    
def ShowPic(string, timein):
    with open(string, "rb") as bitmap_file:
        # Setup the file as the bitmap data source
        bitmap = displayio.OnDiskBitmap(bitmap_file)
        # Create a TileGrid to hold the bitmap
        tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())
        # Create a Group to hold the TileGrid
        group = displayio.Group()
        # Add the TileGrid to the Group
        group.append(tile_grid)
        # Add the Group to the Display
        display.show(group)
        # Loop forever so you can enjoy your image
        for i in range(timein):
            pass
            time.sleep(1)        

def textshow(textin, bgcolor, xc, yc, timein):
    text_area = label.Label(terminalio.FONT, text=textin, color=bgcolor)
    text_area.x = xc
    text_area.y = yc
    splash.append(text_area)
    for i in range(timein):
        pass
        time.sleep(1)

def textout(textin, bgcolor, xc, yc):
    text_area = label.Label(terminalio.FONT, text=textin, color=bgcolor)
    text_area.x = xc
    text_area.y = yc
    splash.append(text_area)


#------------------------------------------------------------------------------------------------------#
# 
# rgb module code
#  
#------------------------------------------------------------------------------------------------------#    

# reverse logic on the rgb pins so that a pull up resistor turns the led off and the pull down turns it on
red = digitalio.DigitalInOut(board.D2)
red.direction = digitalio.Direction.INPUT
red.pull = digitalio.Pull.DOWN

green = digitalio.DigitalInOut(board.D1)
green.direction = digitalio.Direction.INPUT
green.pull = digitalio.Pull.DOWN

blue = digitalio.DigitalInOut(board.D0)
blue.direction = digitalio.Direction.INPUT
blue.pull = digitalio.Pull.DOWN

# dictRed = {"red": 0xFF, 'orange': 0xFF, "yellow": 0xFF, "green": 0, 'blue': 0, 'purple': 0xFF, 'white': 0xFF}
# dictGreen = {"red": 0, 'orange': 0xA5, "yellow": 0xFF, "green": 0xFF, 'blue': 0, 'purple': 0, 'white': 0xFF}
# dictBlue = {"red": 0, 'orange': 0, "yellow": 0, "green": 0, 'blue': 0xFF, 'purple': 0xFF, 'white': 0xFF}

# set of basic digital colour values to be set on demand in 3 dictionaries, one for each pin
dictRed = {  "red": digitalio.Pull.UP, 'cyan': digitalio.Pull.DOWN,   "yellow": digitalio.Pull.UP, "green": digitalio.Pull.DOWN,   'blue': digitalio.Pull.DOWN,   'magenta': digitalio.Pull.UP, 'white': digitalio.Pull.UP, 'off': digitalio.Pull.DOWN}
dictGreen = {"red": digitalio.Pull.DOWN,   'cyan': digitalio.Pull.UP, "yellow": digitalio.Pull.UP, "green": digitalio.Pull.UP, 'blue': digitalio.Pull.DOWN,   'magenta': digitalio.Pull.DOWN,   'white': digitalio.Pull.UP, 'off': digitalio.Pull.DOWN}
dictBlue = { "red": digitalio.Pull.DOWN,   'cyan': digitalio.Pull.UP, "yellow": digitalio.Pull.DOWN,   "green": digitalio.Pull.DOWN,   'blue': digitalio.Pull.UP, 'magenta': digitalio.Pull.UP, 'white': digitalio.Pull.UP, 'off': digitalio.Pull.DOWN}

# changes the led color to one defined in the dictionary
def setColor(color):
    red.pull = dictRed[color]
    green.pull = dictGreen[color]
    blue.pull = dictBlue[color]

#------------------------------------------------------------------------------------------------------#
# 
# gui code
#     
#------------------------------------------------------------------------------------------------------#    

# setting up the states of the GUI
LOADING = 0
PASSCODE = 1
HOME = 2
DANCE = 3
MUSIC = 4
ABOUT = 5
EXIT = 6
REQUEST = 7
DEFAULT = 8

# initial default state is loading
state = LOADING

while True:

    # if state is loading, it goes to passcode
    if state ==  LOADING:
        splash = displayio.Group(max_size=100)
        reset()
        #time.sleep(1)
        #reset()
        #textshow("Welcome", 0x000000, 45, 64, 0.1)
        #reset()
        string1 = "Loading"
        textshow(string1, 0x000000, 30, 64, 0.0001)
        string2 = "..."
        i = 0
        x = 72
        while(i<3):
            textshow(string2[i], 0x000000, x, 64, 0.0001)
            i+=1
            x+=6
        ShowPic("\Robot.bmp", 3)
        time.sleep(2)
        reset()
        textshow("Welcome", 0x000000, 45, 64, 0.1)
        reset()
        state =  PASSCODE

    # if state is passcode, checks the passcode, if correct goes to home, else back to passcode
    if state ==  PASSCODE:
        textout("enter the passcode", 0x000000, 10, 60)
        boolean = False
        boolean = checkPass()
        if boolean:
            boolean = False
            state =  HOME
            reset()
        else:
            reset()
            textshow("wrong passcode", 0x000000, 10, 60, 2)
            #time.sleep(1)
            state = PASSCODE
            reset()

    # if state is home, checks keypad and goes to coressponding state     
    elif state ==  HOME:
        setColor('off')
        textout("Press a key: \n 1) Default \n 2) Dance \n 3) Music \n 4) About \n 5) Exit ", 0x000000, 10, 60)
        keys = 0
        while keys == 0:
            keys = keypadDecode()

        if keys == 1:
            state = DEFAULT
            reset()
        elif keys == 2:
            state =  DANCE
            reset()
        elif keys == 3:
            state =  MUSIC
            reset()
        elif keys == 4:
            state =  ABOUT
            reset()
        elif keys == 5:
            state =  EXIT
            reset()
        else:
            state =  HOME
            reset()

    # if state is dance, plays the dance move coressponding to the keypad number pressed    
    elif state ==  DANCE:
        textout("Press a key: \n 1) Shuffle \n 2) Kick \n 3) Moonwalk \n 4) Wobble \n 5) Squat \n 6) Spin", 0x000000, 10, 60)
        keys = 0
        while keys == 0:
            keys = keypadDecode()

        if keys == 1:
            reset()
            textout("Shuffling", 0x000000, 37, 64)
            setColor('green')
            dance1()
            setColor('off')
            state =  REQUEST
            reset()
        elif keys == 2:
            reset()
            textout("Kick", 0x000000, 37, 64)
            setColor('green')
            dance2()
            setColor('off')
            state =  REQUEST
            reset()
        elif keys == 3:
            reset()
            textout("Moonwalk", 0x000000, 45, 64)
            setColor('green')
            dance3()
            setColor('off')
            textout("Moonwalk", 0x000000, 45, 64)
            state =  REQUEST
            reset()
        elif keys == 4:
            reset()
            textout("Squat", 0x000000, 45, 64)
            setColor('green')
            dance4()
            setColor('off')
            state =  REQUEST
            reset()
        elif keys == 5:
            reset()
            textout("Wobble", 0x000000, 45, 64)
            setColor('green')
            dance5()
            setColor('off')
            state =  REQUEST
            reset()
        elif keys == 6:
            reset()
            textout("Spin", 0x000000, 45, 64)
            setColor('green')
            dance6()
            setColor('off')
            state =  REQUEST
            reset()
        else:
            state =  DANCE

    # if state is about it displays info about robot and returns
    elif state ==  ABOUT:
        textshow("About: \n Dancing Robot GUI", 0x000000, 10, 24, 5)
        textshow("press any button \n to return", 0x000000, 20, 64, 5)
       
        keys =0
        while keys == 0:
            keys = keypadDecode()

        if keys == 1:
            state =  HOME
            reset()
            
        elif keys == 2:
            state =  HOME
            reset()

        elif keys == 3:
            state =  HOME
            reset()

        elif keys == 4:
            state =  HOME
            reset()
   
        elif keys == 5:
            state =  HOME
            reset()

        elif keys == 6:
            state =  HOME
            reset()
            
        else:
            state = ABOUT
            reset()
        
    
    # if state is exit it quits the program
    elif state ==  EXIT:
        textshow("Exiting.....", 0x000000, 30, 64, 3)
        time.sleep(0.5)
        #state =  PASSCODE
        sys.exit()
        #reset()

    # if the state is request it goes to corresponding state according to keypad number pressed
    elif state ==  REQUEST:
        textout("Press a key: \n 1) Dance  \n 2) Play Music \n 3) Home", 0x000000, 15, 60)
        
        keys = 0
        while keys == 0:
            keys = keypadDecode()

        if keys == 1:
            state =  DANCE
            reset()
        elif keys == 2:
            state =  MUSIC
            reset()
        elif keys == 3:
            state =  HOME
            reset()
        else:
            state =  REQUEST

    # if state is music it goes to the song according to the keypad pressed
    elif state ==  MUSIC:
        textout("Press a key: \n 1) Anthem \n 2) Mario \n 3) Crimson \n 4) Canon \n 5) Tetris \n 6) Fortnite", 0x000000, 10, 60)

        keys = 0
        while keys == 0:
            keys = keypadDecode()

        if keys == 1:
            reset()
            setColor('cyan')
            textout("Playing Anthem", 0x000000, 20, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            song1()
            setColor('off')
            state =  REQUEST
            reset()
        elif keys == 2:
            reset()
            setColor('cyan')
            textout("Playing Mario", 0x000000, 20, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            song2()
            setColor('off')
            state =  REQUEST
            reset()
        elif keys == 3:
            reset()
            setColor('cyan')
            textout("Playing Crimson", 0x000000, 20, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            song3()
            setColor('off')
            state =  REQUEST
            reset()
        elif keys == 4:
            reset()
            setColor('cyan')
            textout("Playing Canon", 0x000000, 20, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            song4()
            setColor('off')
            state =  REQUEST
            reset()
        elif keys == 5:
            reset()
            setColor('cyan')
            textout("Playing Tetris", 0x000000, 20, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            song5()
            setColor('off')
            state =  REQUEST
            reset()
        elif keys == 6:
            reset()
            setColor('cyan')
            textout("Playing Fornite", 0x000000, 20, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            song6()
            setColor('off')
            state =  REQUEST
            reset()
        else:
            state =  MUSIC
    
    # default state required for the project.
    elif state == DEFAULT:
        # display not set but can be change only after each song
        setColor('green')
        dance1()
        setColor('cyan')
        dance2()
        setColor('blue')
        dance3()
        setColor('purple')
        dance4()
        setColor('red')
        dance5()
        setColor('yellow')
        dance6()
        setColor('white')
        state = HOME