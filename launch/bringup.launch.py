from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    desc_pkg = get_package_share_directory('omnibot_description')
    bringup_pkg = get_package_share_directory('omnibot_bringup')

    rviz_config = os.path.join(bringup_pkg, 'launch', 'default.rviz')

    return LaunchDescription([
        # Robot State Publisher (mit URDF/Xacro)
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': Command([
                    'xacro ',
                    PathJoinSubstitution([
                        FindPackageShare('omnibot_description'),
                        'urdf',
                        'omnibot.urdf.xacro'
                    ])
                ])
            }]
        ),

        # Hardware Node
        Node(
            package='omnibot_hardware',
            executable='hardware_node',
            name='hardware_node',
            output='screen',
            parameters=[{
                'port': '/dev/ttyUSB0',
                'baud': 115200,
                'wheel_radius': 0.04,
                'base_length': 0.095,
                'base_width': 0.1025,
                'ticks_per_rev': 4320.0,
            }]
        ),

        # RViz2 mit fertiger Config
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rviz_config]
        ),
    ])
