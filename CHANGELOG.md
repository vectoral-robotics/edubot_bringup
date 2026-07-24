## v0.3.0 (2026-07-24)

### Feat

- **bringup**: merge speaker node into dev-alex (EKF + speaker combined)
- **bringup**: fuse wheel odom + IMU with robot_localization EKF
- **bringup**: add imu_node to launch description

### Fix

- **bringup**: wrap robot_description in ParameterValue to fix yaml parse error

## v0.2.0 (2026-07-20)

### Feat

- **bringup**: add imu_node to launch description

## v0.1.0 (2026-07-15)

### Feat

- **viz**: remove rviz launch arg, use Foxglove instead
- **leds**: pass startup_color to led_node in bringup
- **leds**: launch corner LED node in bringup

### Fix

- **deps**: sync package.xml with launch (add rosbridge_server + rosapi, drop rviz2)
- **launch**: add rosapi node alongside rosbridge for topic introspection

## v0.0.2 (2026-07-02)

### Fix

- **ci**: run commitizen via 'uvx --from commitizen cz'
- rviz config

### Refactor

- rename omnibot to edubot across the repo
- bringup node
