# servo_animation_code.py -- show simple servo animation list
import time, random, board
from pwmio import PWMOut
from adafruit_motor import servo

# positionen für jeden servo, die wir durchlaufen
positionen = [[90, 90, 90, 90], [45,45,45,45], [0, 0, 45, 0], [180, 180, 180, 180]]


# your servo will likely have different min_pulse & max_pulse settings
servoA = servo.Servo(PWMOut(board.GP12, frequency=50), min_pulse=500, max_pulse=2250)
servoB = servo.Servo(PWMOut(board.GP13, frequency=50), min_pulse=500, max_pulse=2250)
servoC = servo.Servo(PWMOut(board.GP14, frequency=50), min_pulse=500, max_pulse=2250)
servoD = servo.Servo(PWMOut(board.GP15, frequency=50), min_pulse=500, max_pulse=2250)

# the animation to play
animation = (
    (0, 2.0),
    (90, 2.0),
    (120, 2.0),
    (180, 2.0)
)
ani_pos = 0 # where in list to start our animation
ease_speed = 0.2# how fast to move between positions
num_ease_slices = 50 # how many steps to take between positions

servoA.angle = 50 # start at 0

DEBUG = False

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


def move_servos(servos, positions):
    for servo, position in zip(servos, positions):
        servo.angle = position



print("Start")
print("erst mal normal")
move_servos([servoA, servoB, servoC, servoD], positionen[0])


while True:
    print("jetzt eased")    
    # get the start and end position from the positionen list
    start_positions = positionen[ani_pos]
    end_positions = positionen[(ani_pos + 1) % len(positionen)]
    max_angle_change = max(abs(end - start) for start, end in zip(start_positions, end_positions))
    duration = 2.0 * (max_angle_change / 180.0)  # scale duration based on the maximum angle change
    print("Duration: ", duration, "Max angle change: ", max_angle_change)
    print("Startposition: ", start_positions, "Endposition: ", end_positions)
    
    # move the servos
    move_servos_eased([servoA, servoB, servoC, servoD], start_positions, end_positions, duration)

    # move to the next position
    ani_pos = (ani_pos + 1) % len(positionen)
    time.sleep(0.5)  # wait a bit before starting the animation again
