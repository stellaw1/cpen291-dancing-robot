import time
import board
import displayio
import terminalio
import label
from adafruit_st7735r import ST7735R

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
               

splash = displayio.Group(max_size=10)
reset()
textshow("Loading.....", 0x000000, 30, 64, 3)
reset()
textshow("Welcome", 0x000000, 30, 64, 3)
reset()
textshow("CPEN 291", 0x000000, 30, 64, 3)
reset()
textout("Press a key: \n 1) Dance Menu \n 2) About \n 3) Exit", 0x000000, 10, 60)
reset()
textout("Press a key: \n 1) Shuffle \n 2) Kick \n 3) Moonwalk \n 5) Wobble \n 5) Squat \n 6) Spin", 0x000000, 10, 60)
reset()
textout("About: \n Dancing Robot GUI \n Components: \n 1)Itsy Bitsy \n 2)TFT LCD \n 3)Servos \n 4)Ultrasonic sensor \n 5)Buzzer \n6)Keypad \n 7)RGB module/Shifter with LEDS \n Steps:\n 1)Power up: Welcome Menu that requests password\n 2)If password accepted a new window opens with a menu that has 6 dance moves to choose from If declined request for password again \n3)Press one of the first six buttons to do a dance (with particular music) move for a certain amount of time \n4)Come back to main menu\n 5)Might be able to display temperature as well (default lib / DHT11)", 0x000000, 10, 10)
reset()
textshow("Exiting.....", 0x000000, 30, 64, 3)
reset()
textshow("Created By: \n 1)Manek \n  2)Sanjeev \n 3)Parsa \n 4)Amir \n 5)Stella \n 6)Arnold \n 7)Rain", 0x000000, 10, 60, 3)
reset()