import board
import digitalio
import pwmio
from adafruit_motor import servo
import time


button_up = digitalio.DigitalInOut(board.GP20)
button_up.direction = digitalio.Direction.INPUT
button_up.pull = digitalio.Pull.UP

button_down = digitalio.DigitalInOut(board.GP21)
button_down.direction = digitalio.Direction.INPUT
button_down.pull = digitalio.Pull.UP


# The SG92R servo typically has the following PWM pulse width range:
# Set up servos
pwm_pins = [board.GP12, board.GP13, board.GP14, board.GP15]
servos = []
for pin in pwm_pins:
    pwm = pwmio.PWMOut(pin, duty_cycle=0, frequency=50)
    servos.append(servo.Servo(pwm, min_pulse=500, max_pulse=2400))

# Initial servo angle
angle = 90
for s in servos:
    s.angle = angle
print(f"Initial angle: {angle}")

while True:
    if not(button_up.value):
        angle = min(angle + 10, 180)
        for s in servos:
            s.angle = angle
        print(f"Angle increased to: {angle}")
        time.sleep(0.5)

    if not(button_down.value):
        angle = max(angle - 10, 0)
        for s in servos:
            s.angle = angle
        print(f"Angle decreased to: {angle}")
        time.sleep(0.5)

