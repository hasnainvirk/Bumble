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
# select I3 VNC
```

5. Enable I2C on raspberry pi so that we can use I2C interface for our peripherals, e.g., the OLED module.

```sh
$ sudo raspi-config
# selct I5 I2C
```

6. Setup virtual python environment

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

## Bumble CLI - Command Line Interface

A command line interface is integrated in the code base for components testing on the Raspberry PI. To deploy the code base and install the binary as a CLI interface, follow the instructions below.

### Deploying the code on Raspberry PI

1. Clone the repository on your development platform.

```sh
$ git clone https://github.com/hasnainvirk/Bumble.git
```

2. Deploy code base and install bumble CLI using script.

```sh
# from the root of your repo, make sure script is executable
$ chomod +x deploy.sh
$ ./deploy.sh
```

The script SSHs into raspberry PI, clones the git repo, and installss the CLI binary. It then runs a command `$ bumble --help` which shows the help page for CLI.

More detailed help can be checked, e.g.,

```sh
$ bumble oled --help
Usage: bumble oled [OPTIONS]

Options:
  -text                     Loads text on the OLED screen
  -image TEXT               Loads an image on OLED screen. The image should be
                            in resources folder, e.g. $bumble oled --image
                            grumpy_cat.jpg
  -emoji [happy|sad|angry]  Loads an emoji the OLED screen, e.g. $bumble oled
                            --emoji happy
  -stats                    Loads usage states on the OLED screen
  -v                        Verbosity level default=error, v=info, vv=debug
  --help                    Show this message and exit.
```

## Testing Components

### OLED Panel

- 0.96 inch OLD module driven by I2C (Chip SSD1306)
- Resolution: 124x64 pixels
- Code Reference: https://github.com/adafruit/Adafruit_CircuitPython_SSD1306

```sh
#Installing SSD1306 driver library dependency
$ pip install adafruit-circuitpython-ssd1306
```

#### Testing Text

OLED screen shows example text in 4 rows.

```sh
$ bumble oled -text
```

#### Testing Image

OLED screen shows 1-pixel converted image of an image that is placed in `./components/oled/modules/resources`, e.g.,

```sh
$ bumble oled -image grumpy_cat.jpg
```

#### Testing Emoji

OLED screen shows an animated happy emoji, e.g.,

```sh
$ bumble oled -emoji happy
```

Other options are `sad` and `angry`

#### Testing Stats

OLED screen shows utilization statistics of CPU. RAM and Disk, e.g.,

```sh
$ bumble oled -stats
```

## Wheels

The motors that move the wheels are connected to TB6612 motor driving chips. There are two of these chips located on the control shield that sits on top of the Raspberry PI. Here are the schematics:

![architecture](img/motor_schematics.png)

| Wheel      | Motor name on schematics | Motor name on the board | R.PI GPIO PIN & Pull                    | Direction | speed (PWM) |
| ---------- | ------------------------ | ----------------------- | --------------------------------------- | --------- | ----------- |
| UpperLeft  | M1A                      | M2                      | GPIO_20 pulled Low, GPIO_21 pulled High | forward   | GPIO_0      |
| LowerLeft  | M1B                      | M1                      | GPIO_22 pulled High, GPIO_23 pulled Low | forward   | GPIO_1      |
| UpperRight | M2A                      | M3                      | GPIO_24 pulled High, GPIO_25 pulled Low | forward   | GPIO_12     |
| LowerRight | M2B                      | M4                      | GPIO_26 pulled Low, GPIO_27 pulled High | forward   | GPIO_13     |

### Testing wheels individually

1. Check CLI help.

```sh
$ bumble wheel --help
```

2. For example, move `upper_left` wheel forward

```sh
$ bumble wheel -forward upper_left
```

3. Similarly, move `lower_right` wheel backwards

```sh
$ bumble wheel -backward lower_right
```

## Drive System

For example,

- Drive forward

```sh
$ bumble -drive forward
```

- Drive backward

```sh
$ bumble -drive backward
```

- Turn right

```sh
$ bumble -drive right
```

- Turn left

```sh
$ bumble -drive left
```

## LED Panel

The LED panel a dot matrix of 16x8 pixels. Use this https://dotmatrixtool.com/# tool to create a pattern and get the matrix values out which can be stored in `./components/led_panel/modules/shapes.py`

```sh
$ bumble led --help
$ bumble led -bob
$ bumble led -smile
```

## Line Tracking Sensor

The principal behind this sensor is to emit infra red radiation and then collect it back to make a decision matrix across three GPIO IN pins.

| L (left) | M (middle) | R (right) | Decision             |
| -------- | ---------- | --------- | -------------------- |
| GPIO_19  | GPIO_18    | GPIO_17   | forward, right, left |
| 1        | 0          | 0         | lef                  |
| 0        | 0          | 1         | right                |
| 0        | 1          | 0         | forward              |

In every other case the robot should stop and reevaluate the situation.

```sh
$ bumble lts
```

## Ultrasonic Sensor

The ultrasonic sensor is used to measure the distance to an object by emitting ultrasonic waves and measuring the time it takes for the echo to return. This sensor can be used for obstacle detection and avoidance.

| Pin  | Description    | Connection |
| ---- | -------------- | ---------- |
| VCC  | Power supply   | 5V         |
| GND  | Ground         | GND        |
| TRIG | Trigger signal | GPIO_14    |
| ECHO | Echo signal    | GPIO_4     |

You can also interact with the ultrasonic sensor using the command line interface.

```sh
$ bumble ultrasonic -vvv
 INFO     | Running Ultrasonic Sensor test
 DEBUG    | Measured Distance @ Sensor = 189.54 cm
 DEBUG    | Measured Distance @ UltrasonicSensorTest = 189.54 cm
