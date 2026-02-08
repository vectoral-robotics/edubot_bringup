"""
Bringup launch file for the OmniBot stack.

Starts:
  - robot_state_publisher (URDF/Xacro)
  - omnibot_hardware (real or simulated)
  - optional RViz2 (via omnibot_viz)
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
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
        'namespace': ('', 'ROS namespace for all nodes'),
        'use_rviz': ('true', 'Start RViz2 visualization'),
        'use_sim': ('false', 'Run in simulation mode (no real hardware)'),
        'port': ('/dev/ttyACM0', 'Serial port for the Arduino controller'),
        'baud': ('115200', 'Serial baud rate'),
        'wheel_radius': ('0.04', 'Wheel radius [m]'),
        'base_length': ('0.095', 'Half of robot length [m]'),
        'base_width': ('0.1025', 'Half of robot width [m]'),
        'ticks_per_rev': ('4320.0', 'Encoder ticks per wheel revolution'),
        'cmd_timeout': ('0.5', 'Stop if no cmd_vel received for this time [s]'),
        'odom_hz': ('50.0', 'Odometry update frequency [Hz]'),
        'tf_hz': ('30.0', 'TF broadcast frequency [Hz]'),
        'mecanum_layout': ('X', 'Wheel roller layout: "X" or "O"'),
        'log_commands': ('true', 'Enable debug logging of motor commands'),
    }

    declare_args = [
        DeclareLaunchArgument(name, default_value=default, description=desc)
        for name, (default, desc) in args.items()
    ]

    # -----------------------------
    # Convenience handles
    # -----------------------------
    ns = LaunchConfiguration('namespace')
    use_rviz = LaunchConfiguration('use_rviz')
    use_sim = LaunchConfiguration('use_sim')
    port = LaunchConfiguration('port')
    baud = LaunchConfiguration('baud')
    wheel_radius = LaunchConfiguration('wheel_radius')
    base_length = LaunchConfiguration('base_length')
    base_width = LaunchConfiguration('base_width')
    ticks_per_rev = LaunchConfiguration('ticks_per_rev')
    cmd_timeout = LaunchConfiguration('cmd_timeout')
    odom_hz = LaunchConfiguration('odom_hz')
    tf_hz = LaunchConfiguration('tf_hz')
    mecanum_layout = LaunchConfiguration('mecanum_layout')
    log_commands = LaunchConfiguration('log_commands')

    # Xacro file path (URDF)
    urdf_xacro = PathJoinSubstitution([
        FindPackageShare('omnibot_description'),
        'urdf',
        'robot.urdf',
    ])

    # Optional: colorized console output
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
            'cmd_timeout': cmd_timeout,
            'mecanum_layout': mecanum_layout,
            'log_commands': log_commands,
            'odom_hz': odom_hz,
            'tf_hz': tf_hz,
        }],
    )

    # -----------------------------
    # Include omnibot_viz (RViz)
    # -----------------------------
    viz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('omnibot_viz'),
                'launch',
                'bringup_view.launch.py'
            ])
        ),
        condition=IfCondition(use_rviz)
    )

    # -----------------------------
    # Return LaunchDescription
    # -----------------------------
    return LaunchDescription([
        env,
        *declare_args,
        robot_state_publisher,
        hardware_node,
        viz_launch,
    ])
