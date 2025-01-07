import board
import analogio
import time
import neopixel
import pwmio
from adafruit_motor import servo
import digitalio

import rotaryio



# Die Positionen sind für:
# [Drehfuss, Arm unten, Arm oben, Greifer]
positionen = [[90, 90, 90, 90]
             ]


# Bewegungsverzögerung in Sekunden
Bewegungsdauer = 0.4


encoder = rotaryio.IncrementalEncoder(board.GP2, board.GP3)
last_position = None


# Anzahl der LEDs
num_pixels = 1

# Pin, an dem die WS2812 LED angeschlossen ist
pixel_pin = board.GP18

# Erstelle ein NeoPixel-Objekt
pixels = neopixel.NeoPixel(pixel_pin, num_pixels)

# Initialisiere die Pins für den Joystick
x_axis = analogio.AnalogIn(board.GP26)
y_axis = analogio.AnalogIn(board.GP27)


achsen = [90,90,90,90]


# Initialisieren Sie PWM für den Servo-Motor am Pin GP11
pwm1 = pwmio.PWMOut(board.GP12, duty_cycle=0, frequency=50)
pwm2 = pwmio.PWMOut(board.GP13, duty_cycle=0, frequency=50)
pwm3 = pwmio.PWMOut(board.GP14, duty_cycle=0, frequency=50)
pwm4 = pwmio.PWMOut(board.GP15, duty_cycle=0, frequency=50)

# Initialisieren Sie den Servo-Motor
# mein_servo = servo.Servo(pwm, actuation_range=180, min_pulse=750, max_pulse=2250)
servo1 = servo.Servo(pwm1)
servo2 = servo.Servo(pwm2)
servo3 = servo.Servo(pwm3)
servo4 = servo.Servo(pwm4)


pwms = [pwm1, pwm2, pwm3, pwm4]

def get_voltage(pin):
    return (pin.value * 3.3) / 65536


  
# Set up GP20 as an input with a pull-up resistor
btn_rec = digitalio.DigitalInOut(board.GP20)
btn_rec.direction = digitalio.Direction.INPUT
btn_rec.pull = digitalio.Pull.UP  # Use a pull-up resistor

# Set up GP20 as an input with a pull-up resistor
btn_play = digitalio.DigitalInOut(board.GP21)
btn_play.direction = digitalio.Direction.INPUT
btn_play.pull = digitalio.Pull.UP  # Use a pull-up resistor




def get_duty_cycle(x):
    return int((4369*x+196605)/30)

# Funktion zum Setzen des PWM-Duty-Cycles für einen bestimmten Winkel
def set_servo_angle(pwm, angle):
    pwm.duty_cycle = get_duty_cycle(angle)


# Funktion für Servo Easing
def ease_in_out(t):
    return t * t * (3 - 2 * t)

def move_servos_eased(pwms, start_angles, end_angles, duration):
    steps = 500
    
    for i in range(steps + 1):
        t = i / steps
        eased_t = ease_in_out(t)
        for pwm, start_angle, end_angle in zip(pwms, start_angles, end_angles):
            # print(pwm, start_angle, end_angle)
            angle = start_angle + (end_angle - start_angle) * eased_t
            set_servo_angle(pwm, angle)
        time.sleep(duration / steps)


def zuPosBewegen(positionen):

    # Beispiel: Bewege alle Servos zu allen Positionen in 2 Sekunden
    pixels[0] = (0, 255, 0)
    pixels.show()
    for aktuelle_pos in range(len(positionen)-1):
        move_servos_eased(pwms, positionen[aktuelle_pos], positionen[aktuelle_pos+1], Bewegungsdauer)

    for i in pwms:
        i.deinit()

    # Bereit
    pixels[0] = (100, 0, 0)
    pixels.show()


while True:
    x_val = get_voltage(x_axis)
    y_val = get_voltage(y_axis)
    
    position = encoder.position
    GradProKlick = 5
    if last_position is None or position != last_position:
        print(position)
        if position > (90 / GradProKlick):
            position = (90 / GradProKlick)
            encoder.position = int(90 / GradProKlick)

        if position < -(90 / GradProKlick):
            position = -(90 / GradProKlick)
            encoder.position = -int(90 / GradProKlick)

        winkel = 90 + position * 5
        servo1.angle = winkel
    last_position = position
    
    # print(f"X-Achse: {x_val:.2f} V, Y-Achse: {y_val:.2f} V")
    
    time.sleep(0.1)
    
    if x_val < 1.6:
        bewegung = abs(x_val - 1.6)
        if (achsen[2] < 170):
            achsen[2] += bewegung * 5
            servo2.angle = achsen[2]
            print(f"Joystick nach links {achsen[2]}")
    if x_val > 1.7:
        bewegung = x_val - 1.7
        if (achsen[2] > 10):
            achsen[2] -= bewegung * 5
            servo2.angle = achsen[2]
            print(f"Joystick nach rechts {achsen[2]}")
    if y_val < 1:
        if (achsen[3] < 170):
            achsen[3] += 5
            servo3.angle = achsen[3]
            print(f"Joystick nach unten {achsen[3]}")
    elif y_val > 2:   
        if (achsen[3] > 10):
            achsen[3] -= 5
            servo3.angle = achsen[3]
            print(f"Joystick nach oben {achsen[3]}")
            
    # Check if the button is pressed
    if not(btn_play.value):
        print("PLAY is pressed")
        zuPosBewegen(positionen)
        
        time.sleep(1)
    if not(btn_rec.value):
        print("REC is pressed")
        positionen.append(achsen)
        print(positionen)
        time.sleep(1)
