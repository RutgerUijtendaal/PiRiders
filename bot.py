import time
import urllib.request
import json

import RPi.GPIO as GPIO

import constants as c
from motor import MotorController
from led import LedController
from sensor import Sensor
from button import Button
from enums import Destination, Input

# We import from lots of other files, So instead of having a huge file full of 
# random code we create multiple files for each purpose to keep things a bit organized

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class State(object):
    '''
    The bot is a StateMachine running through different states to represent its
    current job.

    Every tick of the program the bot object runs the run() of the state it's in.

    State changes are triggered by Sensor Data changing, a new delivery coming in or
    the button being pressed. These will be named events. 

    This is the abstract state State class and all other classes implement this class 
    to ensure that every child class implements on_event() and run()

    Also gives access to an overaching function to print the name of the state the program
    is in by using __class__.__name__ and returning that as a string
    '''
    def __init__(self):
        pass

    def on_event(self, event):
        ''' Handles new incoming events '''
        assert 0, "on_event not implemented"

    def run(self):
        assert 0, "run not implemented"

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__


class IdleState(State):
    '''
    The bot always boots in IdleState and requires a button press event 
    to change state into ReceivingState

    There is no run code for this State as it's named IdleState and well...
    is for idling in
    '''
    def __init__(self, bot):
        self.bot = bot

    def on_event(self, event):
        if event == 'button_pressed':
            return ReceivingState(self.bot)

        return self

    def run(self):
        pass


class ReceivingState(State):
    '''
    The active waiting state of the bot. If no new orders are in this
    state continously checks to see if new orders are in.

    If a new_delivery event is fired 
    '''
    def __init__(self, bot):
        self.bot = bot

    def on_event(self, event):
        if event == 'new_delivery':
            return ForwardState(self.bot)
        if event == 'button_pressed':
            return IdleState(self.bot)

        return self

    def run(self):
        pass


class ForwardState(State):
    '''
    The default state the moving robot wants to return to. Any adjustments made 
    eg. turning left, turning right or taking an intersection are ways to get back to
    this state.
    '''
    def __init__(self, bot):
        self.bot = bot

    def on_event(self, event):
        if event == 'l_sensor':
            return LeftState(self.bot)
        if event == 'r_sensor':
            return RightState(self.bot)
        if event == 'button_pressed':
            return EndState(self.bot)
        if event == 'intersection':
            return IntersectionState(self.bot)
        return self

    def run(self):
        self.bot.motor.go_forward()


class LeftState(State):
    '''
    When a sensor on the left detects black we transition to LeftState.
    '''
    def __init__(self, bot):
        self.bot = bot

    def on_event(self, event):
        if event == 'm_sensor' or event == 'no_sensor':
            return ForwardState(self.bot)
        if event == 'button_pressed':
            return EndState(self.bot)
        if event == 'intersection':
            return IntersectionState(self.bot)
        return self

    def run(self):
        '''
        Tell the MotorController to go right 1 step
        Pulls the left wheel back and the right wheel forward
        '''
        self.bot.motor.go_left()


class RightState(State):
    '''
    When a sensor on the right detects black we transition to LeftState.
    '''
    def __init__(self, bot):
        self.bot = bot

    def on_event(self, event):
        if event == 'm_sensor' or event == 'no_sensor':
            return ForwardState(self.bot)
        if event == 'button_pressed':
            return EndState(self.bot)
        if event == 'intersection':
            return IntersectionState(self.bot)
        return self

    def run(self):
        '''
        Tell the MotorController to go left 1 step
        Pulls the left wheel back and the right wheel forward
        '''
        self.bot.motor.go_right()


class IntersectionState(State):
    '''
    When all sensors detect black we transitioin to IntersectionState

    The first time this state is reached we check the destination of the bot
    and turn accordingly. After that we always set the destination to END and
    try to go back to ForwardState like normal.

    The second time an intersection is reached we're in END destination, 
    which is then reached. We go forward till no sensor data is read and stop the
    car by going to EndState
    '''
    def __init__(self, bot):
        self.bot = bot

    def on_event(self, event):
        if event == 'm_sensor':
            return ForwardState(self.bot)
        if event == 'button_pressed':
            return EndState(self.bot)
        if event == 'no_sensor' and self.bot.destination == Destination.STOP:
            return EndState(self.bot)
        elif event == 'no_sensor':
            return ForwardState(self.bot)
        return self

    def run(self):
        '''
        Check the current Destination of the Bot and execute accordingly
        '''
        if self.bot.destination == Destination.STOP:
            self.bot.motor.go_forward()
        elif self.bot.destination == Destination.STARBUCKS:
            self.bot.motor.turn_left()
            self.bot.destination = Destination.END
        elif self.bot.destination == Destination.SCIENCE:
            self.bot.motor.turn_right()
            self.bot.destination = Destination.END
        elif self.bot.destination == Destination.APPLE:
            self.bot.motor.turn_ahead()
            self.bot.destination = Destination.END
        elif self.bot.destination == Destination.END:
            self.bot.destination = Destination.STOP


