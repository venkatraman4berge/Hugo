#!/usr/bin/env python
import roslib
import rospy
from std_msgs.msg import String
import serial
import threading
import signal
import os
import sys
import numpy as np
from geometry_msgs.msg import Twist
ser = serial.Serial('/dev/ttyJoystick', 9600, timeout=0.2)
global linear_velocity_output_limit
linear_velocity_output_limit = 2
global angular_velocity_output_limit
angular_velocity_output_limit = 3
global linear_velocity_joystick_max
linear_velocity_joystick_max = 32767
global linear_velocity_joystick_min
linear_velocity_joystick_min = -32766
global angular_velocity_joystick_max
angular_velocity_joystick_max = 32767
global angular_velocity_joystick_min
linear_velocity_joystick_min = -32766
global linear_velocity_joystick
global angular_velocity_joystick
global remote_control # if 0 then it is autonomous, otherwise controller is enabled. To enable controller, press LT or RT buttons
global vel_msg_transmit


def handler(signum, frame):
    print ("Signal handler called with signal", signum)
    print("Serial CLOSE")
    ser.close()  
    sys.exit(0)


def get_serial_data():
 while not rospy.is_shutdown():
   rospy.sleep(0.1)
   global linear_velocity_joystick
   linear_velocity_joystick = 0
   global angular_velocity_joystick
   angular_velocity_joystick = 0
   global remote_control
   remote_control = 0
   data = []	
   try:
     if (ser.inWaiting() > 40):
       print ("Waiting Byte:" + str(ser.inWaiting()))
       data= ser.readline()
   except serial.SerialException as e:
     print("could not read serial", e)

   rospy.loginfo(data)
   if ("</" in data) and ("/>" in data):
      	data = data.replace("</", "")
        data = data.replace("/>", "")
	data = ' '.join(data.split())
	data_splitted = data.split('/')
	if (len(data_splitted) == 18):
		rospy.loginfo(data_splitted)
		try:
			raw_linear_velocity = float(data_splitted[1])
			raw_angular_velocity = float(data_splitted[2]) 
			LT_Button= int(data_splitted[4]) 
			RT_Button= float(data_splitted[5])
			if ((LT_Button >= 750) or  (RT_Button >= 750)): # LT and RT takes value between 0 and 1024.
				remote_control = 1 # if LT or RT pressed, then enable remote control
			linear_velocity_joystick = float((raw_linear_velocity/linear_velocity_joystick_max)*linear_velocity_output_limit) # max linear velocity will be 1
			angular_velocity_joystick = float((raw_angular_velocity/angular_velocity_joystick_max)*angular_velocity_output_limit) # max angular velocity will be 0.5
			if (abs(raw_linear_velocity) < (0.25*linear_velocity_joystick_max)):
				linear_velocity_joystick = 0
			if (abs(raw_angular_velocity) < (0.15*angular_velocity_joystick_max)):
				angular_velocity_joystick = 0
  		except rospy.ROSInterruptException:
    			pass
		except ValueError:
			print ("Serial Port Data Format Error")
	rospy.loginfo("Linear velocity: " + str(linear_velocity_joystick))
	rospy.loginfo("Angular velocity: " + str(angular_velocity_joystick))
	rospy.loginfo("Remote Control Enabled: " + str(remote_control))
   
 print("Exiting serial thread")


def cmd_vel_publisher():
  global vel_msg_transmit
  vel_msg_transmit = Twist()
  pub = rospy.Publisher('/joystick/cmd_vel', Twist, queue_size=10)
  rate = rospy.Rate(10) # 10hz
  global cmdvel_linear_velocity
  global cmdvel_angular_velocity
  global linear_velocity_joystick
  global angular_velocity_joystick
  global remote_control
  while ((not rospy.is_shutdown()) and (remote_control == 1)):
    vel_msg_transmit.linear.x = linear_velocity_joystick
    vel_msg_transmit.angular.z = angular_velocity_joystick
    pub.publish(vel_msg_transmit)
    rate.sleep()


if __name__ == '__main__':
  signal.signal(signal.SIGINT, handler)
  global linear_velocity_joystick
  linear_velocity_joystick = 0
  global angular_velocity_joystick
  angular_velocity_joystick = 0
  global remote_control
  remote_control = 0
  global vel_msg_transmit
  try:
    print("Velocity Overwrite Node Started")
    rospy.init_node('velocity_overwrite')
    serial_thread = threading.Thread(target=get_serial_data)
    serial_thread.daemon = True
    serial_thread.start()
    publisher_thread = threading.Thread(target=cmd_vel_publisher)
    publisher_thread.daemon = True
    publisher_thread.start()
    print("Thread Started")
    while True:
      try:
        rospy.sleep(1)
        rospy.loginfo("Linear velocity: " + str(linear_velocity_joystick))
        rospy.loginfo("Angular velocity: " + str(angular_velocity_joystick))
        rospy.loginfo("Remote Control Enabled: " + str(remote_control))
        rospy.loginfo("vel_msg_transmit: " + str(vel_msg_transmit))
      except rospy.ROSInterruptException:
        pass
  except rospy.ROSInterruptException:
    pass
  finally:
    print("Serial CLOSE")
    ser.close()  


