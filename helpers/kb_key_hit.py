#!/usr/bin/env python
"""
A Python class implementing KBHIT, the standard keyboard-interrupt poller.
Works transparently on Windows and Posix (Linux, Mac OS X).  Doesn't work
with IDLE.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

"""

import os
import sys
import termios
import atexit
from select import select


class KBHit:

    def __init__(self):
        """Creates a KBHit object that you can call to do various keyboard things."""
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

    def getch(self):
        """Returns a keyboard character after kbhit() has been called.
        Should not be called in the same program as getarrow().
        """
        return sys.stdin.read(1)

    def getarrow(self):
        """Returns an arrow-key code after kbhit() has been called. Codes are
        0 : up
        1 : right
        2 : down
        3 : left
        Should not be called in the same program as getch().
        """
        c = sys.stdin.read(1)
        if c == " ":
            return 4  # space bar
        elif c == "\x1b":
            # c = sys.stdin.read(3)[2]
            c = sys.stdin.read(2)
            if c[0] == "[":
                vals = [65, 67, 66, 68]
                return vals.index(ord(c[1]))
                # return vals.index(ord(c.encode("utf-8")))
        return None

    def kbhit(self):
        """Returns True if keyboard character was hit, False otherwise."""
        dr, dw, de = select([sys.stdin], [], [], 0)
        return dr != []
