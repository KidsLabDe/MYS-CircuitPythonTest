import time
import board
import pwmio
from adafruit_motor import servo

# Initialisieren Sie PWM für den Servo-Motor am Pin GP11
pwm = pwmio.PWMOut(board.GP12, duty_cycle=0, frequency=50)

# Initialisieren Sie den Servo-Motor
# mein_servo = servo.Servo(pwm, actuation_range=180, min_pulse=750, max_pulse=2250)
mein_servo = servo.Servo(pwm)

# Funktion, um den Servo-Motor von -90 bis +90 Grad zu bewegen und zurück
def servo_bewegen(servo, start_winkel, end_winkel, schritt, wartezeit):
    for winkel in range(start_winkel, end_winkel + 1, schritt):
        servo.angle = winkel
        time.sleep(wartezeit)
    for winkel in range(end_winkel, start_winkel - 1, -schritt):
        servo.angle = winkel
        time.sleep(wartezeit)


# servo_bewegen(mein_servo, 0, 180, 1, 0.01)
mein_servo.angle = 0
time.sleep(0.5)
mein_servo.angle = 45
time.sleep(0.5)
mein_servo.angle = 90
time.sleep(0.5)
mein_servo.angle = 135
time.sleep(0.5)
mein_servo.angle = 180
time.sleep(0.5)
mein_servo.angle = 90
time.sleep(0.5)
