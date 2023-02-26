from math import sin, cos, pi, radians, degrees
from magicbot import StateMachine, state

from componentsDrive import DriveTrainModule
from componentsPhotonVision import PhotonVisionModule
from componentsIMU import IMUModule

class ParkingController(StateMachine):
    photonvision : PhotonVisionModule
    drivetrain : DriveTrainModule
    imu : IMUModule

    MODE_NAME = "ParkAprilTag"
    DEFAULT = False
    isEngaged = False

    targetId = None
    new_target = False
    isEnagaged = False

    X = 0
    Y = 0
    theta = 0

    angleTolerance = 5
    motorTolerance = .2

    def park(self):
        self.engage()

    @ state(first=True, must_finish=True)
    def state_rotateAngle(self):
        # Get values for course when AprilTag is found
        if self.new_target == False:
            self.X = self.photonvision.getX()
            self.Y = self.photonvision.getY()
            self.theta = self.photonvision.getPitch()

            self.targetAngle_rad = self.imu.getYPR()[0] + self.theta   #TODO: figure out if IMU uses degrees or radians

            self.targetId = self.photonvision.getID()
            self.new_target = True

            if self.Y > 0:
                self.turn90 = 90
            else:
                self.turn90 = -90

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

    @ state(must_finish=True)
    def state_alignTarget(self):
        # Correct angle with photonvision PID
        isFinished = self.photonvision.runAnglePID()
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

    


        
            
        

        

