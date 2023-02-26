from math import sin, cos, pi, radians, degrees
from magicbot import StateMachine, state

from componentsDrive import DriveTrainModule
from componentsVision import VisionModule
from componentsIMU import IMUModule

class ScoreCubeController(StateMachine):
    vision : VisionModule
    drivetrain : DriveTrainModule
    imu : IMUModule

    targetId = None
    new_target = False
    enagaged = False

    X = 0
    Y = 0
    theta = 0

    angleTolerance = 5
    motorTolerance = .2

    def align(self):
        self.engage()

    @ state(first=True, must_finish=True)
    def state_rotateAngle(self):
        # Get values for course when AprilTag is found
        if self.new_target == False:
            self.X = self.vision.getX()
            self.Y = self.vision.getY()
            self.theta = self.vision.getPitch()

            self.targetAngle_rad = self.imu.getYPR() + self.theta   #TODO: figure out if IMU uses degrees or radians

            self.targetId = self.vision.getID()
            self.new_target = True

            if self.Y > 0:
                self.turn90 = 90
            else:
                self.turn90 = -90

        #TODO: edit componentsIMU runPID to conform with the rest of the PID functions
        # Rotate angle theta
        isFinished = self.imu.runPID(self.theta)
        # If angle is reached
        if isFinished:
            self.next_state_now('state_moveFirstLeg')

    @ state(must_finish=True)
    def state_moveFirstLeg(self):
        distance = self.Y
        # Move target_distance
        isFinished = self.drivetrain.setDistance(distance)   #FIXME: Edit setDistance to conform with rest of PID functions
        # If distance is reached
        if isFinished:
            self.next_state_now('state_move90')

    @ state(must_finish=True)
    def state_rotate90(self):
        #TODO: edit componentsIMU runPID to conform with the rest of the PID functions
        # Rotate 90 degrees to roughly align with AprilTag
        isFinished = self.imu.runPID(self.turn90)
        # If angle is reached
        if isFinished:
            self.next_state_now('state_alignTarget')

    def state_alignTarget(self):
        # Correct angle with vision PID
        isFinished = self.vision.runPVAnglePID()
        # If angle is reached
        if isFinished:
            self.next_state_now('state_moveSecondLeg')

    @ state(must_finish=True)
    def state_moveSecondLeg(self):
        distance = self.X()
        # Move target_distance
        isFinished = self.drivetrain.setDistance(distance)   #FIXME: Edit setDistance to conform with rest of PID functions
        # If distance is reached
        if isFinished:
            self.enagaged = False

    def is_engaged(self):
        return self.engaged

    


        
            
        

        

