import time
import board
import pwmio
import digitalio
import neopixel
#import RPi.GPIO as GPIO
import time
import adafruit_hcsr04
from adafruit_motor import motor


btn1 = digitalio.DigitalInOut(board.GP20)
btn2 = digitalio.DigitalInOut(board.GP21)
btn1.direction = digitalio.Direction.INPUT
btn2.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.UP
btn2.pull = digitalio.Pull.UP
PWM_M1A = board.GP8
PWM_M1B = board.GP9
PWM_M2A = board.GP10
PWM_M2B = board.GP11
abstand_vorne = adafruit_hcsr04.HCSR04(trigger_pin=board.GP4, echo_pin=board.GP5)
abstand_hinten = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP26)

# DC motor setup
#M1A = pwmio.PWMOut(PWM_M1A, frequency=10000)
#M1B = pwmio.PWMOut(PWM_M1B, frequency=10000)
#M2A = pwmio.PWMOut(PWM_M2A, frequency=10000)
#M2B = pwmio.PWMOut(PWM_M2B, frequency=10000)
M1A = pwmio.PWMOut(PWM_M1A, frequency=10000)
M1B = pwmio.PWMOut(PWM_M1B, frequency=10000)
M2A = pwmio.PWMOut(PWM_M2A, frequency=10000)
M2B = pwmio.PWMOut(PWM_M2B, frequency=10000)
motor1 = motor.DCMotor(M1A, M1B)
motor2 = motor.DCMotor(M2A, M2B)

# Throttle value must be between -1.0 and +1.0 or None (Free-Moving)
print("***Start***")
pixels = neopixel.NeoPixel(board.GP18, 2)
pixels.fill(0)

while True:
    try:
        print((abstand_vorne.distance))

    except RuntimeError:
        print("Nicht angeschlossen!")
        pass
    time.sleep(0.1)
    
    try:
        print((abstand_hinten.distance))

    except RuntimeError:
        print("Nicht angeschlossen!")
        pass
    time.sleep(0.1)

while True:
    
    

    
    if not btn1.value:  # button 1 pressed
        # Light up all LEDs
        print("btn1 - motor-start")
        while btn2.value:
              #messung abstand von hier
            try:
                print((abstand_vorne.distance))

            except RuntimeError:
                print("Nicht angeschlossen!")
                pass
                time.sleep(0.1)
    
            try:
                print((abstand_hinten.distance))

            except RuntimeError:
                print("Nicht angeschlossen!")
                pass
                time.sleep(0.1)
    #bis hier
    
    
    
    
    
    
    
    
    
    
        print("Vorwärts")
        motor1.throttle = 0.5
        motor2.throttle = 0.5
        time.sleep(3)
        print("Stop")
        motor1.throttle = None
        motor2.throttle = None
        time.sleep(2)
        
        print("Rückwärts")
        motor1.throttle = -0.5
        motor2.throttle = -0.5
        time.sleep(3)

        print("Stop")
        motor1.throttle = None
        motor2.throttle = None
        time.sleep(2)

        print("Finished")
           
           
    