from component_testing.oled.modules.oled import Oled, RESOURCES_FOLDER
from PIL import ImageFont

import subprocess
import time
import os
import logging


class Stats(Oled):

    def __init__(self):
        super().__init__()
        self.log = logging.getLogger("bumble")

    def load_stats(self):
        # First define some constants to allow easy resizing of shapes.
        padding = -2
        top = padding
        # Move left to right keeping track of the current x position for drawing shapes.
        x = 0

        # Load default font.
        font_path = os.path.join(
            os.path.dirname(__file__), RESOURCES_FOLDER, "Minecraftia-Regular.ttf"
        )
        self.font = ImageFont.truetype(font_path, 8)

        while True:
            # Draw a black filled box to clear the image.
            self.draw.rectangle(
                (0, 0, self.disp.width, self.disp.height), outline=0, fill=0
            )

            try:
                # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
                cmd = "hostname -I | cut -d' ' -f1"
                ip = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
            except subprocess.CalledProcessError as e:
                ip = "N/A"
                self.log.error(f"Error getting IP: {e}")

            try:
                cmd = (
                    "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
                )
                cpu = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
                cpu = cpu.replace("CPU Load: ", "")
            except subprocess.CalledProcessError as e:
                cpu = "N/A"
                self.log.error(f"Error getting CPU load: {e}")

            try:
                cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
                mem_usage = (
                    subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
                )
                mem_usage = mem_usage.replace("Mem: ", "")
            except subprocess.CalledProcessError as e:
                mem_usage = "N/A"
                self.log.error(f"Error getting memory usage: {e}")

            try:
                cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%dGB %s", $3,$2,$5}\''
                disk = subprocess.check_output(cmd, shell=True).decode("utf-8").strip()
                disk = disk.replace("Disk: ", "")
            except subprocess.CalledProcessError as e:
                disk = "N/A"
                self.log.error(f"Error getting disk usage: {e}")

            try:
                self.draw.text((x, top), "IP: ", font=self.font, fill=255)
                ip_width, _ = self.draw.textsize("IP: ", font=self.font)
                self.draw.text((x + ip_width, top), str(ip), font=self.font, fill=1)

                self.draw.text((x, top + 16), "CPU Load: ", font=self.font, fill=255)
                cpu_width, _ = self.draw.textsize("CPU Load: ", font=self.font)
                self.draw.text(
                    (x + cpu_width, top + 16), str(cpu), font=self.font, fill=1
                )

                self.draw.text((x, top + 31), "RAM: ", font=self.font, fill=255)
                ram_width, _ = self.draw.textsize("RAM: ", font=self.font)
                self.draw.text(
                    (x + ram_width, top + 31), str(mem_usage), font=self.font, fill=1
                )

                self.draw.text((x, top + 46), "DISK: ", font=self.font, fill=255)
                disk_width, _ = self.draw.textsize("DISK: ", font=self.font)
                self.draw.text(
                    (x + disk_width, top + 46), str(disk), font=self.font, fill=1
                )

                # Display image.
                self.disp.image(self.image)
                self.disp.show()
            except Exception as e:
                self.log.error(f"Error displaying stats: {e}")

            time.sleep(0.5)
