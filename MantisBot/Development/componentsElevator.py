import rev 
from math import pi

ElevatorLevelDict_m = {
    0: 0,
    1: 0.35,
    2: 0.65,
    3: 1.0,
}

def positionToNextLevel(current_level, next_level):
    assert current_level in ElevatorLevelDict_m.keys(), '[+] ERROR: current level argument not a valid level'
    assert next_level in ElevatorLevelDict_m.keys(), '[+] ERROR: next level argument not a valid level'
    return ElevatorLevelDict_m[next_level] - ElevatorLevelDict_m[current_level]

class ElevatorSparkMax:

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
                gear_ratio=20, wheel_diameter=6.5):
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
            mtype = rev.CANSparkMaxLowLevel.MotorType.kBrushed

        self.mainMotor = rev.CANSparkMax(canID_leader, mtype)
        self.mainMotor.setInverted(inverted)
        self.mainController, self.mainEncoder = self.__configureEncoder__(self.mainMotor)

        followerMotors = []
        for canID in self.canID_followers:
            follower = rev.CANSparkMax(canID, mtype)
            follower.setInverted(not inverted)
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

class ElevatorModule:
    '''
    REFERENCE: https://github.com/REVrobotics/SPARK-MAX-Examples/blob/master/Java/Position%20Closed%20Loop%20Control/src/main/java/frc/robot/Robot.java
    '''

    elevator_motor: ElevatorSparkMax

    def __init__(self, tol=0.05):
        self.currentPosition = 0
        self.nextPosition = 0
        self.currentLevel = 0
        self.nextLevel = 0
        self.stateChanged = False
        self.tol = tol

    def goToNextLevel(self, next_level):
        distance = positionToNextLevel(self.currentLevel, self.nextLevel)
        self.nextElevatorPosition = distance
        self.elevator_motor.setDistance(distance)
        return False

    def getPosition(self):
        self.currentElevatorPosition = self.elevator_motor.getDistance()
        return False

    def isAtLevel(self):
        if abs(self.currentPosition - self.nextPosition) < self.tol:
            self.currentLevel = self.nextLevel
            return True

        return False

    def setNextLevel(self, next_level):
        if next_level not in ElevatorLevelDict_m.keys():
            return True
        self.stateChanged = True
        self.nextElevatorLevel = next_level

    def execute(self):
        # Update elevator position
        self.getPosition()

        # Move level if needed
        if self.stateChanged:
            self.goToNextLevel()
            self.stateChanged = False

        pass



        


        

