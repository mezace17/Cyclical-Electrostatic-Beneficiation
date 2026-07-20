'''
Written by Daniel Pikovskiy and Siyona Jain
'''
HOST = "localhost"
PORT = 4223

UID1 = "21b7"
UID2 = "25GT"
UID3 = "25GV"

import time
from gpiozero import Button
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_silent_stepper_v2 import BrickletSilentStepperV2

# limit switches
limit1 = Button(17, pull_up=True)
limit2 = Button(27, pull_up=True)
limit3 = Button(22, pull_up=True)

# motor setup
def setup_motor(ss):
    ss.set_motor_current(800)
    ss.set_step_configuration(ss.STEP_RESOLUTION_8, True)
    ss.set_max_velocity(5000)
    ss.set_speed_ramping(1000, 5000)
    ss.set_enabled(True)

def stop_motor(ss):
    ss.stop()
    time.sleep(0.3)
    ss.set_enabled(False)

def home_plate1(ss1):
    print("\nhoming plate 1")

    motor1_done = limit1.is_pressed
    if motor1_done:
        print("motor 1 already on limit")

    # only start motor if not homed
    if not motor1_done:
        ss1.drive_forward()

    #keep checking if the motor is homed
    while True:

        #when the motor is homed, stop the motor and break out of the loop
        if limit1.is_pressed:
            stop_motor(ss1)
            setup_motor(ss1)
            motor1_done = True
            break

    time.sleep(0.01)
    print("Plate 1 homed")

def home_plate2(ss2):
    print("\nhoming plate 2")

    motor2_done = limit2.is_pressed
    if motor2_done:
        print("motor 2 already on limit")

    # only start motor if not homed
    if not motor2_done:
        ss2.drive_forward()

    #keep checking if the motor is homed
    while True:

        #when the motor is homed, stop the motor and break out of the loop
        if limit2.is_pressed:
            stop_motor(ss2)
            setup_motor(ss2)
            motor2_done = True
            break

    time.sleep(0.01)
    print("Plate 2 homed")

# retract plates
def retract_plates(ss1, ss2):

    retract_steps = -50000

    print("\nretracting plates")

    motor1_done = False
    motor2_done = False

    ss1.set_steps(retract_steps)
    ss2.set_steps(retract_steps)

    while not (motor1_done and motor2_done):

        # MOTOR 1
        if not motor1_done and ss1.get_remaining_steps() == 0:
            print("motor 1 retracted")
            stop_motor(ss1)
            motor1_done = True

        # MOTOR 2
        if not motor2_done and ss2.get_remaining_steps() == 0:
            print("motor 2 retracted")
            stop_motor(ss2)
            motor2_done = True

        time.sleep(0.01)

    print("both motors retracted")

def motor3_sequence(ss3):

    totalSteps = 0
    steps = 0
    setup_motor(ss3)
    while True:
        try:
            #prompt user to input how far to move the bed or to return to zero

            response = input("Enter how many steps to move the bed up by, or type end to return the bed to home: ")
            if response.lower() == 'end':
                #move the motor back and terminate the loop
                print("motor 3: moving to home")
                ss3.set_steps(totalSteps)
                #keep moving back until we reach home
                while ss3.get_remaining_steps() > 0:
                    time.sleep(0.01)

                stop_motor(ss3)
                break

            else:

                steps = abs(int(response))
                totalSteps += steps
                ss3.set_steps(-1*steps)

                #move the motor back
                print("motor 3: tilting bed")
                while ss3.get_remaining_steps() < 0:
                    time.sleep(0.01)

                stop_motor(ss3)

                setup_motor(ss3)

        except ValueError:
            print("must input either the word end or a number")

    print("motor 3: back at home after having moved a total of", totalSteps, "total steps up")

# main
if __name__ == "__main__":

    ipcon = IPConnection()

    ss1 = BrickletSilentStepperV2(UID1, ipcon)
    ss2 = BrickletSilentStepperV2(UID2, ipcon)
    ss3 = BrickletSilentStepperV2(UID3, ipcon)

    ipcon.connect(HOST, PORT)

    setup_motor(ss1)
    setup_motor(ss2)
    setup_motor(ss3)

    # ensure switches are pressed
    # home_plates(ss1, ss2)
    input("\npress enter to home plate 1:")

    home_plate1(ss1)

    input("\npress enter to home plate 2:")

    home_plate2(ss2)

    # retract plates
    input("\nswitches are pressed. press enter to retract plates:")

    retract_plates(ss1, ss2)

    # tilt and return bed (motor 3)
    input("\npress enter to begin bed tilt procedure:")

    motor3_sequence(ss3)

    # disconnect
    ipcon.disconnect()
