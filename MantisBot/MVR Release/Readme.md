# Miami Valley Regional
## Robotpy Setup
```
python -m pip install --upgrade pip
python -m pip install robotpy
python -m robotpy_installer download robotpy
python -m robotpy_installer install robotpy
```
## Hardware Description
###### Grabber Arm
- **[SparkMax](https://www.revrobotics.com/rev-11-2158/)** (1x):
    - CAN ID `12`
- **[Pneumatic Hub](https://www.revrobotics.com/rev-11-1852/)**:
    - CAN ID `11`

###### Elevator
- **[SparkMax](https://www.revrobotics.com/rev-11-2158/)** (1x, +1 spare):
    - CAN ID `13`

###### Drivetrain
- **[SparkMax](https://www.revrobotics.com/rev-11-2158/)** (4x):
    - *LEFT*: 
        - Leader CAN ID `6`
        - Follower CAN ID `4`
    - *RIGHT*: 
        - Leader CAN ID `2`
        - Follower CAN ID `1`

###### Sensors
- **[Pigeon 2.0](https://www.google.com/search?client=safari&rls=en&q=pigeon+2.0&ie=UTF-8&oe=UTF-8)**:
    - CAN ID `11`

- **[Limelight 2.0](https://docs.limelightvision.io/en/latest/)**: 
    - Static IP address `10.4.45.11`

- **[PhotonVision (RPi)](https://photonvision.org)**: 
    - Static IP address `10.4.45.12`
    - Camera Name `MSWebCam`

## Robot Controls
###### **Left Flight Stick**:
- Ipnut device ID `0`
- **Y-Axis**:
- **Trigger**:

###### **Right Flight Stick**:
- Input device ID `1`
- **Y-Axis**:
- **Trigger**:

## Autonomous Operation
###### **MODE 1**:
###### **MODE 2**:
###### **MODE 3**: