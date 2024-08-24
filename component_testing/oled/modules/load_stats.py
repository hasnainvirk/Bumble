from component_testing.oled.modules.oled import Oled
from PIL import Image, ImageDraw, ImageFont

import subprocess
import time


class Stats(Oled):

    def __init__(self):
        super().__init__()

    def load_stats(self):
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        top = padding
        bottom = self.disp.height - padding
        # Move left to right keeping track of the current x position for drawing shapes.
        x = 0

        while True:
            # Draw a black filled box to clear the image.
            self.draw.rectangle(
                (0, 0, self.disp.width, self.disp.height), outline=0, fill=0
            )

            # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
            cmd = "hostname -I | cut -d' ' -f1"
            ip = subprocess.check_output(cmd, shell=True)
            cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
            cpu = subprocess.check_output(cmd, shell=True)
            cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
            mem_usage = subprocess.check_output(cmd, shell=True)
            cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%dGB %s", $3,$2,$5}\''
            disk = subprocess.check_output(cmd, shell=True)

            # Write two lines of text.
            self.draw.text((x, top), "IP: " + str(ip), font=self.font, fill=255)
            self.draw.text((x, top + 8), str(cpu), font=self.font, fill=255)
            self.draw.text((x, top + 16), str(mem_usage), font=self.font, fill=255)
            self.draw.text((x, top + 25), str(disk), font=self.font, fill=255)

            # Display image.
            self.disp.image(self.image)
            self.disp.show()
            time.sleep(0.5)
