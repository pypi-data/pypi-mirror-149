"""
    The main module for the Everest ride automation project.
    
    KEYBOARD COMMANDS
    -----------------
    's' - E-Stop
    'r' - Reset E-Stop
    
    'right arrow' - Open Gates
    'left arrow' - Close Gates
    
    'up arrow' - Unlock Restraints
    'down arrow' - Lock & Check Restraints
    
    'space' - Dispatch
    
    'f' - Fast Lane Passengers
    'l' - Main Queue Passengers
"""
import sys
from time import sleep

from ridesims.utils import press_key


def loading_unloading_procedure():
    """The procedure and flow necessary to load and unload passengers. """
    # Open the gates:
    print("Gates opening. Waiting... ")
    press_key('right', interval=2)
    # Wait for passengers to load:
    sleep(7.5)

    # Close gates, then short pause:
    print("Gates closing. Waiting... ")
    press_key('left', interval=2)
    sleep(2.5)

    # Close + check restraints:
    print("Restraints locked/unlocking. Waiting... ")
    press_key('down', interval=2)
    sleep(1.5)

    # Release the restraints in Unload Staion:
    press_key('up', interval=2)
    # Wait for passengers to unload & restraints check to complete:
    sleep(16)

    # Dispatch loaded train:
    print("Dispatching loaded train. Waiting... ")
    press_key('space', interval=5.5)
    # Wait for train to exit:
    sleep(10) # maybe 6-7

    # Dispatch unloaded train:
    print("Dispatching unloaded train. Waiting... ")
    press_key('space', interval=5.5)
    # Pause before next run through:
    sleep(12)


def run_automated():
    """Runs automated interactions with the keyboard and mouse. """
    try:
        count = 0
        for i in range(10):
            print(f"STARTING IN {10-i} SECONDS...")
            sleep(1.25)
        # Run on infinite loop:
        while True:
            count += 1
            print(f"This is RUN #{count} ")
            loading_unloading_procedure()

    except KeyboardInterrupt:
        print("AUTOMATED SESSION HAS ENDED! ")
        return

    except Exception as e:
        print(e)
        sys.exit(1)
