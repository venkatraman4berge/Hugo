#!/usr/bin/env python3

from __future__ import print_function

import odrive
from odrive.enums import *
import time
import math

# Find a connected ODrive (this will block until you connect one)
print("finding an odrive...")
my_drive = odrive.find_any()

# Find an ODrive that is connected on the serial port /dev/ttyUSB0
#my_drive = odrive.find_any("serial:/dev/ttyUSB0")

# Calibrate motor and wait for it to finish
if (not my_drive.axis0.encoder.is_ready) or (not my_drive.axis0.motor.is_calibrated):
	print("starting calibration...")
	my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
	while my_drive.axis0.current_state != AXIS_STATE_IDLE:
	    time.sleep(0.1)
	my_drive.axis0.requested_state = AXIS_STATE_ENCODER_INDEX_SEARCH
	while my_drive.axis0.current_state != AXIS_STATE_IDLE:
	    time.sleep(0.1)
	my_drive.axis0.requested_state = AXIS_STATE_ENCODER_OFFSET_CALIBRATION
	while my_drive.axis0.current_state != AXIS_STATE_IDLE:
	    time.sleep(0.1)
	my_drive.save_configuration()
	my_drive.reboot()
my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")
my_drive.axis0.controller.config.control_mode = CTRL_MODE_VELOCITY_CONTROL
my_drive.axis0.controller.config.vel_ramp_rate = 5000
my_drive.axis0.controller.vel_ramp_enable = True

while True:
    setpoint = 20000
    print("Set Point " + str(int(setpoint)))
    my_drive.axis0.controller.vel_ramp_target = setpoint 
    time.sleep(5)
    my_drive.axis0.controller.vel_ramp_target = 0 
    time.sleep(5)
    my_drive.axis0.controller.vel_ramp_target = (-1*setpoint)
    time.sleep(5)
    my_drive.axis0.controller.vel_ramp_target = 0 
    time.sleep(5)

