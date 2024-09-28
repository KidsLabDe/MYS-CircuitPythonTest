import board
import digitalio
import adafruit_tm1637

# Initialisiere die Pins für das TM1637-Modul
clk = digitalio.DigitalInOut(board.GP5)
dio = digitalio.DigitalInOut(board.GP4)

# Initialisiere das TM1637-Modul
display = adafruit_tm1637.TM1637(clk, dio)

# Setze die Helligkeit (optional)
display.brightness = 0.5

# Zeige eine Zahl auf dem Display an
display.show('1234')

# Alternativ: Zeige jede Ziffer einzeln an
# display[0] = 1
# display[1] = 2
# display[2] = 3
# display[3] = 4