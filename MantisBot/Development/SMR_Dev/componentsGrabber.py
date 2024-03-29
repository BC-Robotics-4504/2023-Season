import rev 
from math import pi
import wpilib

GrabberLevelDict_m = {
    0: 0,
    1: 0.10,
    2: 0.14,
    3: -0.02
}

# def distanceToNextLevel(current_level, next_level):
#     assert current_level in GrabberLevelDict_m.keys(), '[+] ERROR: current level argument not a valid level'
#     assert next_level in GrabberLevelDict_m.keys(), '[+] ERROR: next level argument not a valid level'
#     return GrabberLevelDict_m[next_level] - GrabberLevelDict_m[current_level]

class GrabberSparkMax:

    # PID coefficients
    kP = 1e-5
    kI = 1e-8
    kD = 0
    kIz = 0
    # kFF = 0.000156
    kFF = 0.0005
    kMaxOutput = 1
    kMinOutput = -1
    maxRPM = 5700

    # Smart Motion Coefficients
    maxVel = 2000 # rpm
    maxAcc = 1500
    minVel = 0
    allowedErr = 0

    def __init__(self, canID_leader, canID_followers, motorType='brushless', inverted=False,
                gear_ratio=64, wheel_diameter=0.0508):
        self.canID_leader = canID_leader
        self.canID_followers = canID_followers
        self.inverted = inverted
        self.mainMotor = None
        self.followerMotors = None
        self.gear_ratio = gear_ratio
        self.wheel_diameter = wheel_diameter
        self.distance_to_rotations = gear_ratio/(pi*wheel_diameter)

        if motorType == 'brushless':
            mtype = rev.CANSparkMaxLowLevel.MotorType.kBrushless
        else:
            mtype = rev.CANSparkMaxLowLevel.MotorType.kBrushed

        self.mainMotor = rev.CANSparkMax(canID_leader, mtype)
        self.mainMotor.setInverted(inverted)
        self.mainController, self.mainEncoder = self.__configureEncoder__(self.mainMotor)
        self.resetDistance()

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
    
    def disableBrake(self):
        self.mainMotor.setIdleMode(self.mainMotor.IdleMode.kCoast)

    def enableBrake(self):
        self.mainMotor.setIdleMode(self.mainMotor.IdleMode.kBrake)

    def setPercent(self, value):
        self.mainMotor.set(value)
        return False

    def getVelocity(self):
        vel = self.mainEncoder.getVelocity() #rpm
        return vel

    def getDistance(self):
        pos = -self.mainEncoder.getPosition() / self.distance_to_rotations
        return pos

    def resetDistance(self):
        self.mainEncoder.setPosition(0)
        return False

    def setDistance(self, distance):
        rotations = distance * self.distance_to_rotations
        self.mainController.setReference(-rotations, rev.CANSparkMax.ControlType.kSmartMotion)
        return False
    

class GrabberPneumatics:

    PNEUMATIC_FORWARD_CHANNEL = 0
    PNEUMATIC_REVERSE_CHANNEL = 1

    def __init__(self, can_id):
        self.can_id = can_id
        self.hub = wpilib.PneumaticHub(can_id)
        self.is_open = False
        self.doubleSolenoid = self.hub.makeDoubleSolenoid(self.PNEUMATIC_FORWARD_CHANNEL, 
                                                          self.PNEUMATIC_REVERSE_CHANNEL)

    def reset(self):
        self.hub.clearStickyFaults()
        return False
    
    def close(self):
        self.doubleSolenoid.set(wpilib.DoubleSolenoid.Value.kForward) #forward = 1, reverse = 2, off = 0
        self.is_open = False
        return False
    
    def open(self):
        self.doubleSolenoid.set(wpilib.DoubleSolenoid.Value.kReverse) #forward = 1, reverse = 2, off = 0
        self.is_open = True
        return False

    def isOpen(self):
        return self.is_open


class GrabberModule:
    '''
    REFERENCE: https://github.com/REVrobotics/SPARK-MAX-Examples/blob/master/Java/Position%20Closed%20Loop%20Control/src/main/java/frc/robot/Robot.java
    '''
    
    grabber_motor: GrabberSparkMax
    grabber_pneumatics: GrabberPneumatics

    def __init__(self, tol=0.01):
        self.currentPosition = 0
        self.nextPosition = 0
        self.currentLevel = 0
        self.nextLevel = 0
        self.stateChanged = False
        self.tol = tol
        
    def disableBrake(self):
        self.grabber_motor.disableBrake()

    def enableBrake(self):
        self.grabber_motor.enableBrake()

    def goToLevel(self, level):
        distance = GrabberLevelDict_m[level]
        self.nextLevel = level
        self.nextPosition = distance
        self.grabber_motor.setDistance(distance)
        return self.isAtLevel()

    def getDistance(self):
        return self.currentPosition
    
    def updateDistance(self):
        self.currentPosition = self.grabber_motor.getDistance()
        return False

    def isAtLevel(self):
        if abs(self.currentPosition - self.nextPosition) <= self.tol:
            self.currentLevel = self.nextLevel
            return True

        return False

    def openGrabber(self):
        self.grabber_pneumatics.open() 
        self.isOpen = True
        return False
        
    def closeGrabber(self):
        self.grabber_pneumatics.close()
        self.isOpen = False
        return False

    def is_stateChanged(self):
        return self.stateChanged

    def is_open(self):
        return self.isOpen

    def setOpen(self):
        self.stateChanged = True
        self.isOpen = True

    def setClosed(self):
        self.stateChanged = True
        self.isOpen = False

    def execute(self):
        # Update grabber position
        self.updateDistance()

        # Check if state has changed
        if self.stateChanged:
            if self.isOpen:
                self.openGrabber()
            else:
                self.closeGrabber()
            self.stateChanged = False
            
        pass