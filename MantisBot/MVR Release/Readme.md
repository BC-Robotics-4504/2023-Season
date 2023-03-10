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
| Retracted | XX | m |
| Extended | XX | m|

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
| Ground (Default)| XX | m |
| Score Low | XX | m |
| Score Mid | XX | m |
| Score High | XX | m |


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
| Ground (Default)| XX | m |
| Score Low | XX | m |
| Score Mid | XX | m |
| Score High | XX | m |

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
| Ground (Default)| XX | m |
| Score Low | XX | m |
| Score Mid | XX | m |
| Score High | XX | m |

### Robot IP Address

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

### **Left Flight Stick**

- Ipnut device ID `0`
- **Y-Axis**:
- **Trigger**:

### **Right Flight Stick**

- Input device ID `1`
- **Y-Axis**:
- **Trigger**:

## Game Controller Functionality

- [ ] **<CONTROLLER_NAME>**: Move toward target AprilTag
- [ ] **<CONTROLLER_NAME>**: Move toward target retro-reflective tape
- [ ] **<CONTROLLER_NAME>**: Pick up gamepiece
- [ ] **<CONTROLLER_NAME>**: Navigate to target and place high/med/low
- [ ] **<CONTROLLER_NAME>**: Balance on charging station

## Autonomous Operation

### **MODE 1**

### **MODE 2**

### **MODE 3**
