import time
import board
import pwmio
import digitalio
import neopixel
import adafruit_hcsr04
from adafruit_motor import motor

# Set up buttons
btn1 = digitalio.DigitalInOut(board.GP20)  # Button 1 to start the motor
btn2 = digitalio.DigitalInOut(board.GP21)  # Button 2 to stop the motor
btn1.direction = digitalio.Direction.INPUT
btn2.direction = digitalio.Direction.INPUT
btn1.pull = digitalio.Pull.UP
btn2.pull = digitalio.Pull.UP

# Set up ultrasonic sensors
abstand_vorne = adafruit_hcsr04.HCSR04(trigger_pin=board.GP4, echo_pin=board.GP5)
abstand_hinten = adafruit_hcsr04.HCSR04(trigger_pin=board.GP6, echo_pin=board.GP26)

# Set up motor control pins
PWM_M1A = board.GP8
PWM_M1B = board.GP9
PWM_M2A = board.GP10
PWM_M2B = board.GP11

# DC motor setup
M1A = pwmio.PWMOut(PWM_M1A, frequency=10000)
M1B = pwmio.PWMOut(PWM_M1B, frequency=10000)
M2A = pwmio.PWMOut(PWM_M2A, frequency=10000)
M2B = pwmio.PWMOut(PWM_M2B, frequency=10000)
motor1 = motor.DCMotor(M1A, M1B)
motor2 = motor.DCMotor(M2A, M2B)

# Set up neopixel LED
pixels = neopixel.NeoPixel(board.GP18, 2)
pixels.fill(0)  # Turn off LEDs initially

# Start message
print("*** Start ***")

motor_running = False  # Flag to track if the motor is running

def beep():
    piezo.value = True  # Buzzer an
    time.sleep(0.1)     # Warte für 100ms
    piezo.value = False # Buzzer aus
    time.sleep(0.1)     # Pause zwischen den Tönen

def vorwärts():
    motor1.throttle = 0
    motor2.throttle = 0
    time.sleep(7)
    motor1.throttle = -0.5  # Move backward
    motor2.throttle = -0.5  # Move backward
    pixels.fill((255, 0, 0))  # Turn LEDs blue when moving backward

def rückwärts() :
    motor1.throttle = 0
    motor2.throttle = 0
    time.sleep(7)
    motor1.throttle = 0.5  # Move forward
    motor2.throttle = 0.5  # Move forward
    pixels.fill((255, 255, 255))

while True:
    # If btn1 is pressed, start the motor
    if not btn1.value:  # If button 1 is pressed (start)
        if not motor_running:  # If the motor is not already running
            print("Motor started")
            motor1.throttle = -0.5  # Move backward
            motor2.throttle = -0.5  # Move backward
            pixels.fill((0, 0, 255))  # Turn LEDs blue when moving backward
            pixels.fill((255, 0, 0))  # Turn on red LED when motor starts
            motor_running = True  # Set motor_running to True
            time.sleep(0.5)  # Debounce time to prevent multiple triggers

    # If btn2 is pressed, stop the motor
    if not btn2.value:  # If button 2 is pressed (stop)
        if motor_running:  # If the motor is running
            print("Motor stopped")
            motor1.throttle = 0  # Stop motor
            motor2.throttle = 0  # Stop motor
            pixels.fill(0)  # Turn off LEDs when motor stops
            motor_running = False  # Set motor_running to False
            time.sleep(0.5)  # Debounce time to prevent multiple triggers

    # If the motor is running, check the distances and move accordingly
    if motor_running:
        try:
            # Measure distance in front
            front_distance = abstand_vorne.distance
            print(f"Front distance: {front_distance} cm")
        except RuntimeError:
            print("Front sensor not connected!")
            front_distance = None

        try:
            # Measure distance behind
            back_distance = abstand_hinten.distance
            print(f"Back distance: {back_distance} cm")
        except RuntimeError:
            print("Back sensor not connected!")
            back_distance = None

        # If the front distance is less than 4 cm, go backward
        if front_distance is not None and front_distance < 6:
            vorwärts() 
            
            
            
        if back_distance is not None and back_distance < 6:
            rückwärts()
            
            

        time.sleep(0.1)  # Small delay to prevent excessive CPU usage
