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

    goalRange = 0

    def setup(self, tagID=3, goalRange=2):
        self.goalRange = goalRange
        self.tagID = tagID

    @state(first=True)
    def follow(self):
        if self.vision.hasTargets():
            self.vision.runPVAnglePID(5, .1)
            self.vision.runPVLinearPID(self.goalRange, .05, .1)

        else:
            self.drivetrain.setArcade(0,0)
        
    @state()
    def stop(self):
        self.drivetrain.setLeft(0)
        self.drivetrain.setRight(0)
        return False