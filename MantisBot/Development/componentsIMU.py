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
        self.YPR = self.imuSensor.getYawPitchRoll()[-1]
        return False
    
    def setRelativeTargetYaw(self, target_yaw):
        self.target_yaw = target_yaw
        return False
    
    def getCurrentYaw(self):
        return self.getYPR()[0]
    
    def getTargetYaw(self):
        return self.target_yaw
    
    def runPID(self, target_heading, tolerance = 5, speed_tolerance = .1):
        if self.target_yaw == 0:
            self.setRelativeTargetYaw(target_heading + self.getCurrentYaw())

        isFinished = False
        yaw = self.getCurrentYaw()
        rotation_speed = self.imuPID.calculate(-yaw, self.target_yaw)
        rotation_speed = self.drivetrain.clamp(rotation_speed, -1, 1)
        print(self.getCurrentYaw(), yaw - self.getCurrentYaw())
        self.drivetrain.setArcade(0, rotation_speed)

        # If angle is reached
        if abs(yaw - target_heading) <= tolerance and abs(rotation_speed) <= speed_tolerance:
            self.imuPID.reset() #TODO: make sure this doesn't break anything
            isFinished = True
            self.setRelativeTargetYaw(0)
        return isFinished

    def execute(self):
        self.updateYPR()

        if self.isEnabled():
            self.updatePID()