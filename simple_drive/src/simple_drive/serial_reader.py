#!/usr/bin/env python

import roslib
import rospy
import subprocess
import serial
from sensor_msgs.msg import Joy

L_JOY_X = "0"
L_JOY_Y = "1"
R_JOY_X = "2"
R_JOY_Y = "3"
L1 = "4"
L2 = "5"
L3 = "6"
R1 = "7"
R2 = "8"
R3 = "9"
UP = "10"
DOWN = "11"
LEFT = "12"
RIGHT = "13"
START = "14"
BACK = "15"
X_BOX = "16"
SYNC = "17"
A = "18"
B = "19"
X = "20"
Y = "21"


class SerialReader:
    """Class for reading serial port."""

    def __init__(self):
        """Init."""
        self.ser = serial.Serial('/dev/ttyACM0', 9600)
        self.serial_reader_pub = rospy.Publisher('serial_reader',Joy, queue_size=10)

        # Dictionary containing responsefunctions for different commands
        self.command_dict = {
            L_JOY_X: self.on_l_joy_x,
            L_JOY_Y: self.on_l_joy_y,
            R_JOY_X: self.on_r_joy_x,
            R_JOY_Y: self.on_r_joy_y,
            L1: self.on_L1,
            L2: self.on_L2,
            L3: self.on_L3,
            R1: self.on_R1,
            R2: self.on_R2,
            R3: self.on_R3,
            UP: self.on_up,
            DOWN: self.on_down,
            LEFT: self.on_left,
            RIGHT: self.on_right,
            START: self.on_start,
            BACK: self.on_back,
            X_BOX: self.on_x_box,
            SYNC: self.on_sync,
            A: self.on_a,
            B: self.on_b,
            X: self.on_x,
            Y: self.on_y,
        }

    def log(self):
        """Debug logger."""
        if(self.data is not None):
            print(str(self.command) + " : " + str(self.data))
        else:
            print(str(self.command))

    def on_l_joy_x(self):
        """Run when left joystick x value is received."""
        self.log()

    def on_l_joy_y(self):
        """Run when left joystick y value is received."""
        self.log()

    def on_r_joy_x(self):
        """Run when right joystick x value is received."""
        self.log()

    def on_r_joy_y(self):
        """Run when right joystick y value is received."""
        self.log()

    def on_L1(self):
        """Run when L1 is pressed."""
        self.log()

    def on_L2(self):
        """Run when L2 value is received."""
        self.log()

    def on_L3(self):
        """Run when L3 is pressed."""
        self.log()

    def on_R1(self):
        """Run when R1 is pressed."""
        self.log()

    def on_R2(self):
        """Run when R2 value is received."""
        self.log()

    def on_R3(self):
        """Run when R3 is pressed."""
        self.log()

    def on_up(self):
        """Run when up is pressed."""
        self.log()

    def on_down(self):
        """Run when down is pressed."""
        self.log()

    def on_left(self):
        """Run when left is pressed."""
        self.log()

    def on_right(self):
        """Run when right is pressed."""
        self.log()

    def on_start(self):
        """Run when start is pressed."""
        self.log()

    def on_back(self):
        """Run when back is pressed."""
        self.log()

    def on_x_box(self):
        """Run when XBox is pressed."""
        self.log()

    def on_sync(self):
        """Run when sync is pressed."""
        self.log()

    def on_a(self):
        """Run when a is pressed."""
        self.log()

    def on_b(self):
        """Run when b is pressed."""
        self.log()

    def on_x(self):
        """Run when x is pressed."""
        self.log()

    def on_y(self):
        """Run when y is pressed."""
        self.log()

    def run(self):
        """Loop and wait for incoming messsages."""
        self.running = True
        while(self.running):
            line = self.ser.readline()
            if(line != ''):
                self.command = None
                self.data = None
	        #line = line[:-4]
                temp = line.split(":")
		#print(temp)
                if(len(temp) > 1):
                    self.command = temp[0]
                    self.data = temp[1]
                else:
                    self.command = temp[0]
                command = Joy()
                self.serial_reader_pub.publish(command)
		#print(self.command)
                if(self.command is not None):
		    self.command_dict.get(str(self.command), lambda: 'Invalid')()
    def close(self):
        """Close down the listener."""
        self.running = False
        if(self.ser is not None):
            self.ser.close()
            self.ser = None



# Initialize the reader
#serial_reader = SerialReader()
rospy.init_node("SerialReader")
# Start the reader, to stop call .close() function
joystick = SerialReader()
rospy.spin()
