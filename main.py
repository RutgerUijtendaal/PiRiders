#!/usr/local/bin/python3

import time

from bot import Bot

import constants as c

if __name__ == "__main__":
    '''
    Entry Point of the program. The main function does very little besides decide
    the timing of the bot.

    We create a new Bot Object from the Bot Class and tell it to execute
    every time the while loop runs. 

    Every tick the bot checks the sensors, executes its state and sees if it has to
    change state.
    '''
    bot = Bot()

    while True:
        bot.tick()
        time.sleep(c.STEP_TIME)
