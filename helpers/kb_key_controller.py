"""
This module provides a KeyboardKeyController class that you can use 
to send commands to the robot using the keyboard.
"""

import sys
import termios
import atexit
from select import select


class KeyboardKeyController:
    """
    This class provides a KeyboardKeyController object that you can use
    to send commands to the robot using the keyboard.
    """

    def __init__(self):
        """Creates a KeyboardKeyController object that you can call to send commands to the robot."""
        # Save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        # New terminal setting unbuffered
        self.new_term[3] = self.new_term[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)

    def set_normal_term(self):
        """Resets to normal terminal.  On Windows this is a no-op."""
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.old_term)

    def get_command(self):
        """Returns a command when an arrow key or space bar is pressed. Returns None if no key is pressed.
        0 : up
        1 : right
        2 : down
        3 : left
        4 : space bar
        5 : a, rotate camera left
        6 : d, rotate camera right
        7 : w, tilt camera up by 10 degrees
        8 : s, tilt camera down by 10 degrees
        9 : x, set camera straight
        10, q, rotate the camer left by 10 degrees
        11, e, rotate the camera right by 10 degrees
        12, z, open camera
        13, c, close camera
        """
        c = sys.stdin.read(1)
        if c == " ":
            return 4  # space bar
        elif c == "a" or c == "A":
            return 5
        elif c == "d" or c == "D":
            return 6
        elif c == "w" or c == "W":
            return 7
        elif c == "s" or c == "S":
            return 8
        elif c == "x" or c == "X":
            return 9
        elif c == "q" or c == "Q":
            return 10
        elif c == "e" or c == "E":
            return 11
        elif c == "z" or c == "Z":
            return 12
        elif c == "c" or c == "C":
            return 13
        elif c == "\x1b":
            c = sys.stdin.read(2)
            if c[0] == "[":
                vals = [65, 67, 66, 68]
                return vals.index(ord(c[1]))
        return None

    def block_until_key_pressed(self):
        """Returns True if keyboard character was hit, False otherwise."""
        dr, _, _ = select([sys.stdin], [], [], 0)
        return dr != []
