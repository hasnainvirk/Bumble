import RPi.GPIO as GPIO
import time

SIXTY_MICROSECONDS_IN_SECONDS = 0.00006  # apptoximately

"""
NEC Protocol
9ms 0, 4.5ms 1 followed by 4 bytes data
[9ms LOW], [4.5ms HIGH], [Address, Address Inverse (27ms)], [Command, Command Inverse (27ms)]

NEC protocol uses pulse distance encoding of the bits. The data is sent in the form of a series of pulses.
Each pulse is a 562.5µs long 38kHz carrier burst (about 21 cycles). A logical "1" takes 2.25ms to transmit, 
while a logical "0" is only half of that, being 1.125ms.

Signal will be high for 562.5µs and low for 562.5µs for a logical "0".
Signal will be high for 562.5µs and low for 1.6875ms for a logical "1".
"""


class InfraredRecvrBase:
    def __init__(self, pin, data):
        self.pin = pin
        self.data = data
        self.__setup()

    def recv_preamble(self):
        count = 0
        while (
            GPIO.input(self.pin) == 0 and count < 160
        ):  # Wait for 9ms LOW level boot code and exit the loop if it exceeds 9.6ms
            count += 1
            time.sleep(SIXTY_MICROSECONDS_IN_SECONDS)

        count = 0
        while (
            GPIO.input(self.pin) == 1 and count < 80
        ):  # Wait for a 4.5ms HIGH level boot code and exit the loop if it exceeds 4.8ms
            count += 1
            time.sleep(SIXTY_MICROSECONDS_IN_SECONDS)

    def recv_data(self):
        index = 0  # variable to keep track of byte count
        bit_pos = 0  # position of the bit within a byte
        self.data = [0, 0, 0, 0]  # reset the data

        for _ in range(0, 32):  # Start receiving 32 bits of data
            # 4 bytes: 1. address, 2. address inverse, 3. command, 4. command inverse
            count = 0
            while GPIO.input(self.pin) == 0 and count < 15:
                # Wait for the LOW level signal of 562.5 microseconds to pass and exit the loop if it exceeds 60x15=900 microseconds
                # 900 microseconds is still less than 1.125 milliseconds which is the duration of a logical '0', so this is fine.
                count += 1
                time.sleep(SIXTY_MICROSECONDS_IN_SECONDS)

            # reset the count as we start to decide the bit value
            count = 0
            while GPIO.input(self.pin) == 1 and count < 40:
                # waits for logical HIGH level to pass and exits the loop if it exceeds 2.4ms (40x60=2400 microseconds). This is slightly more than 2.25ms which is the duration of a logical '1'.
                count += 1
                time.sleep(SIXTY_MICROSECONDS_IN_SECONDS)

            # if count>8, that is equivalent to receiving logical 1
            if count > 8:
                self.data[index] |= 1 << bit_pos

            if bit_pos == 7:  # if 8th bit was received
                bit_pos = 0  # reset bit position for next byte
                index += 1  # set index for next byte
            else:
                bit_pos += 1  # otherwise, move to next bit

    def verify_data(self) -> bool:
        # Verify the data received
        if self.data[0] + self.data[1] == 0xFF and self.data[2] + self.data[3] == 0xFF:
            # self.log.debug(f"Address Byte: {self.data[0]}")
            # self.log.debug(f"Address Inverse Byte: {self.data[1]}")
            # self.log.debug(f"Command Byte: {self.data[2]}")
            # self.log.debug(f"Command Inverse Byte: {self.data[3]}")
            return True
        else:
            # self.log.error("Malformed data received from IR transmitter")
            return False

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, GPIO.PUD_UP)
        time.sleep(0.1)  # Add a small delay to ensure setup is complete
