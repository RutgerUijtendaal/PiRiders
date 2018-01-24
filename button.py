#!/usr/local/bin/python3

import RPi.GPIO as GPIO
import time

class Button(object):
    '''
    Button class represents a button.

    Has one property to read the current value.
    '''
    def __init__(self, pin):
        self.pin = pin
        # Have to set pull_up_down to make sure the button
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # @Property in Python allows you to call a function like an attribute of a class
    # Basically functions like a getter
    @property
    def value(self):
        return 1 - GPIO.input(self.pin)
