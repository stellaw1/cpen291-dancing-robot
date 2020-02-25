# ------------------------------------------------------------------------------------------------------#
# Authors: Manek, Sanjeev, Parsa, Amir, Stella, Arnold, Rain
#
# Function: Dancing Robot
# 
# Date: 10/02/2020    
# ------------------------------------------------------------------------------------------------------#

# import all the libraries that we need
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

# ------------------------------------------------------------------------------------------------------#
#
# Sonar code
#
# ------------------------------------------------------------------------------------------------------#
# initialize sonar with adafruit_hcsr04 library
# trigger pin at D4 and echo pin at D3 
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D4, echo_pin=board.D3)


# define the checkSonar functions that takes in threshold value
# funciton returns true if distance detected by sonar is less than threshold
def checkSonar(threshold):
    try:
        distance = sonar.distance
        return distance < threshold
    except RuntimeError:
        return False


# ------------------------------------------------------------------------------------------------------#
#
# Keypad code
#
# ------------------------------------------------------------------------------------------------------#
# setting up rows and cols of keypad output to its corresponding pins on the itsybitsy
# board A4 to keypad row 0 (1, 2, 3)
row0 = digitalio.DigitalInOut(board.A4)
row0.direction = digitalio.Direction.INPUT
row0.pull = digitalio.Pull.UP

# board A5 to keypad row 1 (4, 5, 6)
row1 = digitalio.DigitalInOut(board.A5)
row1.direction = digitalio.Direction.INPUT
row1.pull = digitalio.Pull.UP

# board A2 to keypad output 1 (2:3 decoder)
out1 = digitalio.DigitalInOut(board.A2)
out1.direction = digitalio.Direction.OUTPUT
out1.value = False

# board A2 to keypad output 2 (2:3 decoder)
out2 = digitalio.DigitalInOut(board.A3)
out2.direction = digitalio.Direction.OUTPUT
out2.value = False

# create a 2D array representing the keys
keys = ((1, 2, 3),
        (4, 5, 6))


# define keypadDecode function that iterates through the different combination of output 1,2
# function returns the key pressed (1 - 6), if no key is pressed, function returns 0
def keypadDecode():
    key = 0
    for i in range(1, 4):
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


# define helper function to help decode which row the key pressed is at
# function takes column number as parameter and returns the key pressed, returns 0 if no key is pressed 
def keypadHelper(col):
    if not row0.value:
        return col
    if not row1.value:
        return col + 3
    return 0


# define checkPass function to read the input from the keypad
# blocks indefinitely until a password is entered, returns true if password entered is matched, false otherwise
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


# define the interrupt function that checks both the keypad for user input and sonar for distance
# function returns true and flashes RBG red 3 times if any key is pressed or the distance detected by sonar is less than 5cm
# otherwise, function returns false
def interrupt():
    keys = 0
    keys = keypadDecode()
    if keys != 0 or checkSonar(5):
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


# ------------------------------------------------------------------------------------------------------#
#
# dance code
#
# ------------------------------------------------------------------------------------------------------#
# piezo buzzer setup
piezo = pulseio.PWMOut(board.A1, duty_cycle=0, frequency=440, variable_frequency=True)

# servo setup
pwm1 = pulseio.PWMOut(board.D10, frequency=50)
legL = servo.Servo(pwm1)

pwm2 = pulseio.PWMOut(board.D11, frequency=50)
legR = servo.Servo(pwm2)

pwm3 = pulseio.PWMOut(board.D12, frequency=50)
footR = servo.Servo(pwm3)

pwm4 = pulseio.PWMOut(board.D13, frequency=50)
footL = servo.Servo(pwm4)

music = 1

###################################
# frequency lists for the six songs

ANTHEM = [392, 523, 392, 440, 494, 330, 330,
          440, 392, 349, 392, 262, 262,
          294, 294, 330, 349, 349, 392, 440, 494, 523, 587,
          659, 587, 523, 587, 494, 392,
          523, 494, 440, 494, 330, 330,
          440, 392, 349, 392, 262, 262,
          523, 494, 440, 392, 494, 523, 587,
          659, 587, 523, 494, 523, 587, 392, 392, 494, 523, 587,
          523, 494, 440, 392, 440, 494, 330, 330, 392, 440, 494,
          523, 440, 494, 523, 440, 494, 523, 440, 523, 698,
          698, 659, 587, 523, 587, 659, 523, 523,
          587, 523, 494, 440, 494, 523, 440, 440,
          523, 494, 440, 392, 262, 392, 440, 494, 523]

MARIO = [659, 659, 659, 523, 659, 784, 392, 523, 392, 330, 440, 494, 466, 440, 392, 659, 784, 880, 698, 784, 659,
         523, 587, 494, 523, 392, 330, 440, 494, 466, 440, 392, 659, 784, 880, 698, 784, 659, 523, 587, 494]

STRANGER = [131, 165, 196, 247, 262, 247, 196, 165]

ALLSTAR = [466, 369, 369, 311, 369, 369, 369, 311, 369, 369, 369, 466, 466, 369, 369, 311, 369, 369, 369, 311,
         369, 369, 369, 466, 369, 466, 554, 494, 554, 622, 740, 831, 740, 369, 369, 415, 369, 466, 415, 415,
         369, 415, 311]

TETRIS = [659, 494, 523, 587, 659, 587, 523, 494, 440, 440, 523, 659, 587, 523, 494, 494, 494, 523, 587, 523,
          494, 494, 494, 523, 587, 659, 523, 440, 440, 587, 587, 698, 880, 784, 698, 659, 659, 523, 659, 587,
          523, 494, 494, 523, 587, 659, 523, 440, 440, 659, 494, 523, 587, 659, 587, 523, 494, 440, 440, 523,
          659, 587, 523, 494, 494, 523, 587, 659, 523, 440, 440, 587, 587, 698, 880, 784, 698, 659, 659, 523,
          659, 587, 523, 587, 659, 523, 440, 440]

FNITE = [349, 415, 466, 466, 415, 349, 415, 466, 466, 415, 349, 311, 349, 466, 415, 349, 311, 349]


def playSong(song, delay):
    for i in range(len(song)):
        piezo.frequency = song[i]
        piezo.duty_cycle = 65536 // 2  # On 50%
        time.sleep(delay)  # On
    piezo.duty_cycle = 0 # Off

def buzzer_off():
    piezo.duty_cycle = 0 # Off


def buzzer_on():
    piezo.duty_cycle = 65536 // 2  # On 50%

def playNote(freq, delay):
    piezo.frequency = freq
    piezo.duty_cycle = 65536 // 2  # On 50%
    time.sleep(delay)  # On


############################
# basic dance move functions

def rotate(limb, min, max, step, start, song):
    i = start
    for x in range(min, max + step, step):
        limb.angle = x
        if music == 1:
            playNote(song[i % len(song)], 0.3)
        else:
            time.sleep(0.3)
        i += 1
    return i


def double_rotate(limb1, limb2, min, max, step, start, song):
    print(song)
    i = start
    for x in range(min, max + step, step):
        limb1.angle = x
        limb2.angle = x
        playNote(song[i % len(song)], 0.3)
        i += 1
    return i

def tapFoot(start, song, limb):
    if limb == footL:
        start = rotate(footL, 90, 60, -10, start, song)
        start = rotate(footL, 60, 90, 10, start, song)
    else:
        start = rotate(footR, 100, 130, 10, start, song)
        start = rotate(footR, 130, 100, -10, start, song)
    return start

def kick(start, song, limb):
    if limb == legR:
        limb.angle = 160
        start = rotate(footR, 100, 60, -10, start, song)
        start = rotate(footR, 60, 100, 10, start, song)
        limb.angle = 90
    else:
        limb.angle = 20
        start = rotate(footL, 90, 130, 10, start, song)
        start = rotate(footL, 130, 90, -10, start, song)
        limb.angle = 90
    return start

