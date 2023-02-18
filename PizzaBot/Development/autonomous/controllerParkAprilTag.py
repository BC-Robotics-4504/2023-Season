from math import sin, cos, pi, radians, degrees
from magicbot import StateMachine, state

from componentsDrive import DriveTrainModule
from componentsVision import VisionModule
from componentsIMU import IMUModule
from wpimath.controller import PIDController


# from drivetrainController import DriveControl

class ParkAprilTagController(StateMachine):
    vision : VisionModule
    drivetrain : DriveTrainModule
    imu : IMUModule

    targetAngle_rad = None
    negative_pitch = False
    targetDistance_m = None
    targetId = None
    new_target = False
    enagaged = False
    offset = 0

    def align(self, offset_m):
        if self.engaged == False:
            self.enagaged = True
            self.offset_m = offset_m

        self.engage()

    kP_imu = .035
    kI_imu = .03
    kD_imu = .0002
    tolerance_rotateAngle = radians(5) 
    tolerance_rotate90 = radians(30) 
    motor_tolerance = .25
    anglePID = None
    def setup(self):
        self.anglePID = PIDController(self.kP_imu, self.kI_imu, self.kD_imu)

    def clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)


    state(first=True, must_finish=True)
    def state_rotateAngle(self):

        # Identify pitch of target apriltag
        if self.new_target == False:
            self.targetAngle_rad = self.imu.getYPR() + radians(self.vision.getPitch())
            self.targetDistance_m = self.vision.getRange()
            self.targetId = self.vision.getID()
            self.new_target = True

            if self.vision.getPitch() < 0:
                self.negative_pitch = True
            else:
                self.negative_pitch = False

        # Setup PID controller for IMU yaw
        yaw = self.imu.getYPR()[0]
        rotation_speed = self.anglePID.calculate(yaw, self.targetAngle_rad)
        rotation_speed = self.clamp(rotation_speed, -1, 1)
        self.drivetrain.setArcade(0, rotation_speed)

        # If angle is reached
        if abs(yaw - self.targetAngle_rad) <= self.tolerance_rotateAngle and abs(rotation_speed) <= self.motor_tolerance:
            self.anglePID.reset() #TODO: make sure this doesn't break anything
            self.next_state_now('state_moveFirstLeg')

    state(must_finish=True)
    def state_moveFirstLeg(self):
        target_distance = self.targetDistance_m*cos(self.targetAngle_rad)

        # Move target_distance
        self.drivetrain.setDistance(target_distance)

        # If distance is reached
        if self.drivetrain.isAtDistance():
            self.next_state_now('state_move90')

    state(must_finish=True)
    def state_rotate90(self):
        #set PID controller for motor angle 90 degrees
        yaw = self.imu.getYPR()[0]
        rotation_speed = self.anglePID.calculate(yaw, radians(90)*self.negative_pitch)
        rotation_speed = self.clamp(rotation_speed, -1, 1)
        self.drivetrain.setArcade(0, rotation_speed)

        # If angle is reached
        if abs(yaw - self.targetAngle_rad) <= self.tolerance_rotate90 and abs(rotation_speed) <= self.motor_tolerance:
            self.next_state_now('state_alignTarget')

    def state_alignTarget(self):

        # Correct angle with PID controller

        # If angle is reached
        self.next_state_now('state_moveSecondLeg')

    state(must_finish=True)
    def state_moveSecondLeg(self):
        target_distance = self.targetDistance_m*sin(self.targetAngle_rad)
        target_distance -= self.offset_m

        # Move target_distance
        self.drivetrain.setDistance(target_distance)

        # If distance is reached
        if self.drivetrain.isAtDistance():            
            self.engaged = False

    def is_engaged(self):
        return self.engaged

    


        
            
        

        

