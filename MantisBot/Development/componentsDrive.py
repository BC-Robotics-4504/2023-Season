import ctre
import rev 
from wpimath.controller import PIDController
from wpilib import SmartDashboard

from math import pi

from componentsHMI import FlightStickHMI
# from componentsIMU import IMUModule

class ComboSparkMax:

    # PID coefficients
    kP = 5e-5
    kI = 1e-6
    kD = 0
    kIz = 0
    kFF = 0.000156
    kMaxOutput = 1
    kMinOutput = -1
    maxRPM = 5700

    # Smart Motion Coefficients
    maxVel = 2000 # rpm
    maxAcc = 1500
    minVel = 0
    allowedErr = 0

    def __init__(self, canID_leader, canID_followers, motorType='brushless', inverted=False, 
                 gear_ratio=1, wheel_diameter=0.1524):
        self.canID_leader = canID_leader
        self.canID_followers = canID_followers
        self.inverted = inverted
        self.mainMotor = None
        self.followerMotors = None
        self.gear_ratio = gear_ratio
        self.wheel_diameter = wheel_diameter
        self.distance_to_rotations = 1/(2*pi*wheel_diameter*gear_ratio)

        if motorType == 'brushless':
            mtype = rev.CANSparkMaxLowLevel.MotorType.kBrushless
        else:
            mtype = rev.CANSparkMaxLowLevel.MotorType.kBrushed # FIXME!: Is this right?

        self.mainMotor = rev.CANSparkMax(canID_leader, mtype)
        self.mainMotor.restoreFactoryDefaults()
        self.mainMotor.setInverted(self.inverted)
        self.mainController, self.mainEncoder = self.__configureEncoder__(self.mainMotor)

        followerMotors = []
        for canID in self.canID_followers:
            follower = rev.CANSparkMax(canID, mtype)
            follower.restoreFactoryDefaults()
            follower.setInverted(self.inverted)
            follower.follow(self.mainMotor)                              
            followerMotors.append(follower)

        self.followerMotors = followerMotors

    def __configureEncoder__(self, motor, smartMotionSlot=0):
        mainController = motor.getPIDController()
        mainEncoder = motor.getEncoder()
        
        # PID parameters
        mainController.setP(self.kP)
        mainController.setI(self.kI)
        mainController.setD(self.kD)
        mainController.setIZone(self.kIz)
        mainController.setFF(self.kFF)
        mainController.setOutputRange(self.kMinOutput, self.kMaxOutput)

        # Smart Motion Parameters
        mainController.setSmartMotionMaxVelocity(self.maxVel, smartMotionSlot)
        mainController.setSmartMotionMinOutputVelocity(self.minVel, smartMotionSlot)
        mainController.setSmartMotionMaxAccel(self.maxAcc, smartMotionSlot)
        mainController.setSmartMotionAllowedClosedLoopError(self.allowedErr, smartMotionSlot)
        return mainController, mainEncoder

    def setPercent(self, value):
        self.mainMotor.set(value)
        return False

    def getVelocity(self):
        vel = self.mainEncoder.getVelocity() #rpm
        return vel

    def getDistance(self):
        pos = self.mainEncoder.getPosition()
        return pos

    def resetDistance(self):
        self.mainEncoder.setPosition(0)
        return False
    
    def setDistance(self, distance):
        rotations = distance*self.distance_to_rotations
        self.mainController.setReference(rotations, rev.CANSparkMax.ControlType.kSmartMotion)
        return False


class DriveTrainModule:
    mainLeft_motor: ComboSparkMax
    mainRight_motor: ComboSparkMax
    hmi_interface: FlightStickHMI

    def __init__(self):
        self.leftSpeed = 0
        self.leftSpeedChanged = False
        
        self.rightSpeed = 0
        self.rightSpeedChanged = False  

        self.arcadeSpeed = [0,0]    

        self.autoLockout = True

    def setLeft(self, value):
        self.leftSpeed = value
        self.leftSpeedChanged = True
        
    def setRight(self, value):
        self.rightSpeed = value
        self.rightSpeedChanged = True

    def resetDistance(self):
        self.mainRight_motor.resetDistance()
        self.mainLeft_motor.resetDistance()

    def setDistance(self, value):
        self.mainRight_motor.setDistance(value)
        self.mainLeft_motor.setDistance(value)
        return False
        
    def is_leftChanged(self):
        return self.leftSpeedChanged
    
    def is_rightChanged(self):
        return self.rightSpeedChanged

    def enable_autoLockout(self):
        self.autoLockout = True
        return False

    def disable_autoLockout(self):
        self.autoLockout = False
        return False

    def is_lockedout(self):
        return self.autoLockout

    # Arcade drive code from https://xiaoxiae.github.io/Robotics-Simplified-Website/drivetrain-control/arcade-drive/
    def setArcade(self, drive, rotate):
        self.arcadeSpeed = [drive, rotate]
        """Drives the robot using arcade drive."""
        # variables to determine the quadrants
        maximum = max(abs(drive), abs(rotate))
        total, difference = drive + rotate, drive - rotate

        # set speed according to the quadrant that the values are in
        if drive >= 0:
            if rotate >= 0:  # I quadrant
                self.setLeft(maximum)
                self.setRight(difference)
            else:            # II quadrant
                self.setLeft(total)
                self.setRight(maximum)
        else:
            if rotate >= 0:  # IV quadrant
                self.setLeft(total)
                self.setRight(-maximum)
            else:            # III quadrant
                self.setLeft(-maximum)
                self.setRight(difference)
    
    def getArcadeLinear(self):
        return self.arcadeSpeed[0]
    
    def getArcadeRotation(self):
        return self.arcadeSpeed[1]

    def check_hmi(self):
        (leftSpeed, rightSpeed) = self.hmi_interface.getInput()
        self.setLeft(leftSpeed)
        self.setRight(rightSpeed)
        return False
    
    def clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)

    def execute(self):

        if not self.autoLockout:
            self.check_hmi()
        
        '''This gets called at the end of the control loop'''
        if self.is_leftChanged():
            self.mainLeft_motor.setPercent(self.leftSpeed)
            self.leftSpeedChanged = False

        if self.is_rightChanged():
            self.mainRight_motor.setPercent(self.rightSpeed)
            self.rightSpeedChanged = False