def footIn(start, song, limb):
    if limb == legR:
        start = rotate(limb, 90, 10, -10, start, song)
        start = rotate(limb, 10, 90, 10, start, song)
    else:
        start = rotate(limb, 90, 170, 10, start, song)
        start = rotate(limb, 170, 90, -10, start, song)
    return start

def footOut(start, song, limb):
    if limb == legR:
        start = rotate(limb, 90, 160, 10, start, song)
        start = rotate(limb, 160, 90, -10, start, song)
    else:
        start = rotate(legL, 90, 20, -10, start, song)
        start = rotate(legL, 20, 90, 10, start, song)
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
    for angle in range(30, 90, 15):  # 180 - 0 degrees, 5 degrees at a time.
        start = double_rotate(legL, legR, angle, angle, 15, start, song)
    for angle in range(90, 120, 15):  # 0 - 180 degrees, 5 degrees at a time.
        start = double_rotate(legL, legR, angle, angle, -15, start, song)
    for angle in range(120, 90, -15):  # 180 - 0 degrees, 5 degrees at a time.
        start = double_rotate(legL, legR, angle, angle, 15, start, song)
    return start


def reset_servo():
    footR.angle = 97
    time.sleep(0.1)
    footL.angle = 92
    time.sleep(0.1)
    legR.angle = 90
    time.sleep(0.1)
    legL.angle = 90
    time.sleep(0.1)


###################################################################
# 6 dance moves created as a combination of the smaller moves above

def dance1():
    reset_servo()
    if music:
        buzzer_on()
    start = 0
    for i in range(3):
        start = wiggle(start, STRANGER)
    buzzer_off()
    reset_servo()


def dance2():
    reset_servo()
    if music:
        buzzer_on()
    start = 0
    for i in range(2):
        start = footOut(start, MARIO, legL)
        start = footIn(start, MARIO, legL)
        start = footOut(start, MARIO, legR)
        start = footIn(start, MARIO, legR)
    buzzer_off()
    reset_servo()


def dance3():
    reset_servo()
    if music:
        buzzer_on()
    start = 0
    for i in range(2):
        start = footOut(start, ANTHEM, legL)
        start = tapFoot(start, ANTHEM, footL)
        start = kick(start, ANTHEM, legL)

        start = footOut(start, ANTHEM, legR)
        start = tapFoot(start, ANTHEM, footR)
        start = kick(start, ANTHEM, legR)
    buzzer_off()
    reset_servo()



def dance4():
    reset_servo()
    if music:
        buzzer_on()
    start = 0
    for j in range(3):
        start = tapFoot(start, TETRIS, footL)
    for j in range(3):
        start = tapFoot(start, TETRIS, footR)
    buzzer_off()
    reset_servo()


def dance5():
    reset_servo()
    if music:
        buzzer_on()
    start = 0
    for i in range(3):
        start = kick(start, ALLSTAR, legL)
        start = kick(start, ALLSTAR, legR)
    buzzer_off()
    reset_servo()


def dance6():
    reset_servo()
    if music:
        buzzer_on()
    start = 0
    for i in range(3):
        start = shuffle(start, FNITE)
    buzzer_off()
    reset_servo()





# ------------------------------------------------------------------------------------------------------#
#
# songs code
#
# ------------------------------------------------------------------------------------------------------#


# define 6 songs

