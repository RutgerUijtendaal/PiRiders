import RPi.GPIO as GPIO
import time

import constants as c

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class Led():
    '''
    Represents a single led that can be turned on or off
    '''
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)


class FrontLeds():
    '''
    Create 4 led objects for the 4 front leds.

    Every 50 ticks of the bot the led moves 1 forward, cycling back when it reaches
    an end.
    '''
    def __init__(self, pins):
        self.pins = pins
        self.leds = []
        for pin in self.pins:
            self.leds.append(Led(pin))
        self.current_led = 2
        self.counter = 0
        self.modifier = 1

    def tick(self):
        # Every 50 ticks we switch leds
        if self.counter % 50 == 0:
            # First turn off all leds
            for led in self.leds:
                led.off()

            # Turn on the next led in the sequence
            self.leds[self.current_led].on()

            # Increase/decrease the counter by one for next cycle
            self.current_led += self.modifier

            # Invert the modifier to go back and forth with the led cycle
            if self.current_led == 3 or self.current_led == 0:
                self.modifier = self.modifier * -1

        self.counter += 1


class LedController():
    '''
    Gather both the front and side leds in a LedController to allow control
    of all leds from 1 class
    '''
    def __init__(self):
        self.front_led = FrontLeds(c.PINS_FRONT_LED)
        self.left_led = Led(c.PINS_LEFT_LED)
        self.right_led = Led(c.PINS_RIGHT_LED)

    def forward_led_tick(self):
        self.front_led.tick()

    def turn_on_left_led(self):
        self.left_led.on()

    def turn_on_right_led(self):
        self.right_led.on()

    def turn_off_side_leds(self):
        self.left_led.off()
        self.right_led.off()
