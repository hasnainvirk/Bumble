import RPi.GPIO as GPIO
from components.remote_control.modules.buttons import (
    ButtonControls as button_ctrls,
    button_key_codes,
)
import logging, time, threading


GPIO_15 = 15
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

"""
An IR receiver recognizes its remote control or transmitter through a series of encoded signals that are transmitted by the remote and decoded by the receiver. Here's a step-by-step explanation of how this process works:

1. **Signal Transmission**:
   - The remote control sends out infrared (IR) signals in the form of modulated light pulses. These pulses are typically modulated at a specific frequency (e.g., 38 kHz) to distinguish them from ambient IR light.

2. **Modulation and Encoding**:
   - The data to be transmitted (e.g., button press information) is encoded using a specific protocol (e.g., NEC, Sony, RC5). This encoding involves converting the data into a series of pulses and spaces (on and off periods) that represent binary data.

3. **Reception**:
   - The IR receiver module detects the modulated IR light pulses and demodulates them to retrieve the encoded data. The demodulation process filters out the carrier frequency, leaving the original binary data.

4. **Decoding**:
   - The microcontroller or processor connected to the IR receiver decodes the binary data according to the specific protocol used by the remote control. This involves interpreting the timing of the pulses and spaces to reconstruct the original data.

5. **Recognition**:
   - The decoded data typically includes an address or identifier that specifies the intended receiver. The microcontroller compares this address with its own address to determine if the signal is meant for it. If the addresses match, the microcontroller processes the command; otherwise, it ignores the signal.

In the provided code snippet, the process of recognizing and decoding the IR signal is implemented as follows:

1. **Initial Detection**:
   - The code waits for a LOW signal on the GPIO pin, indicating the start of an IR transmission.
   - It then waits for a 9ms LOW level boot code and a 4.5ms HIGH level boot code, which are part of the NEC protocol's preamble.

2. **Data Reception**:
   - The code enters a loop to receive 32 bits of data. Each bit consists of a LOW period followed by a HIGH period.
   - The duration of the HIGH period determines whether the bit is a '0' or a '1'.

3. **Bit Decoding**:
   - For each bit, the code measures the duration of the LOW and HIGH periods.
   - If the HIGH period is longer than a certain threshold, it is interpreted as a '1'; otherwise, it is a '0'.

4. **Data Storage**:
   - The received bits are stored in an array, which represents the complete command sent by the remote control.

Here is a simplified version of how the code works:

This code waits for the specific timing of the IR signal to decode the transmitted data, which allows the IR receiver to recognize and respond to its remote control.
"""


class InfraredReceiver:

    def __init__(self, ctrls: button_ctrls):
        self.log = logging.getLogger("bumble")
        self.pin = GPIO_15
        self.data = [0, 0, 0, 0]
        self.ctrls = ctrls
        self.lock = threading.Lock()
        self.__setup()

    def start(self):
        # Start the infrared receiver in a separate thread
        self.thread = threading.Thread(
            target=self.__run,
            name="IR Receiver",
        )
        self.thread.daemon = False
        self.thread.start()

    def shutdown(self):
        # remove the interrupt
        GPIO.remove_event_detect(self.pin)
        GPIO.cleanup()
        self.thread.join()

    def __run(self):
        # Set up an interrupt to detect the signal
        try:
            GPIO.add_event_detect(
                self.pin, GPIO.FALLING, callback=self.__handle_interrupt
            )
        except RuntimeError as e:
            self.log.error(f"Failed to add edge detection: {e}")
            GPIO.cleanup()

    def __handle_interrupt(self, channel):
        self.lock.acquire()
        if GPIO.input(channel) == 0:
            self.__recv_preamble()
            self.__recv_data()
            if self.__verify_data():
                data = self.data[2]
                self.log.debug(f"Received data: {data}")
                for command in button_key_codes:
                    if button_key_codes[command] == data:
                        self.log.debug(f"calling button controller: {command}")
                        self.ctrls[command]["action"]()  # calls the callable object
                        break
        self.lock.release()

    def __recv_preamble(self):
        count = 0
        while (
            GPIO.input(self.pin) == 0 and count < 200
        ):  # Wait for 9ms LOW level boot code and exit the loop if it exceeds 12ms
            count += 1
            time.sleep(SIXTY_MICROSECONDS_IN_SECONDS)

        count = 0
        while (
            GPIO.input(self.pin) == 1 and count < 80
        ):  # Wait for a 4.5ms HIGH level boot code and exit the loop if it exceeds 4.8ms
            count += 1
            time.sleep(SIXTY_MICROSECONDS_IN_SECONDS)

    def __recv_data(self):
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

    def __verify_data(self) -> bool:
        # Verify the data received
        if self.data[0] + self.data[1] == 0xFF and self.data[2] + self.data[3] == 0xFF:
            self.log.debug(f"Address Byte: {self.data[0]}")
            self.log.debug(f"Address Inverse Byte: {self.data[1]}")
            self.log.debug(f"Command Byte: {self.data[2]}")
            self.log.debug(f"Command Inverse Byte: {self.data[3]}")
            return True
        else:
            self.log.error("Malformed data received from IR transmitter")
            return False

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, GPIO.PUD_UP)
        time.sleep(0.1)  # Add a small delay to ensure setup is complete