class EndState(State):
    '''
    End state of the bot. We contact the server that the order has been completed
    (or cancelled) and go back to ReceivingState to wait for a new order
    '''
    def __init__(self, bot):
        self.bot = bot

    def on_event(self, event):
        return self

    def run(self):
        # Tell the server we're done with this order by going to the url
        self.bot.destination = Destination.STOP

        try:
            with urllib.request.urlopen(c.DELIVERED_URL) as url:
                pass
        except urllib.error.URLError as e:
            print(e.reason)

        # Force state change back to receiving a new order after we told the server we are done
        self.bot.state = ReceivingState(self.bot)


class Bot():
    '''
    Main class of the program. Handles all the functions of the car.
    This class runs through the programs main logic every program tick. 
    It:
        - Runs the logic of the current state (the states handle the wheels)
        - Adjusts the leds based on current state
        - Reads if the button is pressed
        - Asks the server if any new orders are available
        - Adjusts the state depending on the data read from the sensors

    '''
    def __init__(self):
        '''
        Create all the different objects the bot uses.
            - motor: MotorController class which controls both wheels
            - sens: Sensor class which reads the sensor data and returns an INPUT
            - btn: Button class to read the button data
            - led: LedController to work with the front and side leds
            - state: State the program is currently in, constantly changes
            - destination. Destination Enumeration to represent the bots current goal
        '''
        self.motor = MotorController()
        self.sens = Sensor(c.PINS_SENSOR)
        self.btn = Button(c.PIN_BUTTON)
        self.led = LedController()
        self.state = IdleState(self)
        self.destination = Destination.STOP

    def get_destination(self):
        '''
        Make contact with the server to see if new deliveries are available

        If a new delivery is found we change the destination of the bot.
        '''
        order_data = None

        # Contact webserver
        try:
            with urllib.request.urlopen(c.DELIVERY_URL) as url:
                order_data = json.loads(url.read().decode())
        except urllib.error.URLError as e:
            print(e.reason)

        # If new delivery is found change destination
        if order_data is not None and order_data['order'] == 'true':
            if order_data['location'] == 'Starbucks':
                print("Received Starbucks location")
                return Destination.STARBUCKS
            if order_data['location'] == 'Science Center':
                print("Received Science Center location")
                return Destination.SCIENCE
            if order_data['location'] == 'Apple Center':
                print("Received Apple Center location")
                return Destination.APPLE
        else:
            return Destination.STOP

    def tick(self):
        '''
        Main logic of the program that gets looped through every tick
        '''
        # First execute the current state
        self.state.run()

        # Read the current sensor data
        sens_input = self.sens.sensor_input

        # Reset leds every tick
        self.led.turn_off_side_leds()

        # Led Control for turn signals
        if isinstance(self.state, ReceivingState):
            self.led.turn_on_left_led()
            self.led.turn_on_right_led()

        if isinstance(self.state, IntersectionState) and self.destination == Destination.APPLE:
            self.led.turn_on_left_led()
            self.led.turn_on_right_led()

        if isinstance(self.state, RightState) or (isinstance(self.state, IntersectionState) and self.destination == Destination.STARBUCKS):
            self.led.turn_on_right_led()

        if isinstance(self.state, LeftState) or (isinstance(self.state, IntersectionState) and self.destination == Destination.SCIENCE):
            self.led.turn_on_left_led()

        # Progress front facing leds 1 tick
        self.led.forward_led_tick()

        # First check the button value, acts as interrupt for sensor
        # Always makes the state go to EndState which interrupts the order
        # And goes back to ReceiveState after to start a new order
        if self.btn.value == 1:
            self.state = self.state.on_event('button_pressed')
            # Sleep half a second to make sure the button isn't pressed multiple times
            time.sleep(0.5)

        # If we need to check for new deliveries, we do that first.
        # Check for deliveries if Destination is in STOP and we're in ReceivingState
        # No need to waste time contacting the server otherwise
        if self.destination == Destination.STOP and isinstance(self.state, ReceivingState):
            self.destination = self.get_destination()
            if self.destination != Destination.STOP:
                self.state = self.state.on_event('new_delivery')

        # Check sensor data and set right event
        if sens_input == Input.RIGHT:
            self.state = self.state.on_event('r_sensor')
        elif sens_input == Input.LEFT:
            self.state = self.state.on_event('l_sensor')
        elif sens_input == Input.MIDDLE:
            self.state = self.state.on_event('m_sensor')
        elif sens_input == Input.INTERSECTION:
            self.state = self.state.on_event('intersection')
        elif sens_input == Input.NO_SENSOR:
            self.state = self.state.on_event('no_sensor')

        
        # Print the class we're currently in to console
        print(self.state.__repr__())
