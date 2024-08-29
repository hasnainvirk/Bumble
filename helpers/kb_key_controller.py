import sys
import termios
import atexit
from select import select


class KeyboardKeyController:

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
        """
        c = sys.stdin.read(1)
        if c == " ":
            return 4  # space bar
        elif c == "\x1b":
            c = sys.stdin.read(2)
            if c[0] == "[":
                vals = [65, 67, 66, 68]
                return vals.index(ord(c[1]))
        return None

    def block_until_key_pressed(self):
        """Returns True if keyboard character was hit, False otherwise."""
        dr, dw, de = select([sys.stdin], [], [], 0)
        return dr != []
