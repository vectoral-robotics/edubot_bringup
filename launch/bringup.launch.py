"""
Bringup launch file for the OmniBot stack.

Starts:
  - robot_state_publisher (URDF/Xacro)
  - omnibot_hardware (real or simulated)
  - optional RViz2 with a predefined config

All parameters are exposed as launch arguments for easy configuration.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.substitutions import (
    Command,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # -----------------------------
    # Launch arguments
    # -----------------------------
    args = {
        # Meta / UX
        'namespace': ('', 'ROS namespace for all nodes'),
        'use_rviz': ('true', 'Start RViz2 with a default config'),
        'rviz_config': (
            PathJoinSubstitution([FindPackageShare('omnibot_bringup'), 'launch', 'default.rviz']),
            'Path to RViz config file',
        ),

        # Hardware / sim selection
        'use_sim': ('false', 'Run in simulation mode (no real hardware)'),

        # Serial config
        'port': ('/dev/ttyUSB0', 'Serial port for the Arduino controller'),
        'baud': ('115200', 'Serial baud rate'),

        # Robot kinematics / encoders
        'wheel_radius': ('0.04', 'Wheel radius [m]'),
        'base_length': ('0.095', 'Half of robot length [m]'),
        'base_width': ('0.1025', 'Half of robot width [m]'),
        'ticks_per_rev': ('4320.0', 'Encoder ticks per wheel revolution'),
        'encoder_dt': ('0.02', 'Encoder sampling interval [s]'),
        'cmd_timeout': ('0.5', 'Stop if no cmd_vel received for this time [s]'),
        'mecanum_layout': ('X', 'Wheel roller layout: "X" or "O"'),
        'log_commands': ('false', 'Enable debug logging of motor commands'),
    }

    declare_args = [
        DeclareLaunchArgument(name, default_value=default, description=desc)
        for name, (default, desc) in args.items()
    ]

    # Convenience handles
    ns = LaunchConfiguration('namespace')
    use_rviz = LaunchConfiguration('use_rviz')
    rviz_config = LaunchConfiguration('rviz_config')

    use_sim = LaunchConfiguration('use_sim')
    port = LaunchConfiguration('port')
    baud = LaunchConfiguration('baud')

    wheel_radius = LaunchConfiguration('wheel_radius')
    base_length = LaunchConfiguration('base_length')
    base_width = LaunchConfiguration('base_width')
    ticks_per_rev = LaunchConfiguration('ticks_per_rev')
    encoder_dt = LaunchConfiguration('encoder_dt')
    cmd_timeout = LaunchConfiguration('cmd_timeout')
    mecanum_layout = LaunchConfiguration('mecanum_layout')
    log_commands = LaunchConfiguration('log_commands')

    # Xacro file path (URDF)
    urdf_xacro = PathJoinSubstitution([
        FindPackageShare('omnibot_description'),
        'urdf',
        'omnibot.urdf.xacro',
    ])

    # Optional: make Python logs line-buffered in terminals
    env = SetEnvironmentVariable('RCUTILS_COLORIZED_OUTPUT', '1')

    # -----------------------------
    # Nodes
    # -----------------------------
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        namespace=ns,
        output='screen',
        parameters=[{
            # If your Xacro supports macro args, you can pass them here, e.g.:
            # 'robot_description': Command(['xacro ', urdf_xacro, ' use_sim:=', use_sim]),
            'robot_description': Command(['xacro ', urdf_xacro]),
        }],
    )

    hardware_node = Node(
        package='omnibot_hardware',
        executable='hardware_node',
        name='hardware_node',
        namespace=ns,
        output='screen',
        parameters=[{
            'use_sim': use_sim,
            'port': port,
            'baud': baud,
            'wheel_radius': wheel_radius,
            'base_length': base_length,
            'base_width': base_width,
            'ticks_per_rev': ticks_per_rev,
            'encoder_dt': encoder_dt,
            'cmd_timeout': cmd_timeout,
            'mecanum_layout': mecanum_layout,
            'log_commands': log_commands,
        }],
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        namespace=ns,
        output='screen',
        arguments=['-d', rviz_config],
        condition=IfCondition(use_rviz),
    )

    return LaunchDescription([
        env,
        *declare_args,
        robot_state_publisher,
        hardware_node,
        rviz,
    ])
