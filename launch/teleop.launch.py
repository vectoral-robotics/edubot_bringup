from launch_ros.actions import Node

from launch import LaunchDescription


def generate_launch_description():
    teleop_params = {
        "require_enable_button": False,
        "enable_button": 5,
        "enable_turbo_button": 4,
        "axis_linear.x": 1,
        "axis_linear.y": 0,
        "axis_angular.yaw": 3,
        "scale_linear.x": 0.5,
        "scale_linear.y": 0.5,
        "scale_linear_turbo.x": 1.0,
        "scale_linear_turbo.y": 1.0,
        "scale_angular.yaw": 1.0,
    }

    return LaunchDescription(
        [
            # Joystick input node
            Node(package="joy", executable="joy_node", name="joy_node", output="screen"),
            # Teleop node
            Node(
                package="teleop_twist_joy",
                executable="teleop_node",
                name="teleop_twist_joy_node",
                output="screen",
                parameters=[teleop_params],
            ),
        ]
    )
