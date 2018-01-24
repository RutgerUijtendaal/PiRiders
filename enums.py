from enum import IntEnum

class Destination(IntEnum):
    '''
    Enumeration of the different destinations the car can have.
    '''
    STOP = 0
    STARBUCKS = 1
    SCIENCE = 2
    APPLE = 3
    END = 4

class Input(IntEnum):
    '''
    Enumeration of the different inputs the sensor reads
    '''
    RIGHT = 0
    LEFT = 1
    MIDDLE = 2
    INTERSECTION = 3
    NO_SENSOR = 4