# USSR anthem
def song1():
    timeout = time.time() + 10
    while True:

        if time.time() > timeout:
            break

        temp = False

        for f in (392, 523, 392, 440, 494, 330, 330,
                  440, 392, 349, 392, 262, 262,
                  294, 294, 330, 349, 349, 392, 440, 494, 523, 587,
                  659, 587, 523, 587, 494, 392,
                  523, 494, 440, 494, 330, 330,
                  440, 392, 349, 392, 262, 262,
                  523, 494, 440, 392, 494, 523, 587,
                  659, 587, 523, 494, 523, 587, 392, 392, 494, 523, 587,
                  523, 494, 440, 392, 440, 494, 330, 330, 392, 440, 494,
                  523, 440, 494, 523, 440, 494, 523, 440, 523, 698,
                  698, 659, 587, 523, 587, 659, 523, 523,
                  587, 523, 494, 440, 494, 523, 440, 440,
                  523, 494, 440, 392, 262, 392, 440, 494, 523):
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

        temp = False

        for f in (
        330, 330, 330, 262, 330, 392, 196, 262, 196, 165, 220, 247, 233, 220, 196, 330, 392, 440, 349, 392, 330,
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

        temp = False

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

        temp = False

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

        temp = False

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

        temp = False

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


# ------------------------------------------------------------------------------------------------------#
#
# display code
#
# ------------------------------------------------------------------------------------------------------#

# define reset function that resets the display when we want to change the state of the FSM
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
    color_palette[0] = 0xFFFFFF  # White
    bg_white = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_white)


# method to upload picture onto the LCD
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
            time.sleep(0.1)

        # define textshow function that shows time dependent text (shows for 'timein' seconds)


def textshow(textin, bgcolor, xc, yc, timein):
    text_area = label.Label(terminalio.FONT, text=textin, color=bgcolor)
    text_area.x = xc
    text_area.y = yc
    splash.append(text_area)
    for i in range(timein):
        pass
        time.sleep(1)


# define textout function that shows time independent text
def textout(textin, bgcolor, xc, yc):
    text_area = label.Label(terminalio.FONT, text=textin, color=bgcolor)
    text_area.x = xc
    text_area.y = yc
    splash.append(text_area)


# ------------------------------------------------------------------------------------------------------#
#
# rgb module code
#
# ------------------------------------------------------------------------------------------------------#

# reverse logic on the rgb pins so that a pull up resistor turns the led off and the pull down turns it on
# board D2 to red color
red = digitalio.DigitalInOut(board.D2)
red.direction = digitalio.Direction.INPUT
red.pull = digitalio.Pull.DOWN

# board D1 to green color
green = digitalio.DigitalInOut(board.D1)
green.direction = digitalio.Direction.INPUT
green.pull = digitalio.Pull.DOWN

# board D0 to blue color
blue = digitalio.DigitalInOut(board.D0)
blue.direction = digitalio.Direction.INPUT
blue.pull = digitalio.Pull.DOWN

# set of basic digital colour values to be set on demand in 3 dictionaries, one for each pin
dictRed = {"red": digitalio.Pull.UP, 'cyan': digitalio.Pull.DOWN, "yellow": digitalio.Pull.UP,
           "green": digitalio.Pull.DOWN, 'blue': digitalio.Pull.DOWN, 'magenta': digitalio.Pull.UP,
           'white': digitalio.Pull.UP, 'off': digitalio.Pull.DOWN}
dictGreen = {"red": digitalio.Pull.DOWN, 'cyan': digitalio.Pull.UP, "yellow": digitalio.Pull.UP,
             "green": digitalio.Pull.UP, 'blue': digitalio.Pull.DOWN, 'magenta': digitalio.Pull.DOWN,
             'white': digitalio.Pull.UP, 'off': digitalio.Pull.DOWN}
dictBlue = {"red": digitalio.Pull.DOWN, 'cyan': digitalio.Pull.UP, "yellow": digitalio.Pull.DOWN,
            "green": digitalio.Pull.DOWN, 'blue': digitalio.Pull.UP, 'magenta': digitalio.Pull.UP,
            'white': digitalio.Pull.UP, 'off': digitalio.Pull.DOWN}


