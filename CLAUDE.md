# edubot_bringup — Claude guidelines

ROS2 package providing the top-level launch files that bring up the EduBot
robot (`bringup.launch.py`, `teleop.launch.py`). Part of the EduBot ROS2 stack,
consumed by `edubot_dashboard` via its vcstool manifest.

These guidelines will grow over time. For now the most important rule:

## Commits

All commits MUST follow the [Conventional Commits](https://www.conventionalcommits.org) spec.

Format:

    <type>(<optional scope>): <short summary>

Common types: `feat`, `fix`, `docs`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.

- Imperative mood ("add", not "added").
- Summary under ~72 characters, lower case, no trailing period.
- Scope is optional and names the affected area.

Example:

    feat(bringup): add lidar enable flag to launch
