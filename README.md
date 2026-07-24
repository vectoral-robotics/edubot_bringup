# edubot_bringup

Top-level launch files that bring up the [EduBot](https://github.com/vectoral-robotics) robot — by Vectoral.

## What it is

`edubot_bringup` is the entry point of the EduBot ROS 2 stack. Its launch files
start everything needed to operate the robot in one command: the robot state
publisher (URDF), the hardware interface ([`edubot_hardware`](https://github.com/vectoral-robotics/edubot_hardware)),
the corner status LEDs (`led_node`), and a rosbridge WebSocket server (+ rosapi)
that the dashboard and Foxglove connect to. It orchestrates the other packages
rather than containing robot logic itself.

It can also start a small speaker bridge node that listens to plain ROS topics
for text and volume, which keeps Blockly and the web dashboard free from custom
message packages.

## Installation

Requires ROS 2 Humble. Build it in a colcon workspace together with the other
EduBot packages it depends on (`edubot_description`, `edubot_hardware`), plus
`rosbridge_server` and `rosapi` from the ROS distribution:

```bash
cd ~/ros2_ws/src
git clone https://github.com/vectoral-robotics/edubot_bringup.git
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --packages-select edubot_bringup
source install/setup.bash
```

## Usage

Bring up the full robot:

```bash
# On the real robot
ros2 launch edubot_bringup bringup.launch.py

# In simulation (no hardware), without the corner LEDs
ros2 launch edubot_bringup bringup.launch.py use_sim:=true use_leds:=false
```

Visualization is handled by Foxglove in the browser (via the rosbridge server on
port 9090), so there is no RViz launch argument.

Keyboard teleoperation:

```bash
ros2 launch edubot_bringup teleop.launch.py
```

Common launch arguments (see `launch/bringup.launch.py` for the full list):

| Argument | Default | Description |
|---|---|---|
| `use_sim` | `false` | Run against the simulated backend instead of hardware |
| `use_leds` | `true` | Start the corner NeoPixel LED node |
| `led_count` | `4` | Number of corner NeoPixels |
| `led_brightness` | `0.4` | NeoPixel brightness (0.0–1.0) |
| `port` | `/dev/ttyACM0` | Serial port of the ESP32 controller |
| `baud` | `115200` | Serial baud rate |
| `mecanum_layout` | `X` | Wheel roller layout (`X` or `O`) |
| `use_speaker` | `true` | Start the speaker bridge node |
| `speaker_default_volume` | `80` | Default speaker volume (0–100) |

## Contributing

- Work on a short-lived feature branch and open a pull request against `main`
  (which is protected); changes land via PR review.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org)
  (`feat:`, `fix:`, `docs:`, …). See `CLAUDE.md` for repo conventions.

## License

PolyForm Perimeter 1.0.0 (source-available) — see [LICENSE](LICENSE).
