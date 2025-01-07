import board
import analogio
import time
import neopixel
import pwmio
from adafruit_motor import servo
import digitalio

import rotaryio


def init():
    global positionen, DEBUG, Bewegungsdauer, encoder, last_position, num_pixels, pixel_pin, pixels, x_axis, y_axis, achsen, pwm1, pwm2, pwm3, pwm4, servo1, servo2, servo3, servo4, pwms, btn_rec, btn_change, axis_12, btn_play

    # Die Positionen sind für:
    # [Drehfuss, Arm unten, Arm oben, Greifer]
    positionen = [[90, 90, 90, 90], [13, 72, 125, 130], [13, 72, 125, 130], [13, 72, 125, 130], [13, 72, 125, 130], [13, 72, 125, 130]]

    DEBUG = False
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

    achsen = [90, 90, 90, 90]

    # Initialisieren Sie PWM für den Servo-Motor am Pin GP11
    pwm1 = pwmio.PWMOut(board.GP12, duty_cycle=0, frequency=50)
    pwm2 = pwmio.PWMOut(board.GP13, duty_cycle=0, frequency=50)
    pwm3 = pwmio.PWMOut(board.GP14, duty_cycle=0, frequency=50)
    pwm4 = pwmio.PWMOut(board.GP15, duty_cycle=0, frequency=50)

    # Initialisieren Sie den Servo-Motor
    servo1 = servo.Servo(pwm1)
    servo2 = servo.Servo(pwm2)
    servo3 = servo.Servo(pwm3)
    servo4 = servo.Servo(pwm4)

    pwms = [pwm1, pwm2, pwm3, pwm4]

    # Set up GP20 as an input with a pull-up resistor
    btn_rec = digitalio.DigitalInOut(board.GP20)
    btn_rec.direction = digitalio.Direction.INPUT
    btn_rec.pull = digitalio.Pull.UP  # Use a pull-up resistor

    # der change butten ändert die achsen - die pico hat nur 3 ADC und kann deswegen nur 1 1/2 joysticks abfragen
    btn_change = digitalio.DigitalInOut(board.GP19)
    btn_change.direction = digitalio.Direction.INPUT
    btn_change.pull = digitalio.Pull.UP  # Use a pull-up resistor

    # wir merken uns, welche achsen gerade angesteuert werden
    axis_12 = True

    # Set up GP20 as an input with a pull-up resistor
    btn_play = digitalio.DigitalInOut(board.GP21)
    btn_play.direction = digitalio.Direction.INPUT
    btn_play.pull = digitalio.Pull.UP  # Use a pull-up resistor

# Call the init function to initialize everything
init()


def get_voltage(pin):
    return (pin.value * 3.3) / 65536


def ease_in_out(t):
    """
    Kubische Easing-Funktion für sanftere Bewegungen
    t: Float zwischen 0.0 und 1.0
    """
    if t < 0.5:
        return 4 * t * t * t
    else:
        p = 2 * t - 2
        return 0.5 * p * p * p + 1

def set_servo_angle(pwm, angle):
    """
    Setzt den Servo auf einen bestimmten Winkel
    pwm: PWM-Objekt
    angle: Winkel in Grad (0-180)
    """
    # Typische Werte für SG90 Servo (anpassen falls nötig)
    min_duty = 0.5  # 0.5ms bei 0°
    max_duty = 2.5  # 2.5ms bei 180°
    duty = min_duty + (max_duty - min_duty) * (angle / 180)
    pwm.duty_cycle = int(duty * 65535 / 100)  # Umrechnung für 16-bit Timer

