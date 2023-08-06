"""A module for utility functions. """

from time import sleep

from pydirectinput import keyDown, keyUp


def press_key(key, interval: float = 0.15):
    """Presses a key for a given interval of time. """
    keyDown(key)
    sleep(interval)
    keyUp(key)
