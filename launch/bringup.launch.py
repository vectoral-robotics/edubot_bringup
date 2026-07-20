"""
Bringup launch file for the EduBot stack.

Starts:
  - robot_state_publisher (URDF/Xacro)
  - edubot_hardware (real or simulated)
  - corner NeoPixel LED node (optional)
  - rosbridge WebSocket server
"""

from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.conditions import IfCondition
from launch.substitutions import (
    Command,
    LaunchConfiguration,
    NotSubstitution,
    PathJoinSubstitution,
)


def generate_launch_description():
    # -----------------------------
    # Launch arguments
    # -----------------------------
    args = {
        "namespace": ("", "ROS namespace for all nodes"),
        "use_sim": ("false", "Run in simulation mode (no real hardware)"),
        "port": ("/dev/ttyACM0", "Serial port for the Arduino controller"),
        "baud": ("115200", "Serial baud rate"),
        "wheel_radius": ("0.04", "Wheel radius [m]"),
        "base_length": ("0.095", "Half of robot length [m]"),
        "base_width": ("0.1025", "Half of robot width [m]"),
        "ticks_per_rev": ("4320.0", "Encoder ticks per wheel revolution"),
        "cmd_timeout": ("0.5", "Stop if no cmd_vel received for this time [s]"),
        "odom_hz": ("50.0", "Odometry update frequency [Hz]"),
        "tf_hz": ("30.0", "TF broadcast frequency [Hz]"),
        "mecanum_layout": ("X", 'Wheel roller layout: "X" or "O"'),
        "log_commands": ("true", "Enable debug logging of motor commands"),
        "use_leds": ("true", "Start the corner NeoPixel LED node"),
        "led_count": ("4", "Number of corner NeoPixels"),
        "led_brightness": ("0.4", "NeoPixel brightness [0.0-1.0]"),
        "use_imu": ("true", "Start the BNO085 IMU node"),
        "imu_frame_id": ("imu_link", "frame_id for sensor_msgs/Imu messages"),
        "imu_hz": ("100.0", "IMU publish rate [Hz]"),
        "use_ekf": (
            "true",
            "Fuse wheel odometry + IMU with robot_localization (EKF). "
            "When true the EKF owns the odom->base_link TF and hardware_node "
            "stops broadcasting it.",
        ),
    }

    declare_args = [
        DeclareLaunchArgument(name, default_value=default, description=desc)
        for name, (default, desc) in args.items()
    ]

    # -----------------------------
    # Convenience handles
    # -----------------------------
    ns = LaunchConfiguration("namespace")
    use_sim = LaunchConfiguration("use_sim")
    port = LaunchConfiguration("port")
    baud = LaunchConfiguration("baud")
    wheel_radius = LaunchConfiguration("wheel_radius")
    base_length = LaunchConfiguration("base_length")
    base_width = LaunchConfiguration("base_width")
    ticks_per_rev = LaunchConfiguration("ticks_per_rev")
    cmd_timeout = LaunchConfiguration("cmd_timeout")
    odom_hz = LaunchConfiguration("odom_hz")
    tf_hz = LaunchConfiguration("tf_hz")
    mecanum_layout = LaunchConfiguration("mecanum_layout")
    log_commands = LaunchConfiguration("log_commands")
    use_leds = LaunchConfiguration("use_leds")
    led_count = LaunchConfiguration("led_count")
    led_brightness = LaunchConfiguration("led_brightness")
    use_imu = LaunchConfiguration("use_imu")
    imu_frame_id = LaunchConfiguration("imu_frame_id")
    imu_hz = LaunchConfiguration("imu_hz")
    use_ekf = LaunchConfiguration("use_ekf")

    # Xacro file path (URDF)
    urdf_xacro = PathJoinSubstitution(
        [
            FindPackageShare("edubot_description"),
            "urdf",
            "robot.urdf",
        ]
    )

    # Optional: colorized console output
    env = SetEnvironmentVariable("RCUTILS_COLORIZED_OUTPUT", "1")

    # -----------------------------
    # Nodes
    # -----------------------------
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        namespace=ns,
        output="screen",
        parameters=[
            {
                "robot_description": ParameterValue(Command(["xacro ", urdf_xacro]), value_type=str),
            }
        ],
    )

    hardware_node = Node(
        package="edubot_hardware",
        executable="hardware_node",
        name="hardware_node",
        namespace=ns,
        output="screen",
        parameters=[
            {
                "use_sim": use_sim,
                "port": port,
                "baud": baud,
                "wheel_radius": wheel_radius,
                "base_length": base_length,
                "base_width": base_width,
                "ticks_per_rev": ticks_per_rev,
                "cmd_timeout": cmd_timeout,
                "mecanum_layout": mecanum_layout,
                "log_commands": log_commands,
                "odom_hz": odom_hz,
                "tf_hz": tf_hz,
                # When the EKF runs it owns the odom->base_link TF, so the
                # hardware node must relinquish it (exactly one publisher).
                "publish_tf": ParameterValue(
                    NotSubstitution(use_ekf), value_type=bool
                ),
            }
        ],
    )

    # robot_localization EKF: fuses /odom (wheel) + /imu/data (BNO085) into
    # /odometry/filtered and broadcasts the fused odom->base_link transform.
    ekf_config = PathJoinSubstitution(
        [
            FindPackageShare("edubot_bringup"),
            "config",
            "ekf.yaml",
        ]
    )
    ekf_node = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_filter_node",
        namespace=ns,
        output="screen",
        condition=IfCondition(use_ekf),
        parameters=[ekf_config],
    )

    # Corner status LEDs (NeoPixel over SPI on the Raspberry Pi 5).
    # Runs in its own node; falls back to a no-op backend when use_sim is true
    # or the SPI hardware/library is unavailable.
    led_node = Node(
        package="edubot_hardware",
        executable="led_node",
        name="led_node",
        namespace=ns,
        output="screen",
        condition=IfCondition(use_leds),
        parameters=[
            {
                "use_sim": use_sim,
                "num_pixels": led_count,
                "brightness": led_brightness,
                # Cool white — same shade as the boot animation so the
                # breathing-to-steady transition is visually seamless.
                "startup_color": [200, 225, 255],
            }
        ],
    )

    # BNO085 IMU (I2C on the Raspberry Pi 5).
    imu_node = Node(
        package="edubot_hardware",
        executable="imu_node",
        name="imu_node",
        namespace=ns,
        output="screen",
        condition=IfCondition(use_imu),
        parameters=[
            {
                "use_sim": use_sim,
                "frame_id": imu_frame_id,
                "publish_hz": imu_hz,
            }
        ],
    )

    # rosapi — exposes ROS services (topics, services, params) over rosbridge.
    # Must run alongside rosbridge_websocket so clients can introspect the graph.
    # rosapi/rosbridge are deliberately left un-namespaced (unlike the robot
    # nodes above): the dashboard connects to a fixed rosbridge endpoint, and
    # rosbridge already sees the whole graph regardless of namespace.
    rosapi_node = Node(
        package="rosapi",
        executable="rosapi_node",
        name="rosapi",
        output="screen",
    )

    # rosbridge WebSocket server - allows the web dashboard to publish /cmd_vel
    rosbridge_node = Node(
        package="rosbridge_server",
        executable="rosbridge_websocket",
        name="rosbridge_websocket",
        output="screen",
        parameters=[
            {
                "port": 9090,
                "address": "",
            }
        ],
    )

    # -----------------------------
    # Return LaunchDescription
    # -----------------------------
    return LaunchDescription(
        [
            env,
            *declare_args,
            robot_state_publisher,
            hardware_node,
            led_node,
            imu_node,
            ekf_node,
            rosapi_node,
            rosbridge_node,
        ]
    )
