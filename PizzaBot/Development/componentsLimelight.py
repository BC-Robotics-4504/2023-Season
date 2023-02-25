from networktables import NetworkTables
from photonvision import PhotonCamera, PhotonUtils
from math import radians, degrees
from wpimath.controller import PIDController

from componentsDrive import DriveTrainModule


class LimelightModule:
    drivetrain: DriveTrainModule
    camera: PhotonCamera

    def __init__(self, camera_height_m=.3, target_height_m=.3, camera_pitch_rad=0, goal_range_m=0):
        self.camera_height = camera_height_m
        self.target_height = target_height_m
        self.camera_pitch = camera_pitch_rad
        self.goal_range = goal_range_m
        self.result = None

        self.table = NetworkTables.getTable("limelight")
        self.hasTargets = bool(self.table.getNumber('tv',None))
        self.targetX = self.table.getNumber('tx',None)
        self.targetY = self.table.getNumber('ty',None)
        self.targetArea = self.table.getNumber('ta',None)
        # targetSkew = table.getNumber('ts',None)

        self.LLAnglePID = PIDController(.035, .03, .0002)
        self.LLLinearPID = PIDController(.035, .03, .0002)



    def getRange(self):
        if self.hasTargets:
            target_pitch = self.targetX
            target_range = PhotonUtils.calculateDistanceToTarget(self.camera_height, 
                                                                self.target_height, 
                                                                self.camera_pitch,
                                                                target_pitch)
            return target_range
        else:
            return None

    def getX(self):
        if self.hasTargets:
            return self.targetX
        else:
            return None

    def getY(self):
        if self.hasTargets:
            return self.targetY
        else:
            return None  

    #TODO: find out how to get target ID via networktables
    # def getID(self):
    #     if self.result is not None:
    #         if self.hasTargets():
    #             id = self.result.getBestTarget().getFiducialId()
    #             return id
    #         else:
    #             return None

    def hasTargets(self):
        return self.hasTargets

    def runLLAnglePID(self, tolerance, speed_tolerance):
            isFinished = False

            yaw = self.getX()
            rotation_speed = self.LLAnglePID.calculate(yaw, 0)
            rotation_speed = self.drivetrain.clamp(rotation_speed, -1, 1)
            self.drivetrain.setArcade(self.drivetrain.getArcadeLinear(), rotation_speed)

            # If angle is reached
            if abs(yaw) <= tolerance and abs(rotation_speed) <= speed_tolerance:
                self.LLAnglePID.reset()
                isFinished = True
            return isFinished

    def runLLLinearPID(self, target_range, tolerance, speed_tolerance):
        isFinished = False

        # Calculate PID output and update motors
        linear_speed = self.LLLinearPID.calculate(range, target_range)
        linear_speed = self.drivetrain.clamp(linear_speed, -1, 1)
        self.drivetrain.setArcade(linear_speed, self.drivetrain.getArcadeRotation())

        # If angle is reached
        if abs(range) <= tolerance and abs(linear_speed) <= speed_tolerance:
            self.LLLinearPID.reset()
            isFinished = True
        return isFinished

    def execute(self):
        result = self.camera.getLatestResult()
        self.result = result
        pass



    def execute(self):
        self.hasTargets = bool(self.table.getNumber('tv',None))
        self.targetX = self.table.getNumber('tx',None)
        self.targetY = self.table.getNumber('ty',None)
        self.targetArea = self.table.getNumber('ta',None)
        pass