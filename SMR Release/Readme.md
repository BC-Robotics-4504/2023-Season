# 2023 Smoky Mountains Regional

## Robotpy Setup

BC Robotics (Team #4504) has designed their 2023 FIRST Robotics submission using [Robotpy](https://robotpy.readthedocs.io/en/stable/install/robot.html) with the [MagicBot Framework](https://robotpy.readthedocs.io/en/stable/frameworks/magicbot.html). To keep the relevant libraries current, the following code will need to be run regularly in a terminal interface:

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

### **[GameSir G7 Wired Controller](https://www.amazon.com/dp/B0BM9HRCCV?ref_=cm_sw_r_apin_dp_ER34REM3C1FQSY0W5MQR)**

- Input device ID `0`
- **Left Joystick**: Move Robot along the Y-axis
- **Right Joystick**: Moves robot along X-axis
- **Right Trigger**: Open Grabber
- **Left Trigger**: Closes Grabber
- **Y**: Score a High Goal  
- **B**: Score a Mid Goal  
- **A**: Return superstructure to default positon  
- **Back**: Fully retracts superstructure and disables break
- **Start**: Fully retracts superstructure  
- **D-Pad Up**: Pickup from loading zone

## Game Controller Functionality  

- **<Score_High>**: Score a high goal
- **<Score_Mid>**: Score a medium goal
- **<Score_Low>**: Score a low goal
- **<controller_floor>**: Picks up a gamepiece from the ground  
- **<controller_station>**: Picks up a gamepiece from the loading zone  
- **<controller_autonomous>**: Controls autonomous mode


## Autonomous Operation

  **Our autonomous plan is as follows...**

  1. Backup .5 meters
  2. Extend grabber and elevator
  3. Move up .5 meters
  4. Score a gamepiece (preferably cube)
  5. Backup 3 meters and exit the communtity (when .5 meters is reached the superstructure retracts.)
