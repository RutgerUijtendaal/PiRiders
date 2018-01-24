#!/usr/local/bin/python3

import time
import RPi.GPIO as GPIO

import constants as c


class MotorController():
    '''
    MotorController class to control both wheels to create direction.

    Creates 2 motor objects with the assigned GPIO pins. Both motors are called
    every time a direction is set. Either both go forward or one goes backward
    and one forward (to turn)

    Also contains motor control for during the IntersectionState where the bot
    has to execute a longer move.

    '''
    def __init__(self):
        # Degrees the wheel turns per motor step
        self.deg_per_step = c.MOTOR_DEG_PER_STEP
        # Amount of steps for a full revolution of the wheels
        self.steps_per_rev = int(360 / self.deg_per_step)
        # Create motor objects for the controller to use
        self.ml = Motor(c.PINS_MOTOR_LEFT)
        # Motors are mirrored, one needs inverted directions
        self.mr = Motor(c.PINS_MOTOR_RIGHT, modifier=-1)

    def go_forward(self):
        self.mr.forward()
        self.ml.forward()

    def go_right(self):
        self.ml.forward()
        self.mr.backward()

    def go_left(self):
        self.mr.forward()
        self.ml.backward()

    # Go 1/8 of a wheel rotation forward
    def turn_ahead(self):
        for _ in range(int(self.steps_per_rev / 8)):
            self.go_forward()
            time.sleep(c.STEP_TIME)

    # Go 1/8 of a wheel rotation forward
    # Then go 1/4 of a wheel rotation to the left 
    def turn_left(self):
        self.turn_ahead()

        for _ in range(int(self.steps_per_rev / 4)):
            self.go_left()
            time.sleep(c.STEP_TIME)

    # Go 1/8 of a wheel rotation forward
    # Then go 1/4 of a wheel rotation to the right
    def turn_right(self):
        self.turn_ahead()

        for _ in range(int(self.steps_per_rev / 4)):
            self.go_right()
            time.sleep(c.STEP_TIME)


class Motor():
    '''
    Motor Class handles the control of one of the wheels

    Stepper Motors require a series of 4 inputs (on/off). You cycle
    these inputs, always moving the one a spot, to force the motor to rotate.

    By create a sequence of we move the 1 forward of backward 1 spot every step,
    which allows the wheel to move forward or backward.
    '''
    def __init__(self, pins, modifier=1):
        '''
        Requires the GPIO pins and in the constructor.
        Optionally a modifier can be set to -1 to always invert the wheel direction
        (in case it's assembled the wrong way around)
        '''
        self.pins = pins
        for pin in self.pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
        self.modifier = modifier
        # Adjust the direction if needed
        self.step_dir = 1 * self.modifier
        self.seq = [[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]]
        self.seq_length = len(self.seq)
        self.step_counter = 0

    def forward(self):
        # Make sure the direction is set to default
        self.step_dir = 1 * self.modifier
        self.take_step()

    def backward(self):
        # Invert the direction of the wheel to go backward
        self.step_dir = -1 * self.modifier
        self.take_step()

    def take_step(self):
        '''
        Take a step with the motor. 

        It cycles through all 4 inputs and checks the sequence. If the sequence
        has a 1 on the pins spot ([0, 1, 2, 3]) it sets that GPIO pin to True, else
        it sets it to False.

        Changing the True input 1 pin each time allows the motor to rotate
        '''
        # Loop through all the pins for this motor
        for pin in range(0, 4):
            xpin = self.pins[pin]
            # Check if the pin has a 1 or a 0
            if self.seq[self.step_counter][pin] != 0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)

        # Move the sequence one forward for next cycle
        self.step_counter += self.step_dir

        # Make sure we stay within the sequence length
        if self.step_counter >= self.seq_length:
            self.step_counter = 0
        if self.step_counter < 0:
            self.step_counter = self.seq_length + self.step_dir