# define function setColor that takes an input string and changes the RBG to the specified color
# if the string color is defined in the dictionary declared above changes the led color to one defined in the dictionary
def setColor(color):
    red.pull = dictRed[color]
    green.pull = dictGreen[color]
    blue.pull = dictBlue[color]


def anim(time):
    for i in range(time):
        ShowPic("\dance-0.bmp", 0.1)
        ShowPic("\dance-1.bmp", 0.1)
        ShowPic("\dance-2.bmp", 0.1)
        ShowPic("\dance-3.bmp", 0.1)
        ShowPic("\dance-4.bmp", 0.1)
        ShowPic("\dance-5.bmp", 0.1)
        ShowPic("\dance-6.bmp", 0.1)
        ShowPic("\dance-7.bmp", 0.1)
        ShowPic("\dance-8.bmp", 0.1)
        ShowPic("\dance-9.bmp", 0.1)
        ShowPic("\dance-10.bmp", 0.1)
        ShowPic("\dance-11.bmp", 0.1)
        ShowPic("\dance-12.bmp", 0.1)
        ShowPic("\dance-13.bmp", 0.1)
        ShowPic("\dance-14.bmp", 0.1)
        ShowPic("\dance-15.bmp", 0.1)
        ShowPic("\dance-16.bmp", 0.1)
        ShowPic("\dance-17.bmp", 0.1)
        ShowPic("\dance-18.bmp", 0.1)
        ShowPic("\dance-19.bmp", 0.1)
        ShowPic("\dance-20.bmp", 0.1)


def animRev(time):
    for i in range(time):
        ShowPic("\dance-20.bmp", 0.1)
        ShowPic("\dance-19.bmp", 0.1)
        ShowPic("\dance-18.bmp", 0.1)
        ShowPic("\dance-17.bmp", 0.1)
        ShowPic("\dance-16.bmp", 0.1)
        ShowPic("\dance-15.bmp", 0.1)
        ShowPic("\dance-14.bmp", 0.1)
        ShowPic("\dance-13.bmp", 0.1)
        ShowPic("\dance-12.bmp", 0.1)
        ShowPic("\dance-11.bmp", 0.1)
        ShowPic("\dance-10.bmp", 0.1)
        ShowPic("\dance-9.bmp", 0.1)
        ShowPic("\dance-8.bmp", 0.1)
        ShowPic("\dance-7.bmp", 0.1)
        ShowPic("\dance-6.bmp", 0.1)
        ShowPic("\dance-5.bmp", 0.1)
        ShowPic("\dance-4.bmp", 0.1)
        ShowPic("\dance-3.bmp", 0.1)
        ShowPic("\dance-2.bmp", 0.1)
        ShowPic("\dance-1.bmp", 0.1)
        ShowPic("\dance-0.bmp", 0.1)


# ------------------------------------------------------------------------------------------------------#
#
# gui code
#
# ------------------------------------------------------------------------------------------------------#

# define the states of the GUI
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

