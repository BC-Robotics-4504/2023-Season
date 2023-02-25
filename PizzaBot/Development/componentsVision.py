from photonvision import PhotonCamera, PhotonUtils
from math import pi, radians
from wpimath.controller import PIDController

from componentsDrive import DriveTrainModule
class VisionModule:

    drivetrain: DriveTrainModule
    camera: PhotonCamera

    def __init__(self, camera_height_m=0.17, target_height_m=0.1524, camera_pitch_rad=0, goal_range_m=1):
        self.camera_height = camera_height_m
        self.target_height = target_height_m
        self.camera_pitch = camera_pitch_rad
        self.goal_range = goal_range_m
        self.result = None

        self.PVAnglePID = PIDController(.035, .03, .0002)
        self.PVLinearPID = PIDController(.035, .2, .0002)

    def getRange(self):
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

    def runPVAnglePID(self, tolerance, speed_tolerance):
        isFinished = False

        yaw = self.getYaw()
        rotation_speed = self.PVAnglePID.calculate(yaw, 0)
        rotation_speed = self.drivetrain.clamp(rotation_speed, -1, 1)
        self.drivetrain.setArcade(self.drivetrain.getArcadeLinear(), rotation_speed)

        # If angle is reached
        if abs(yaw) <= tolerance and abs(rotation_speed) <= speed_tolerance:
            self.PVAnglePID.reset()
            isFinished = True
        return isFinished

    def runPVLinearPID(self, target_range, tolerance, speed_tolerance):
        isFinished = False

        # Calculate PID output and update motors
        trange = -(self.getRange())
        linear_speed = self.PVLinearPID.calculate(trange, target_range)
        # linear_speed = self.drivetrain.clamp(linear_speed, -1, 1)
        # print(f"target_range = {target_range}/+-{tolerance}")
        # print(f"range = {range}")
        # print("Lspeed = " + str(linear_speed))
        self.drivetrain.setArcade(-(linear_speed), self.drivetrain.getArcadeRotation())
        error = trange - target_range
        print(trange, target_range, error)
        print(self.result.getBestTarget().getPitch())
        # If angle is reached
        # if abs(error) <= tolerance and abs(linear_speed) <= speed_tolerance:
        if abs(error) <= tolerance:

            self.PVLinearPID.reset()
            isFinished = True
            print('finished')
        return isFinished


    def execute(self):
        result = self.camera.getLatestResult()
        self.result = result
        pass