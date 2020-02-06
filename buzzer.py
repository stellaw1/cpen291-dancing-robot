# Starter code taken from https://learn.adafruit.com/introducing-adafruit-itsybitsy-m4/circuitpython-pwm

import time
import board
import simpleio
 
# For the M4 boards:
piezo = pulseio.PWMOut(board.A1, duty_cycle=0, frequency=440, variable_frequency=True)

# g +C g a B e e A g f G c c D d e F f g A b    +c   +D p g +E +d +c   +D b g +C b a B e e A g f G c c +C b a G p p
freq_ussr = [196, 277, 196, 220, 247, 165, 165, 233, 196, 174, 208, 131, 131, 156, 147, 165, 185, 174, 196, 233, 123,
             262, 311, 311, 196, 330, 294, 261, 311, 247, 196, 277, 247, 220, 247, 165, 165, 233, 196, 131, 131, 277,
             247, 220, 207, 207, 207]

while True:
    for f in range(freq_ussr):
        piezo.frequency = f
        piezo.duty_cycle = 65536 // 2  # On 50%
        time.sleep(0.25)  # On for 1/4 second
        piezo.duty_cycle = 0  # Off
        time.sleep(0.05)  # Pause between notes
    time.sleep(0.5)