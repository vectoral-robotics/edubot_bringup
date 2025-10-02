cmake_minimum_required(VERSION 3.5)
project(omnibot_bringup)

find_package(ament_cmake REQUIRED)

# Installiere den launch-Ordner
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
