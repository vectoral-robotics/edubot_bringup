cmake_minimum_required(VERSION 3.10)
project(omnibot_bringup)

find_package(ament_cmake REQUIRED)

# Install launch files and any RViz configs bundled alongside
install(
  DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
