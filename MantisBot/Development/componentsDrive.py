import ctre
import rev 
from wpimath.controller import PIDController

from math import pi

from componentsHMI import FlightStickHMI
from componentsIMU import IMUModule

class ComboSparkMax:
    def __init__(self, canID_leader, canID_followers, motorType='brushless', inverted=False):
        self.canID_leader = canID_leader
        self.canID_followers = canID_followers
        self.inverted = inverted
        self.mainMotor = None
        self.followerMotors = None

        if motorType == 'brushless':
            mtype = rev.CANSparkMaxLowLevel.MotorType.kBrushless
        else:
            mtype = rev.CANSparkMaxLowLevel.MotorType.kBrushed # FIXME!: Is this right?

        self.mainMotor = rev.CANSparkMax(canID_leader, mtype)
        self.mainMotor.setInverted(self.inverted)
        self.mainEncoder = self.mainMotor.getEncoder(rev.SparkMaxRelativeEncoder.Type.kHallSensor, 42)

        followerMotors = []
        for canID in self.canID_followers:
            follower = rev.CANSparkMax(canID, mtype)
            follower.setInverted(self.inverted)
            follower.follow(self.mainMotor)                              
            followerMotors.append(follower)

        self.followerMotors = followerMotors

    def setPercent(self, value):
        self.mainMotor.set(value)
        return False

    def getVelocity(self):
        vel = self.mainEncoder.getVelocity() #rpm
        return vel
    
    def getPosition(self):
        enc = self.mainEncoder.getPosition()
        return enc
#FIXME!: There was a spelling error in getController. Controller was spelled "Contoller"
    def getController(self):
        con = self.mainMotor.getPIDController()
        return con 

    def resetEncoder(self):
        self.mainEncoder.setPosition(0)
        return False

