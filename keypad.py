# L2B - G11 MP1
# 
# Authors: 
# Sources: https://learn.adafruit.com/matrix-keypad?view=all

# import libraries
import time
import digitalio
import board
import adafruit_matrixkeypad

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
out1.value = False;

out2 = digitalio.DigitalInOut(board.D9)
out2.direction = digitalio.Direction.OUTPUT
out2.value = False;

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

col0 = (out1 && !out2)
col0 = (out2 && !out1)
col0 = (out1 && out2)

# Membrane 3x4 matrix keypad 
cols = [digitalio.DigitalInOut(x) for x in (col0, col1, col2)]
rows = [digitalio.DigitalInOut(x) for x in (board.A4, board.A5)]
 
# define key values using a tuple
keys = ((1, 2, 3),
        (4, 5, 6)#,
        # (7, 8, 9),
        # ('*', 0, '#')
        )
 
keypad = adafruit_matrixkeypad.Matrix_Keypad(rows, cols, keys)

def keypadDecode():
    time.sleep(.1)
    out1.value = True
    out2.value = False
    key = keypadHelper(1)
    if key != 0:
        return key
    time.sleep(.1)
    out1.value = False
    out2.value = True
    key = keypadHelper(2)
    if key != 0:
        return key
    time.sleep(.1)
    out1.value = True
    out2.value = True
    key = keypadHelper(3)
    return key

def keypadHelper(col):
    count = 0
    for x in (rows):
        if not x.value:
            return col + count
        count += 3
    return 0


# function that runs when key 1 is pressed
def key1Func():
    #do dance 1?

# function that runs when key 2 is pressed
def key2Func():
    #light LED?

# prints input to console
def printPressed():
    while True:
        keys = keypad.pressed_keys

        if keys:
            print("Pressed: ", keys)
        time.sleep(0.1)

# function that checks if input matches passcode every 4 input
def checkPass():
    seq = []
    pwd = [1, 3, 5, '*']
    i = 0

    while True: 
        keys = keypad.pressed_keys
        if keys: 
            seq.append(keys)
            i = i + 1
            time.sleep(0.4)

        if i >= 4: 
            if seq == pwd: 
                seq = []
                i = 0
                print("passcode correct")
            else: 
                seq = []
                print("password incorrect")

        time.sleep(0.1)

# main function loop
def main():
    checkPass()
    while True: 
        keys = keypad.pressed_keys

        if keys: 
            if keys == [1]: 
                key1Func()
            elif keys == [2]: 
                key2Func()
            elif keys == [3]: 
                key3Func()
            elif keys == [4]: 
                key4Func()
            elif keys == [5]: 
                key5Func()
            elif keys == [6]: 
                key6Func()
            # elif keys == [7]:
            #     key7Func()
            # elif keys == [8]:
            #     key8Func()
            # elif keys == [9]:
            #     key9Func()
            # elif keys == [0]:
            #     key0Func()
            # elif keys == ['*']:
            #     keyStarFunc()
            # elif keys == ['#']:
            #     keyPoundFunc()
            else: 
                print("Error. ")
            
