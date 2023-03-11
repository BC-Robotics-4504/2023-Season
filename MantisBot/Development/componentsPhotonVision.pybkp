from photonvision import PhotonCamera, PhotonUtils
from math import pi, radians
from wpimath.controller import PIDController

from componentsDrive import DriveTrainModule
class PhotonVisionModule:

    drivetrain: DriveTrainModule
    camera: PhotonCamera

    def __init__(self, camera_height_m=0.17, target_height_m=0.1524, camera_pitch_rad=0, goal_range_m=1):
        self.camera_height = camera_height_m
        self.target_height = target_height_m
        self.camera_pitch = camera_pitch_rad
        self.goal_range = goal_range_m
        self.result = None

        self.anglePID = PIDController(.035, .03, .0002)
        self.linearPID = PIDController(.4, .03, .0002)

    def getRange(self): # DEPRICATED? USE getX
        if self.result.hasTargets():
            target_pitch_deg = self.result.getBestTarget().getPitch()
            # target_pitch_deg = self.result.getBestTarget().getYaw()
            target_pitch_rad = target_pitch_deg/180*2*pi
            target_range = PhotonUtils.calculateDistanceToTarget(self.camera_height, 
                                                                self.target_height, 
                                                                self.camera_pitch,
                                                                target_pitch_rad)
            return target_range
        else:
            return None

    def getYaw(self):
        if self.result.hasTargets():
            yaw = self.result.getBestTarget().getYaw()
            return yaw
        else:
            return None
    def getPitch(self):
        if self.result.hasTargets():
            yaw = self.result.getBestTarget().getPitch()
            return yaw
        else:
            return None    
    def getX(self):
        if self.result.hasTargets():
            X = self.result.getBestTarget().getBestCameraToTarget().X()
            return X
        else:
            return None  
    def getY(self):
        if self.result.hasTargets():
            Y = self.result.getBestTarget().getBestCameraToTarget().X()
            return Y
        else:
            return None  
    def getID(self):
        if self.result is not None:
            if self.result.hasTargets():
                id = self.result.getBestTarget().getFiducialId()
                return id
            else:
                return None
    def hasTargets(self):
        if self.result == None:
            return False
        return self.result.hasTargets()

    def runAnglePID(self, tolerance = 5, speed_tolerance = .1):
        isFinished = False
        yaw = self.getYaw()
        rotation_speed = self.anglePID.calculate(yaw, 0)
        rotation_speed = self.drivetrain.clamp(rotation_speed, -1, 1)
        self.drivetrain.setArcade(self.drivetrain.getArcadeLinear(), rotation_speed)

        # If angle is reached
        if abs(yaw) <= tolerance and abs(rotation_speed) <= speed_tolerance:
            self.anglePID.reset()
            isFinished = True
        return isFinished

    def runLinearPID(self, target_range = .5, tolerance = .1, speed_tolerance = .1):
        isFinished = False
        # Calculate PID output and update motors
        X = self.getX()
        linear_speed = self.linearPID.calculate(X, target_range)
        linear_speed = self.drivetrain.clamp(linear_speed, -1, 1)
        self.drivetrain.setArcade(linear_speed, self.drivetrain.getArcadeRotation())
        error = X - target_range
        print(X, target_range, error)
        print(self.result.getBestTarget().getPitch())

        # If angle is reached
        if abs(error) <= tolerance and abs(linear_speed) <= speed_tolerance:
            self.linearPID.reset()
            isFinished = True
        return isFinished


    def execute(self):
        result = self.camera.getLatestResult()
        self.result = result
        pass