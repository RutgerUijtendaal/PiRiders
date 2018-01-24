#!/usr/local/bin/python3

import RPi.GPIO as GPIO

from enums import Input


class Sensor(object):
    '''
    Sensor class to contact the sensor.

    Creates a sensor object with the GPIO pins and reads out the data

    Returns an INPUT enumeration of which leds found black below them.
    '''
    def __init__(self, pins):
        self.pins = pins
        for p in self.pins:
            GPIO.setup(p, GPIO.IN)

    # @Property in Python allows you to call a function like an attribute of a class
    # Basically functions like a getter
    @property
    def data(self):
        s_left = GPIO.input(self.pins[0])
        s_middle = GPIO.input(self.pins[1])
        s_right = GPIO.input(self.pins[2])
        return((s_left, s_middle, s_right))

    # @Property in Python allows you to call a function like an attribute of a class
    # Basically functions like a getter
    @property
    def sensor_input(self):
        sens_data = self.data

        if sens_data == (1, 0, 0) or sens_data == (1, 1, 0):
            return Input.RIGHT
        elif sens_data == (0, 0, 1) or sens_data == (0, 1, 1):
            return Input.LEFT
        elif sens_data == (1, 0, 1):
            return Input.MIDDLE
        elif sens_data == (0, 0, 0):
            return Input.INTERSECTION
        elif sens_data == (1, 1, 1):
            return Input.NO_SENSOR

