from magicbot import state, timed_state, StateMachine, AutonomousStateMachine
from wpimath.controller import PIDController

from componentsVision import VisionModule
from componentsDrive import DriveTrainModule

from math import sqrt

# THIS IS CODED TO WORK WITH THE PHOTONVISION MODULE, NOT THE LIMELIGHT
class AprilTagPVController(AutonomousStateMachine):

    MODE_NAME = "AprilTagPhotonVision"
    DEFAULT = True

    drivetrain : DriveTrainModule
    vision : VisionModule


    def setup(self, tagID=3, goalRange=3):
        self.goalRange = goalRange
        self.tagID = tagID

    @state(first=True)
    def follow(self):
        isFinished = False
        self.lowest_value = 0
        self.highest_value = 0
        if self.vision.hasTargets():
            self.drivetrain.enable_autoLockout()
            self.vision.runPVAnglePID(5, .1)
            isFinished = self.vision.runPVLinearPID(self.goalRange, .1, .1)
            # print(self.drivetrain.getArcadeLinear(), self.drivetrain.getArcadeRotation())
            # print(self.vision.getYaw(), self.vision.getRange(), self.goalRange)
        




        else:
            self.drivetrain.setArcade(0,0)
            self.drivetrain.disable_autoLockout()


        if isFinished:
            self.next_state_now('stop')

        
        
    @state()
    def stop(self):
        self.drivetrain.setLeft(0)
        self.drivetrain.setRight(0)
        self.drivetrain.disable_autoLockout()
        return False