# keeps checking the FSM state and update the current state according to the inputs
while True:
    # if state is loading, it goes to passcode
    if state == LOADING:
        splash = displayio.Group(max_size=100)
        reset()
        ShowPic("\Robot.bmp", 2)
        # display "Loading..." meassage on the LCD
        string1 = "Loading"
        textshow(string1, 0x000000, 30, 64, 0.0001)
        string2 = "..."
        i = 0
        x = 72
        while (i < 3):
            textshow(string2[i], 0x000000, x, 64, 0.0001)
            i += 1
            x += 6
        # display the robot picture on the LCD

        time.sleep(2)
        reset()
        # display the "Welcome" text on the LCD
        textshow("Welcome", 0x000000, 45, 64, 0.1)
        reset()
        # proceed to passcode state for the FSM to request for passcode
        state = PASSCODE

    # if state is passcode, checks the passcode, if correct goes to home, else back to passcode
    if state == PASSCODE:
        # display "enter the passcode", runs checkPass function
        textout("enter the passcode", 0x000000, 10, 60)
        boolean = False
        boolean = checkPass()
        # if passcode is correct the FSM proceed to the home state
        if boolean:
            boolean = False
            state = HOME
            reset()
        # if passcode is incorrect display "wrong passcode" and then keeps fetching passcode
        else:
            reset()
            textshow("wrong passcode", 0x000000, 10, 60, 2)
            # time.sleep(1)
            state = PASSCODE
            reset()

    # if state is home, checks keypad and goes to coressponding state
    elif state == HOME:
        setColor('off')
        # display the home menu on the screen
        textout("Press a key: \n 1) Default \n 2) Dance \n 3) Music \n 4) About \n 5) Exit ", 0x000000, 10, 60)
        keys = 0
        # keeps checking the keypad for a input, blocks indefinitely until user inputs
        while keys == 0:
            keys = keypadDecode()

        # set the next state of the FSM according to the user input
        if keys == 1:
            state = DEFAULT
            reset()
        elif keys == 2:
            state = DANCE
            reset()
        elif keys == 3:
            state = MUSIC
            reset()
        elif keys == 4:
            state = ABOUT
            reset()
        elif keys == 5:
            state = EXIT
            reset()
        else:
            state = HOME
            reset()

    # if state is dance, plays the dance move coressponding to the keypad number pressed
    elif state == DANCE:
        # display the dance menu on the screen
        textout("Press a key: \n 1) Walk \n 2) Shuffle \n 3) Ballerina \n 4) Pigeon \n 5) Excite \n 6) Karate",
                0x000000, 10, 60)
        keys = 0
        # keeps checking the keypad for a input,
        # blocks indefinitely until user inputs or until sonar detects an object less than 5cm
        while keys == 0 and not checkSonar(5):
            keys = keypadDecode()

        # call the corresponding dance function depending on user input then move the FSM to request state
        # if no user input, check sonar for distance less than 5, if such, return FSM to home state.
        if keys == 1:
            reset()
            textout("Walking", 0x000000, 43, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            setColor('green')
            time.sleep(2)
            reset()
            anim(1)
            dance1()
            animRev(1)
            setColor('off')
            state = REQUEST
            reset()
        elif keys == 2:
            reset()
            textout("Shuffling", 0x000000, 43, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            setColor('green')
            time.sleep(2)
            reset()
            anim(1)
            dance2()
            animRev(1)
            setColor('off')
            state = REQUEST
            reset()
        elif keys == 3:
            reset()
            textout("Ballerina", 0x000000, 43, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            setColor('green')
            time.sleep(2)
            reset()
            anim(1)
            dance3()
            animRev(1)
            setColor('off')
            state = REQUEST
            reset()
        elif keys == 4:
            reset()
            textout("Pigeon", 0x000000, 45, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            setColor('green')
            time.sleep(2)
            reset()
            anim(1)
            dance4()
            animRev(1)
            setColor('off')
            state = REQUEST
            reset()
        elif keys == 5:
            reset()
            textout("Excite", 0x000000, 45, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            setColor('green')
            time.sleep(2)
            reset()
            anim(1)
            dance5()
            animRev(1)
            setColor('off')
            state = REQUEST
            reset()
        elif keys == 6:
            reset()
            textout("Karate", 0x000000, 45, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            setColor('green')
            time.sleep(2)
            reset()
            anim(1)
            dance6()
            animRev(1)
            setColor('off')
            state = REQUEST
            reset()
        elif checkSonar(5):
            setColor('red')
            time.sleep(0.1)
            state = HOME
            setColor('off')
            reset()
        # if no user input / sonar detection, stay in dance state
        else:
            state = DANCE

    # if state is about it displays info about robot and returns
    elif state == ABOUT:
        textshow("About: \n Dancing Robot GUI", 0x000000, 10, 24, 5)
        textshow("press any button \n to return", 0x000000, 20, 64, 5)

        keys = 0
        # keeps checking the keypad for a input,
        # blocks indefinitely until user inputs or until sonar detects an object less than 5cm
        while keys == 0 and not checkSonar(5):
            keys = keypadDecode()

        temp = False

        while True:
            distance = sonar.distance
            reset()
            textout(str(distance), 0x000000, 50, 50)
            if interrupt():
                temp = True
                break

        if keys == 1:
            state = HOME
            reset()

        elif keys == 2:
            state = HOME
            reset()

        elif keys == 3:
            state = HOME
            reset()

        elif keys == 4:
            state = HOME
            reset()

        elif keys == 5:
            state = HOME
            reset()

        elif keys == 6:
            state = HOME
            reset()

        elif checkSonar(5):
            setColor('red')
            time.sleep(0.1)
            state = DANCE
            setColor('off')
            reset()

        else:
            state = ABOUT
            reset()


    # if state is exit it quits the program
    elif state == EXIT:
        textshow("Exiting.....", 0x000000, 30, 64, 3)
        time.sleep(0.5)
        # state =  PASSCODE
        sys.exit()
        # reset()

    # if the state is request it goes to corresponding state according to keypad number pressed
    elif state == REQUEST:
        textout("Press a key: \n 1) Dance  \n 2) Play Music \n 3) Home", 0x000000, 15, 60)

        keys = 0
        while keys == 0:
            keys = keypadDecode()

        if keys == 1:
            state = DANCE
            reset()
        elif keys == 2:
            state = MUSIC
            reset()
        elif keys == 3:
            state = HOME
            reset()
        else:
            state = REQUEST

    # if state is music it goes to the song according to the keypad pressed
    elif state == MUSIC:
        textout("Press a key: \n 1) Anthem \n 2) Mario \n 3) Crimson \n 4) Canon \n 5) Tetris \n 6) Fortnite", 0x000000,
                10, 60)

        keys = 0
        while keys == 0 and not checkSonar(5):
            keys = keypadDecode()

        if keys == 1:
            reset()
            setColor('cyan')
            textout("Playing Anthem", 0x000000, 20, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            song1()
            setColor('off')
            state = REQUEST
            reset()
        elif keys == 2:
            reset()
            setColor('cyan')
            textout("Playing Mario", 0x000000, 20, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            song2()
            setColor('off')
            state = REQUEST
            reset()
        elif keys == 3:
            reset()
            setColor('cyan')
            textout("Playing Crimson", 0x000000, 20, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            song3()
            setColor('off')
            state = REQUEST
            reset()
        elif keys == 4:
            reset()
            setColor('cyan')
            textout("Playing Canon", 0x000000, 20, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            song4()
            setColor('off')
            state = REQUEST
            reset()
        elif keys == 5:
            reset()
            setColor('cyan')
            textout("Playing Tetris", 0x000000, 20, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            song5()
            setColor('off')
            state = REQUEST
            reset()
        elif keys == 6:
            reset()
            setColor('cyan')
            textout("Playing Fornite", 0x000000, 20, 48)
            textout("Press any Button", 0x000000, 17, 64)
            textout("to return", 0x000000, 35, 80)
            song6()
            setColor('off')
            state = REQUEST
            reset()
        elif checkSonar(5):
            setColor('red')
            time.sleep(0.1)
            state = HOME
            setColor('off')
            reset()
        else:
            state = MUSIC

    # default state required for the project.
    elif state == DEFAULT:
        # display not set but can be change only after each song
        music = 0
        time.sleep(2)
        reset()
        textout("Default Mode", 0x000000, 27, 48)
        setColor('green')
        time.sleep(2)
        anim(2)
        dance1()
        setColor('cyan')
        dance2()
        setColor('blue')
        dance3()
        setColor('magenta')
        dance4()
        setColor('red')
        dance5()
        setColor('yellow')
        dance6()
        setColor('white')
        reset()
        animRev(2)
        music = 1
        state = HOME