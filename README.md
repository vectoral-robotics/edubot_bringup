# edubot_bringup

Top-level launch files that bring up the [EduBot](https://github.com/vectoral-robotics) robot — by Vectoral.

## What it is

`edubot_bringup` is the entry point of the EduBot ROS 2 stack. Its launch files
start everything needed to operate the robot in one command: the robot state
publisher (URDF), the hardware interface ([`edubot_hardware`](https://github.com/vectoral-robotics/edubot_hardware)),
a rosbridge WebSocket server for the dashboard, and optionally RViz
([`edubot_viz`](https://github.com/vectoral-robotics/edubot_viz)). It orchestrates the
other packages rather than containing robot logic itself.

## Installation

Requires ROS 2 Humble. Build it in a colcon workspace together with the other
EduBot packages it depends on (`edubot_description`, `edubot_hardware`,
`edubot_viz`):

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

# In simulation (no hardware), without RViz
ros2 launch edubot_bringup bringup.launch.py use_sim:=true use_rviz:=false
```

Keyboard teleoperation:

```bash
ros2 launch edubot_bringup teleop.launch.py
```

Common launch arguments (see `launch/bringup.launch.py` for the full list):

| Argument | Default | Description |
|---|---|---|
| `use_sim` | `false` | Run against the simulated backend instead of hardware |
| `use_rviz` | `true` | Start RViz2 visualization |
| `port` | `/dev/ttyACM0` | Serial port of the ESP32 controller |
| `baud` | `115200` | Serial baud rate |
| `mecanum_layout` | `X` | Wheel roller layout (`X` or `O`) |

## Contributing

- Work on a short-lived feature branch and open a pull request against `main`
  (which is protected); changes land via PR review.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org)
  (`feat:`, `fix:`, `docs:`, …). See `CLAUDE.md` for repo conventions.

## License

PolyForm Perimeter 1.0.0 (source-available) — see [LICENSE](LICENSE).