```

## Servo for ultrasonic sensor

This servo motor makes the ultrasonic sensor move on a base plate from 0 to 180 degrees.

```sh
$ bumble servo --help
Usage: bumble servo [OPTIONS]

Options:
  -ultrasonic                   Selects Ultrasonic Sensor Servo
  -camera                       Selects Camera Servos
  -point [straight|right|left]  Makes the Servo point in the given direction
  -rotate [center|right|left]   Makes the Servo rotate in the given direction
  -tilt [close|open]            Makes the camera servo open or shut the camera
                                module
  -v                            Verbosity level default=error, v=info,
                                vv=debug
  --help                        Show this message and exit.

```

**NOTE** Use only `rotate` and `point` with `-ultrasonic` option. `-tilt` can be used with camera servo only

For example pointing the base plate straight (90 degrees),

```sh
$ bumble servo -ultrasonic -point straight -vvv
 INFO     | Running Ultrasonic Sensor Servo test
 DEBUG    | Ultrasonic Servo - Point straight
```

Or rotating the base plate all the way to right (0 degree) step by step,

```sh
$ bumble servo -ultrasonic -rotate right -vvv
 INFO     | Running Ultrasonic Sensor Servo test
 DEBUG    | Ultrasonic Servo - Point straight
 DEBUG    | Ultrasonic Servo - Rotating Right

```

## Servos for Camera

There are two servos attached to Camera module.

1. Base plate servo - helps the camera move from 0 to 180 degrees. This allows the camera to rotate from right to left.
2. Camera tilt servo - helps the camera to tilt back down to close the module ot tilt back up to open it up.

### Testing the camera servos

```sh
$ bumble servo -camera -rotate right -vvv
 INFO     | Running Camera Servo test
 DEBUG    | Camera Servo - Rotating Right
```

```sh
$ bumble servo -camera -point straight -vvv
 INFO     | Running Camera Servo test
 DEBUG    | Camera Servo - Point straight
```

```sh
$ bumble servo -camera -tilt close -vvv
 INFO     | Running Camera Servo test
 DEBUG    | Camera Servo - Closing Camera
```

```sh
$ bumble servo -camera -tilt open -vvv
 INFO     | Running Camera Servo test
 DEBUG    | Camera Servo - Opening Camera
```

## Infrared Receiver - Remote Control

The IR chip uses NEC IR protocol. The controllign GPIO pin `GPIO_15=15` is connected to high voltage (3.3v) through an internal resistor, ensuring that the pin reads as high (1) when it is not connected to anything else.

### NEC Protocol

| Timing | Byte            | Pin Pull  |
| ------ | --------------- | --------- |
| 9ms    | Preamble        | Low       |
| 4.5ms  | None            | High      |
| 13.5ms | Address         | High, Low |
| 13.5ms | Address Inverse | High, Low |
| 13.5ms | Command         | High, Low |
| 13.5ms | Command Inverse | High, Low |

NEC protocol uses pulse distance encoding of the bits. The data is sent in the form of a series of pulses.
Each pulse is a 562.5µs long 38kHz carrier burst.

Signal will be high for 562.5µs and low for 562.5µs for a logical "0". It takes 1.125ms to transmit a 0.

Signal will be high for 562.5µs and low for 1.6875ms for a logical "1". It takes 2.25ms to transmit a 1.

### Testing Remote Control

When pressed "2" on the remote control after executing the test sequence.

```sh
$ bumble remote -vvv
 INFO     | Running Remote Control test
 DEBUG    | Address Byte: 0
 DEBUG    | Address Inverse Byte: 255
 DEBUG    | Command Byte: 25
 DEBUG    | Command Inverse Byte: 230
 DEBUG    | Received data: 25
 DEBUG    | calling button controller: two
 INFO     | two

```

## Manually Driving the Robot with Collision Avoidance

You can control the robot with Arrow Keys and Space Bar.

- Arrow Keys -> Direction
- Space Bar -> Brake

## Setup on Raspberry PI

1. Install dependencies.
2. Start the manual drive program:
   ```sh
   $ python main.py -vvvv
   ```

## Setup on a different machine

1. Install dependecies
2. Start the client program
   ```sh
   $ python ~/Bumble/helpers/kb_controller_client.py
   ```
