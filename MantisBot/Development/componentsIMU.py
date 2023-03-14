# import imp
# import wpilib
import ctre
from math import radians #, degrees
from wpimath.controller import PIDController

from componentsDrive import DriveTrainModule


class IMUModule:
    drivetrain: DriveTrainModule
    imuSensor: ctre.Pigeon2

    def __init__(self):
        self.YPR = (0, 0, 0)
        self.imuPID = PIDController(.035, .03, .0002)
        self.target_yaw = 0
        self.yaw_tolerance = 0.01
        self.speed_tolerance = 0.1
        self.enabled = False

    def resetPID(self):
        self.imuPID.reset()
        return False

    def enablePID(self):
        self.enabled = True
        return False
    
    def disablePID(self):
        self.enabled = False
        return False

    def isEnabled(self):
        return self.enabled

    def getYPR(self):
        return self.YPR
    
    def updateYPR(self):
        self.YPR = self.imuSensor.getYawPitchRoll()
        return False
    
    def setRelativeTargetYaw(self, target_yaw):
        self.target_yaw = target_yaw
        return False
    
    def getCurrentYaw(self):
        return self.YPR[0]
    
    def getTargetYaw(self):
        return self.target_yaw
    
    def goToAngle(self, angle):
        self.setRelativeTargetYaw(angle)
        self.enablePID()
        return self.isAtAngle()
    
    def isAtAngle(self):
        yaw = self.getCurrentYaw()
        target_yaw = self.getTargetYaw()
        if abs(yaw - target_yaw) <= self.yaw_tolerance:
            self.disablePID()
            return True
        return False
    
    def updatePID(self):
        yaw = self.getCurrentYaw()
        target_yaw = self.getTargetYaw()
        rotation_speed = self.imuPID.calculate(yaw, target_yaw)
        rotation_speed = self.drivetrain.clamp(rotation_speed, -1, 1)
        self.drivetrain.setArcade(0, rotation_speed)
        self.isAtAngle() #TODO: determine if we need the speed tolerance check
        return False
    
    # def runPID(self, target_heading, tolerance = 5, speed_tolerance = .1):
    #     isFinished = False

    #     # Convert degree heading into usuable form
    #     self.targetAngle_rad = self.getYPR() + radians(target_heading)

    #     yaw = self.getYPR()[0]
    #     rotation_speed = self.imuPID.calculate(yaw, self.targetAngle_rad)
    #     rotation_speed = self.drivetrain.clamp(rotation_speed, -1, 1)
    #     self.drivetrain.setArcade(0, rotation_speed)

    #     # If angle is reached
    #     if abs(yaw - self.targetAngle_rad) <= tolerance and abs(rotation_speed) <= speed_tolerance:
    #         self.imuPID.reset() #TODO: make sure this doesn't break anything
    #         isFinished = True
    #     return isFinished

    def execute(self):
        self.updateYPR()

        if self.isEnabled():
            self.updatePID()