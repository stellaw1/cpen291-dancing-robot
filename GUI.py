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

#------------------------------------------------------------------------------------------------------#
#
# songs code 
#     
#------------------------------------------------------------------------------------------------------#    

# setting up the piezo buzzer
piezo = pulseio.PWMOut(board.A1 , duty_cycle=0, frequency=440, variable_frequency=True)

# define 6 songs

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

def song3():

    timeout = time.time() + 30 
    while True:
        
        if time.time() > timeout:
            break

        for f in (196, 247, 294, 370, 392, 370, 294, 247, 196, 262, 294, 392, 294): #enter the song frequency here):
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

        for f in (131, 165, 196, 262, 98, 123, 147, 196, 110, 131, 165, 220, 82, 98, 123, 165, 87, 110, 131, 175, 
                131, 165, 196, 262, 87, 110, 131, 175, 98, 123, 147, 196, 110): #enter the song frequency here):
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

        for f in (659, 494, 523, 587, 659, 587, 523, 494, 440, 440, 523, 659, 587, 523, 494, 494, 494, 523, 587, 523,
                494, 494, 494, 523, 587, 659, 523, 440, 440, 587, 587, 698, 880, 784, 698, 659, 659, 523, 659, 587, 
                523, 494, 494, 523, 587, 659, 523, 440, 440, 659, 494, 523, 587, 659, 587, 523, 494, 440, 440, 523, 
                659, 587, 523, 494, 494, 523, 587, 659, 523, 440, 440, 587, 587, 698, 880, 784, 698, 659, 659, 523,
                659, 587, 523, 587, 659, 523, 440, 440): #enter the song frequency here):
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

        for f in (149, 149, 149, 446, 1485, 149, 149, 149, 446, 297, 297, 149, 595, 149, 149, 149, 149, 1931): #enter the song frequency here):
            piezo.frequency = f
            piezo.duty_cycle = 65536 // 2  # On 50%
            time.sleep(0.25)  # On for 1/4 second
            piezo.duty_cycle = 0  # Off
            time.sleep(0.05)  # Pause between notes
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
    display = ST7735R(display_bus, width=128, height=128, colstart=2, rowstart=1)
    global splash
    display.show(splash)
    color_bitmap = displayio.Bitmap(128, 128, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFFFFFF # White
    bg_white = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_white)

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
    reset()
    for i in range(0, 12, 1):
        play_note(CRIMSON[i])
        wiggle()
    reset()


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
        string = "Loading..."
        i = 0
        x = 30
        while(i<10):
            textshow(string[i], 0x000000, x, 64, 0.0001)
            i+=1
            x+=6
        reset()
        textshow("Welcome", 0x000000, 30, 64, 0.1)
        reset()
        textshow("CPEN 291", 0x000000, 30, 64, 0.1)
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
        textout("Press a key: \n 1) Dance Menu \n 2) Music \n 3) Exit \n 4) About ", 0x000000, 10, 60)
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
            state =  EXIT
            reset()
        elif keys == 5:
            state =  ABOUT
            reset()
        else:
            state =  HOME
            reset()

    # if state is dance, plays the dance move coressponding to the keypad number pressed    
    elif state ==  DANCE:
        textout("Press a key: \n 1) Shuffle \n 2) Kick \n 3) Moonwalk \n 5) Wobble \n 5) Squat \n 6) Spin", 0x000000, 10, 60)
        keys = 0
        while keys == 0:
            keys = keypadDecode()

        if keys == 1:
            dance1()
            state =  REQUEST
            reset()
        elif keys == 2:
            dance2()
            state =  REQUEST
            reset()
        elif keys == 3:
            dance3()
            state =  REQUEST
            reset()
        elif keys == 4:
            dance4()
            state =  REQUEST
            reset()
        elif keys == 5:
            dance5()
            state =  REQUEST
            reset()
        elif keys == 6:
            dance6()
            state =  REQUEST
            reset()
        else:
            state =  DANCE

    # if state is about it displays info about robot and returns
    elif state ==  ABOUT:
        textshow("About: \n Dancing Robot GUI", 0x000000, 10, 10, 5)
        textshow("press any button to return", 0x000000, 10, 60, 5)
       
        keys =0
        while keys == 0:
            keys = keypadDecode()

        if keys == 1:
            state =  HOME
            reset()
            textshow("Created By: \n 1)Manek \n  2)Sanjeev \n 3)Parsa \n 4)Amir \n 5)Stella \n 6)Arnold \n 7)Rain", 0x000000, 10, 60, 1)
            time.sleep(1)
            reset()
        elif keys == 2:
            state =  HOME
            reset()
            textshow("Created By: \n 1)Manek \n  2)Sanjeev \n 3)Parsa \n 4)Amir \n 5)Stella \n 6)Arnold \n 7)Rain", 0x000000, 10, 60, 1)
            time.sleep(1)
            reset()
        elif keys == 3:
            state =  HOME
            reset()
            textshow("Created By: \n 1)Manek \n  2)Sanjeev \n 3)Parsa \n 4)Amir \n 5)Stella \n 6)Arnold \n 7)Rain", 0x000000, 10, 60, 1)
            time.sleep(1)
            reset()
        elif keys == 4:
            state =  HOME
            reset()
            textshow("Created By: \n 1)Manek \n  2)Sanjeev \n 3)Parsa \n 4)Amir \n 5)Stella \n 6)Arnold \n 7)Rain", 0x000000, 10, 60, 1)
            time.sleep(1)
            reset()
        elif keys == 5:
            state =  HOME
            reset()
            textshow("Created By: \n 1)Manek \n  2)Sanjeev \n 3)Parsa \n 4)Amir \n 5)Stella \n 6)Arnold \n 7)Rain", 0x000000, 10, 60, 1)
            time.sleep(1)
            reset()
        elif keys == 6:
            state =  HOME
            reset()
            textshow("Created By: \n 1)Manek \n  2)Sanjeev \n 3)Parsa \n 4)Amir \n 5)Stella \n 6)Arnold \n 7)Rain", 0x000000, 10, 60, 1)
            time.sleep(1)
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
        textout("Press a key: \n 1) Dance  \n 2) Play Music \n 3) Home", 0x000000, 10, 60)
        
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
        textout("Press a key: \n 1) song1 \n 2) song2 \n 3) song3 \n 5) song4 \n 5) song5 \n 6) song6", 0x000000, 10, 60)

        keys = 0
        while keys == 0:
            keys = keypadDecode()

        if keys == 1:
            song1()
            state =  REQUEST
            reset()
        elif keys == 2:
            song2()
            state =  REQUEST
            reset()
        elif keys == 3:
            song3()
            state =  REQUEST
            reset()
        elif keys == 4:
            song4()
            state =  REQUEST
            reset()
        elif keys == 5:
            song5()
            state =  REQUEST
            reset()
        elif keys == 6:
            song6()
            state =  REQUEST
            reset()
        else:
            state =  MUSIC
    
    # default state required for the project.
    elif state == DEFAULT:
        # display not set but can be change only after each song
        dance1()
        dance2()
        dance3()
        dance4()
        dance5()
        dance6()
        state = HOME