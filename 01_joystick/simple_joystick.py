import board
import analogio
import time

# Initialisiere die Pins für den Joystick
x_axis = analogio.AnalogIn(board.GP26)
y_axis = analogio.AnalogIn(board.GP27)

def get_voltage(pin):
    return (pin.value * 3.3) / 65536

while True:
    x_val = get_voltage(x_axis)
    y_val = get_voltage(y_axis)
    
    print(f"X-Achse: {x_val:.2f} V, Y-Achse: {y_val:.2f} V")
    
    time.sleep(0.1)
    