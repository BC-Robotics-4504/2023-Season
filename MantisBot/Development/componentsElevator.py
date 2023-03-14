import rev 
from math import pi

ElevatorLevelDict_m = {
    0: 0,
    1: 0.35,
    2: 1.0,
    3: 1.025,
}

def positionToNextLevel(next_level):
    assert next_level in ElevatorLevelDict_m.keys(), '[+] ERROR: next level argument not a valid level'
    return ElevatorLevelDict_m[next_level]

class ElevatorSparkMax:

    # PID coefficients
    kP = 5e-5
    kI = 1e-7
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
                gear_ratio=20, wheel_diameter=0.0381 ): # 1.5 inch sprocket diameter
        self.canID_leader = canID_leader
        self.canID_followers = canID_followers
        self.inverted = inverted
        self.mainMotor = None
        self.followerMotors = None
        self.gear_ratio = gear_ratio
        self.sprocket_diameter = wheel_diameter
        self.distance_to_rotations = gear_ratio/(pi*wheel_diameter)

        if motorType == 'brushless':
            mtype = rev.CANSparkMaxLowLevel.MotorType.kBrushless
        else:
            mtype = rev.CANSparkMaxLowLevel.MotorType.kBrushed

        self.mainMotor = rev.CANSparkMax(canID_leader, mtype)
        self.mainMotor.setInverted(inverted)
        self.mainController, self.mainEncoder = self.__configureEncoder__(self.mainMotor)
        self.resetDistance()

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
        pos = -self.mainEncoder.getPosition() / self.distance_to_rotations
        return pos

    def resetDistance(self):
        self.mainEncoder.setPosition(0)
        return False

    def setDistance(self, distance):
        rotations = distance * self.distance_to_rotations
        self.mainController.setReference(-rotations, rev.CANSparkMax.ControlType.kSmartMotion)
        return False

class ElevatorModule:
    '''
    REFERENCE: https://github.com/REVrobotics/SPARK-MAX-Examples/blob/master/Java/Position%20Closed%20Loop%20Control/src/main/java/frc/robot/Robot.java
    '''

    elevator_motor: ElevatorSparkMax

    def __init__(self, tol=0.001):
        self.currentPosition = 0
        self.nextPosition = 0
        self.currentLevel = 0
        self.nextLevel = 0
        self.stateChanged = False
        self.tol = tol

    def goToLevel(self, level):
        distance = positionToNextLevel(level)
        self.nextPosition = distance
        self.elevator_motor.setDistance(distance)
        return self.isAtLevel()

    def getDistance(self):
        return self.currentPosition
    
    def updateDistance(self):
        self.currentPosition = self.elevator_motor.getDistance()
        return False

    def isAtLevel(self):
        if abs(self.currentPosition - self.nextPosition) <= self.tol:
            self.currentLevel = self.nextLevel
            return True

        return False

    def execute(self):
        # Update elevator position
        self.updateDistance()

        # Move level if needed
        if self.stateChanged:
            self.goToNextLevel()
            self.stateChanged = False

        pass



        


        