def move_servos_eased(pwms, start_angles, end_angles, duration, steps=500):
    """
    Bewegt mehrere Servos gleichzeitig mit Easing
    
    Parameters:
        pwms: Liste von PWM-Objekten
        start_angles: Liste der Startwinkel
        end_angles: Liste der Zielwinkel
        duration: Gesamtdauer der Bewegung in Sekunden
        steps: Anzahl der Zwischenschritte (default: 500)
    """
    # Eingabevalidierung
    if not (len(pwms) == len(start_angles) == len(end_angles)):
        raise ValueError("Anzahl der PWMs, Start- und Endwinkel muss übereinstimmen")
    
    # Minimale Verzögerung zwischen Schritten (in Sekunden)
    min_delay = 0.001
    
    # Berechne tatsächliche Verzögerung
    step_delay = max(duration / steps, min_delay)
    actual_steps = int(duration / step_delay)
    
    try:
        for i in range(actual_steps + 1):
            t = i / actual_steps
            eased_t = ease_in_out(t)
            
            for pwm, start_angle, end_angle in zip(pwms, start_angles, end_angles):
                # Begrenze Winkel auf gültigen Bereich
                angle = max(0, min(180, start_angle + (end_angle - start_angle) * eased_t))
                set_servo_angle(pwm, angle)
                
            time.sleep(step_delay)
            
    except KeyboardInterrupt:
        # Sauberes Beenden bei Ctrl+C
        print("Bewegung unterbrochen")
        
    except Exception as e:
        print(f"Fehler während der Bewegung: {e}")
        raise


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



def move_servos_eased(servos, start_positions, end_positions, duration):
    steps = 500
    for i in range(steps + 1):
        t = i / steps
        eased_t = t * t * (3 - 2 * t)
        for servo, start_pos, end_pos in zip(servos, start_positions, end_positions):
            if DEBUG:
                print("Servo: ", servo, "Start: ", start_pos, "End: ", end_pos)
            servo.angle = start_pos + (end_pos - start_pos) * eased_t
        time.sleep(duration / steps)


servo1.angle=achsen[0]
servo2.angle=achsen[1]
servo3.angle=achsen[2]
servo4.angle=achsen[3]
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
    
    if axis_12:
        axis1 = 1
        axis2 = 2
    else:
        axis1 = 0
        axis2 = 3
    
    if x_val < 1.6:
        bewegung = abs(x_val - 1.6)
        if (achsen[axis1] < 170):
            achsen[axis1] += int(bewegung * 5)
            if axis_12:
                servo2.angle = achsen[axis1]
            else:
                servo1.angle = achsen[axis1]
            print(f"Joystick nach links {axis1} {achsen[axis1]}")
    if x_val > 1.7:
        bewegung = x_val - 1.7
        if (achsen[axis1] > 10):
            achsen[axis1] -= int(bewegung * 5)
            if axis_12:
                servo2.angle = achsen[axis1]
            else:
                servo1.angle = achsen[axis1]
            print(f"Joystick nach rechts {axis1} {achsen[axis1]}")
    if y_val < 1:
        if (achsen[axis2] < 170):
            achsen[axis2] += 5
            if axis_12:
                servo3.angle = achsen[axis2]
            else:
                servo4.angle = achsen[axis2]
            print(f"Joystick nach unten {axis2} {achsen[axis2]}")
    elif y_val > 2:   
        if (achsen[axis2] > 10):
            achsen[axis2] -= 5
            if axis_12:
                servo3.angle = achsen[axis2]
            else:
                servo4.angle = achsen[axis2]
            print(f"Joystick nach oben {axis2} {achsen[axis2]}")
            
    # Check if the button is pressed
    if not(btn_play.value):
        print("PLAY is pressed")
        # loop through the positions
        for i in range(0, len(positionen)):
            print(positionen[i])
            move_servos_eased([servo1, servo2, servo3, servo4], achsen, positionen[i], Bewegungsdauer)
            achsen = positionen[i]
        # zuPosBewegen(positionen)
        print("Ende")
        
        time.sleep(1)
    if not(btn_rec.value):
        print("REC is pressed")
        positionen.append(achsen)
        print(positionen)
        time.sleep(1)

    if not(btn_change.value):
        print("CHANGE is pressed")
        axis_12 = not(axis_12)
        print(axis_12)
        # positionen = [[90, 90, 90, 90]]
        time.sleep(1)