class DriveTrainModule:
    mainLeft_motor: ComboSparkMax
    mainRight_motor: ComboSparkMax
    hmi_interface: FlightStickHMI
    imu : IMUModule

    tol = 0.1
    kP = 0.1
    kI = 1e-4
    kD = 1
    kIz = 0 
    kFF = 0 
    kMaxOutput = 1 
    kMinOutput = -1
    maxRPM = 5700
    maxVel = 2000 # rpm
    minVel = 0
    maxAcc = 1500
    wheelDiameter_in = 2.5

    def __init__(self):
        self.fsR = 0
        self.fsL = 0
        self.changed = False
        self.autoLockout = True
        self.targetDistance = 0
        self.currentDistance = 0
        self.targetAngle = 0
        self.currentAngle = 0
        self.driveControllerActive = False
        self.angleControllerActive = False

    def setup(self):
        self.controllerLeft = self.__setupDistanceController__(self.mainLeft_motor)
        self.controllerRight = self.__setupDistanceController__(self.mainRight_motor)
        self.controllerAngle = PIDController(.035, .03, .0002)

    def __setupDistanceController__(self, motor, smartMotionSlot=0, allowedErr=0):
        controller = motor.getController()
        # set PID coefficients
        controller.setP(self.kP)
        controller.setI(self.kI)
        controller.setD(self.kD)
        controller.setIZone(self.kIz)
        controller.setFF(self.kFF)
        controller.setOutputRange(self.kMinOutput, self.kMaxOutput)
        controller.setSmartMotionMaxVelocity(self.maxVel, smartMotionSlot)
        controller.setSmartMotionMinOutputVelocity(self.minVel, smartMotionSlot)
        controller.setSmartMotionMaxAccel(self.maxAcc, smartMotionSlot)
        controller.setSmartMotionAllowedClosedLoopError(allowedErr, smartMotionSlot)
        return controller

    def setInput(self, fsTuple): # fsTuple = (fsL, fsR)
        self.fsL = fsTuple[0]
        self.fsR = fsTuple[1]
        self.changed = True
        return False

    def getHMIInput(self):
        (self.fsL, self.fsR) = self.hmi_interface.getInput()
        return None

    def getVelocity(self):
        vL = self.mainLeft_motor.getVelocity()
        vR = self.mainRight_motor.getVelocity()
        return (vL, vR)

    def enable_autoLockout(self):
        self.autoLockout = True

    def disable_autoLockout(self):
        self.autoLockout = False

    def is_autoLockoutActive(self):
        return self.autoLockout

    def is_changed(self):
        return self.changed

    def setMotors(self):
        self.mainLeft_motor.setPercent(self.fsL)
        self.mainRight_motor.setPercent(self.fsR)
        self.changed = False
        return False
    
    def setDistance(self, distance_m):
        self.currentDistance = 0
        self.targetDistance = distance_m
        self.controllerLeft.resetController()
        self.controllerRight.resetController()
        self.enable_autoLockout()
        self.distanceControllerActive = True
        self.angleControllerActive = False
        self.stateChanged = True
        return False

    def getDistance(self):
        self.currentDistance = self.mainLeft_motor.getPosition()
        return False
    
    def __setMotorsDistance__(self):
        rotations = self.targetDistance/(self.wheelDiameter_in*25.4e-3*pi)
        self.controllerLeft.setReference(rotations, rev.CANSparkMax.ControlType.kSmartMotion)
        self.controllerRight.setReference(rotations, rev.CANSparkMax.ControlType.kSmartMotion)
    
    def isAtDistance(self):
        if abs(self.currentDistance - self.targetDistance) < self.tol:
            return True          
        return False

    def resetDistanceController(self):
        self.disable_autoLockout()
        self.targetAngle = 0
        self.distanceControllerActive = False    
        return False  
    
    def setAngle(self, angle_rad):
        self.targetAngle = angle_rad
        self.distanceControllerActive = False
        self.angleControllerActive = True
        self.enable_autoLockout()
        self.stateChanged = True
        return False

    def getAngle(self):
        # FIXME: Do we need to address edge case where yaw and current position > 2*pi?
        (yaw, *_) = self.imu.getYPR()
        self.currentAngle = yaw #FIXME: is this in rad or degrees
        return yaw

    def __setMotorsAngle__(self):
        # rotation_speed = self.imuPID.calculate(yaw, self.targetAngle_rad)
        rotation_speed = self.controllerAngle.calculate(self.currentAngle, self.targetAngle)
        self.__setArcade__(0, rotation_speed)
        return False

    def isAtAngle(self):
        if self.controllerAngle.atSetpoint():
            return True
        return False

    def resetAngleController(self):
        self.controllerAngle.reset() #FIXME: Do we need this?
        self.disable_autoLockout()
        self.targetAngle = 0
        self.angleControllerActive = False
        return False

    # Arcade drive code from https://xiaoxiae.github.io/Robotics-Simplified-Website/drivetrain-control/arcade-drive/
    def __setArcade__(self, drive, rotate):
        self.arcadeSpeed = [drive, rotate]
        """Drives the robot using arcade drive."""
        # variables to determine the quadrants
        maximum = max(abs(drive), abs(rotate))
        total, difference = drive + rotate, drive - rotate

        # set speed according to the quadrant that the values are in
        if drive >= 0:
            if rotate >= 0:  # I quadrant
                self.mainLeft_motor.setPercent(maximum)
                self.mainRight_motor.setPercent(difference)
            else:            # II quadrant
                self.mainLeft_motor.setPercent(total)
                self.mainRight_motor.setPercent(maximum)
        else:
            if rotate >= 0:  # IV quadrant
                self.mainLeft_motor.setPercent(total)
                self.mainRight_motor.setPercent(-maximum)
            else:            # III quadrant
                self.mainLeft_motor.setPercent(-maximum)
                self.mainRight_motor.setPercent(difference)

    def abortControllers(self):
        self.distanceControllerActive = False
        self.angleControllerActive = False

    """
    The execute() function is run once each loop in teleopPeriodic
    """
    def execute(self):
        # Always poll current distance and current angle
        self.getDistance()
        self.getAngle()

        if self.is_autoLockoutActive():
            if self.driveControllerActive:

                if self.stateChanged:
                    self.__setMotorsDistance__()
                    self.stateChanged = False

                if self.isAtDistance():              
                    self.resetDistanceController()

            if self.angleControllerActive:

                if self.stateChanged:
                    self.__setMotorsAngle__()
                    self.stateChanged = False

                if self.isAtAngle():
                    self.resetAngleController()

            """Note: An external function needs to call setMotors() function before this will do anything useful"""
            if self.is_changed():
                self.setMotors()
        
        else: 
            self.getHMIInput()
            self.setMotors()



        

