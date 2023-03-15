# Miami Valley Regional

## Robotpy Setup

BC Robotics (Team #4504) has designed their 2023 FIRST Robotics submission using the [Robotpy](https://robotpy.readthedocs.io/en/stable/install/robot.html) with the [MagicBot Framework](https://robotpy.readthedocs.io/en/stable/frameworks/magicbot.html). To keep the relevant libraries current, the follow code will need to be run regularly in a terminal interface:

```sh
python -m pip install --upgrade pip
python -m pip install robotpy
python -m robotpy_installer download robotpy
python -m robotpy_installer install robotpy
```

## Hardware Configuration

### Grabber Arm

- **[SparkMax](https://www.revrobotics.com/rev-11-2158/)** (1x):
  - Drives [Neo Brushless Motor V1.1](https://www.revrobotics.com/rev-21-1650/)

| Position | Value | Unit |
| --- | --- | --- |
| CAN ID | 12 |  |
| Gear Ratio | 1:64 |  |
| Sprocket Diameter | 0.0762 (3) | m (in) |
| Retracted | 0 | m |
| Mid-Extended | 0.06 | m |
| Extended | 0.12 | m|

- **[Pneumatic Hub](https://www.revrobotics.com/rev-11-1852/)**:
  - CAN ID `11`
  - Double solenoid

### Elevator

- **[SparkMax](https://www.revrobotics.com/rev-11-2158/)** (1x, +1 spare):
  - Drives [Neo Brushless Motor V1.1](https://www.revrobotics.com/rev-21-1650/)

| Position | Value | Unit |
| --- | --- | --- |
| CAN ID | 13 |  |
| Gear Ratio | 1:20 |  |
| Sprocket Diameter | 0.0508 (2) | m (in) |
| Ground (Default)| 0 | m |
| Score Low | 0.25 | m |
| Score Mid | 0.40 | m |
| Score Extra-Mid | 0.8 | m |
| Score High | 1.0620 | m |

### Drivetrain

- **[SparkMax](https://www.revrobotics.com/rev-11-2158/)** (4x):
  - *LEFT SIDE*: 
    - Drives 2x [Neo Brushless Motor V1.1](https://www.revrobotics.com/rev-21-1650/)
    - [2 Motor Gearbox](https://www.revrobotics.com/rev-21-2099/)
    - Inverted

| Position | Value | Unit |
| --- | --- | --- |
| Leader CAN ID | 2 |  |
| Follower CAN ID | 1 |  |
| Gear Ratio | (68/30)x(52/11) |  |
| Wheel Diameter | 0.1524 (6) | m (in) |

  - *RIGHT SIDE*: 
    - Drives 2x [Neo Brushless Motor V1.1](https://www.revrobotics.com/rev-21-1650/)
    - [2 Motor Gearbox](https://www.revrobotics.com/rev-21-2099/)
    - Non-inverted

| Position | Value | Unit |
| --- | --- | --- |
| Leader CAN ID | 3 |  |
| Follower CAN ID | 4 |  |
| Gear Ratio | (68/30)x(52/11)|  |
| Wheel Diameter | 0.1524 (6) | m (in) |

### Robot IP Address
`10.45.4.1` 
### Sensors

- **[Pigeon 2.0](https://www.google.com/search?client=safari&rls=en&q=pigeon+2.0&ie=UTF-8&oe=UTF-8)**:
  - CAN ID `15`
  - Orientation: Z up, X forward, Y right

| Sensor Direction | Robot Direction |
| --- | --- |
| +X | Right |
| +Y | Forward |
| +Z | Up |

- **[Limelight 2.0](https://docs.limelightvision.io/en/latest/)**:
  - Static IP address `10.4.45.11`

- **[PhotonVision (RPi)](https://photonvision.org)**:
  - Static IP address `10.4.45.12`
  - Camera Name `MSWebCam`

## Robot Controls

### **[Left Flight Stick](https://www.amazon.com/9632910403-Logitech-WingMan-ATTACK-Joystick/dp/B0000ALFC5)**

- Input device ID `0`
- **Y-Axis**: Move Left Driveside Forward and Back
- **Trigger**: Open Grabber
- **L2**: Score a Low Goal
- **L3**: Score a High Goal 
- **L4**: Score a Mid Goal 
- **L5**: Score a Mid Goal 
- **L6**: Fully extends grabber
- **L8**: Fully retracts grabber
- **L9**: Resets elevator 
- **L11**: Fully extends elevator 

### **[Right Flight Stick](https://www.logitechg.com/en-us/products/space/extreme-3d-pro-joystick.963290-0403.html)**

- Input device ID `1`
- **Y-Axis**: Move Right Driveside Forward and Back
- **Trigger**: Close Grabber
- **R3**: Pickup Gamepiece from the ground
- **R4**: Pickup Gamepiece from the ground
- **R5**: Pickup Gamepiece from the loading zone
- **R6**: Pickup Gamepiece from the loading zone
## Game Controller Functionality

-  **<Score_High>**: Score a high goal
-  **<Score_Mid>**: Score a medium goal
-  **<Score_Low>**: Score a low goal
-  **<controller_floor>**: Picks up a gamepiece from the ground 
-  **<controller_station>**: Picks up a gamepiece from the loading zone 
-  **<controller_autonomous>**: Controls autonomous mode


## Autonomous Operation

  **Our autonomous plan is as follows...**

  1. Score pre-loaded cargo
  2. Backup and head out of the community 
