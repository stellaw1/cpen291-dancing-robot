import time
import board
import pulseio

piezo = pulseio.PWMOut(board.A1 , duty_cycle=0, frequency=440, variable_frequency=True)

def USSR_anthem():
    while True:
        for f in (196, 277, 196, 220, 247, 165, 165, 233, 196, 174, 208, 131, 131, 156, 147, 165, 185, 174, 196, 233, 123,
                262, 311, 311, 196, 330, 294, 261, 311, 247, 196, 277, 247, 220, 247, 165, 165, 233, 196, 131, 131, 277,
                247, 220, 207, 207, 207):
            piezo.frequency = f
            piezo.duty_cycle = 65536 // 2  # On 50%
            time.sleep(0.25)  # On for 1/4 second
            piezo.duty_cycle = 0  # Off
            time.sleep(0.05)  # Pause between notes
        time.sleep(0.5)

#Mario main theme melody
#Source: https://www.princetronics.com/supermariothemesong/
def mario_theme():
    while True:
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

# all i want for christmas intro
def crimson():
    while True:
        for f in (196, 247, 294, 370, 392, 370, 294, 247, 196, 262, 294, 392, 294):
            piezo.frequency = f
            piezo.duty_cycle = 65536 // 2  # On 50%
            time.sleep(0.25)  # On for 1/4 second
            piezo.duty_cycle = 0  # Off
            time.sleep(0.05)  # Pause between notes
        time.sleep(0.5)

# pachebel Canon in C
def canon():
    while True:
        for f in (196, 247, 294, 370, 392, 370, 294, 247, 196, 262, 294, 392, 294):
            piezo.frequency = f
            piezo.duty_cycle = 65536 // 2  # On 50%
            time.sleep(0.25)  # On for 1/4 second
            piezo.duty_cycle = 0  # Off
            time.sleep(0.05)  # Pause between notes
        time.sleep(0.5)