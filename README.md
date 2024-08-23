# Bumble

Base OS Build

1. Raspberry Pi Imager for Mac OS - https://www.raspberrypi.com/software/
2. Virtual Desktop for Mac OS to connect to Raspberry PI - https://www.realvnc.com/en/connect/download/viewer/
3. Raspberry PI OS (Bookworm 64-bit) - Installing Desktop version for starters, may change to headless later on
4. Customisation notes :
   1. Username: ######
   2. Password: ######
   3. local DNS address: #####.local
   4. Connected to ###### SSID
   5. An SSH key also set (####)

## Booting Bumble for first time

1. Power up with USB C.
2. SSH into raspberry pi and update packages

```sh
$ ssh <username>@<hostname>.local
$ sudo apt update
$ sudo apt upgrade
```

3. Installing and enabling VNC Server on Raspberry PI for remote desktop viewing

```sh
$ sudo apt install realvnc-vnc-server realvnc-vnc-viewer
```

4. Interface Configuration for VNC. From Raspi Configuration window, select and enable VNC.

```sh
$ sudo raspi-config
```

5. Setup virtual python environment

```sh
$ sudo apt install virtualenvwrapper
$ mkdir .virtualenvs

# if having difficulties locating the folder where virtualenvwrapper was installed
$ cd /
$ sudo find -iname "virtualenvwrapper.sh"

# Add the following to .bashrc
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/bin/virtualenv
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh

# create virtualenv
$ mkvirtualenv bumble
```

6. Setup python bindings for Raspberry PI GPIO

```sh
# Inside bumble virtual env
$ pip install RPi.gpio
```

## Development Platform Setup

1. Python virtual environment setup

```sh
$ pyenv shell 3.12.4
$ pyenv virtualenvwrapper
$ mkvirtualenv bumble
```

2. Installing Mock Raspberry PI GPIO library

```sh
pip install Mock.GPIO
```

## Testing Components

### OLED Panel

- 0.96 inch OLD module driven by I2C (Chip SSD1306)
- Resolution: 124x64 pixels
- Code Reference: https://github.com/adafruit/Adafruit_CircuitPython_SSD1306

```sh
#Installing SSD1306 driver library
$ pip install adafruit-circuitpython-ssd1306
```
