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

    def getYPR(self):
        return self.YPR
    


    PID = None
    
    def runPID(self, target_heading, tolerance = 15, speed_tolerance = .1):
        isFinished = False
        yaw = self.getYPR()[1][0]
        # Convert degree heading into usuable form
        print(self.YPR)
        self.targetAngle_rad = yaw + radians(target_heading)
    
        rotation_speed = self.imuPID.calculate(yaw, self.targetAngle_rad)
        rotation_speed = self.drivetrain.clamp(rotation_speed, -1, 1)
        self.drivetrain.setArcade(0, rotation_speed)

        # If angle is reached
        if abs(yaw - self.targetAngle_rad) <= radians(tolerance) and abs(rotation_speed) <= speed_tolerance:
            self.imuPID.reset() #TODO: make sure this doesn't break anything
            isFinished = True
        return isFinished

    def execute(self):
        self.YPR = self.imuSensor.getYawPitchRoll()
        pass 
