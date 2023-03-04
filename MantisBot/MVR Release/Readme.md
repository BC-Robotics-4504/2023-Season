# Miami Valley Regional

## Robotpy Setup

```sh
python -m pip install --upgrade pip
python -m pip install robotpy
python -m robotpy_installer download robotpy
python -m robotpy_installer install robotpy
```

## Hardware Configuration

### Grabber Arm

- **[SparkMax](https://www.revrobotics.com/rev-11-2158/)** (1x):
  - CAN ID `12`
  - 1:64 gear ratio
  - Drives [Neo Brushless Motor V1.1](https://www.revrobotics.com/rev-21-1650/)
  - Sprocket diameter XX

- **[Pneumatic Hub](https://www.revrobotics.com/rev-11-1852/)**:
  - CAN ID `11`
  - Double solenoid

### Elevator

- **[SparkMax](https://www.revrobotics.com/rev-11-2158/)** (1x, +1 spare):
  - CAN ID `13`
  - 1:20 gear ratio
  - Drives [Neo Brushless Motor V1.1](https://www.revrobotics.com/rev-21-1650/)
  - Sprocket diameter XX

### Drivetrain

- **[SparkMax](https://www.revrobotics.com/rev-11-2158/)** (4x):
  - *LEFT SIDE*: 
    - Leader CAN ID `6`
    - Follower CAN ID `4`
    - 30:68 gear ratio
    - Drives 2x [Neo Brushless Motor V1.1](https://www.revrobotics.com/rev-21-1650/)
    - [2 Motor Gearbox](https://www.revrobotics.com/rev-21-2099/)
    - Wheel diameter 6 in (0.1524 m) OD
    - Inverted

  - *RIGHT SIDE*: 
    - Leader CAN ID `2`
    - Follower CAN ID `1`
    - 30:68 gear ratio
    - Drives 2x [Neo Brushless Motor V1.1](https://www.revrobotics.com/rev-21-1650/)
    - [2 Motor Gearbox](https://www.revrobotics.com/rev-21-2099/)
    - Wheel diameter 6 in (0.1524 m) OD
    - Non-inverted

### Sensors

- **[Pigeon 2.0](https://www.google.com/search?client=safari&rls=en&q=pigeon+2.0&ie=UTF-8&oe=UTF-8)**:
  - CAN ID `11`
  - Orientation: Z up, X forward, Y right

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

## Autonomous Operation

### **MODE 1**

### **MODE 2**

### **MODE 3**

## Game Controller Functionality

- [ ] **<CONTROLLER_NAME>**: Move toward target AprilTag
- [ ] **<CONTROLLER_NAME>**: Move toward target retro-reflective tape
- [ ] **<CONTROLLER_NAME>**: Pick up gamepiece
- [ ] **<CONTROLLER_NAME>**: Navigate to target and place high/med/low
- [ ] **<CONTROLLER_NAME>**: Balance on charging station