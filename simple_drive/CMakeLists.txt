cmake_minimum_required(VERSION 2.8.3)

project(simple_drive)

find_package(catkin REQUIRED COMPONENTS
  rospy
  sensor_msgs
  geometry_msgs
  actionlib_msgs
  std_msgs
  message_generation
)

catkin_python_setup()

add_message_files(
  FILES
  serial_joy.msg
)

 generate_messages(
   DEPENDENCIES
   std_msgs  # Or other packages containing msgs
 )

catkin_package(
  LIBRARIES ${PROJECT_NAME}
  CATKIN_DEPENDS rospy sensor_msgs geometry_msgs actionlib_msgs std_msgs message_runtime
)

catkin_install_python(
  PROGRAMS nodes/simple_drive nodes/drive_teleop nodes/cmd_vel_mux
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)


# Install launch files
install(DIRECTORY launch/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/launch
)

# Install firmware files
install(DIRECTORY drive_firmware/
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/drive_firmware
)
