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


    def setup(self, tagID=3, goalRange=2):
        self.goalRange = goalRange
        self.tagID = tagID
        self.isFinished = False

    @state(first=True)
    def follow(self):
        if self.vision.hasTargets():
            self.vision.runPVAnglePID(5, .1)
            # self.isFinished = self.vision.runPVLinearPID(self.goalRange, .05, .1)
            print(self.drivetrain.getArcadeLinear(), self.drivetrain.getArcadeRotation())

        else:
            self.drivetrain.setArcade(0,0)

        if self.isFinished:
            self.next_state_now('stop')

        
        
    @state()
    def stop(self):
        self.drivetrain.setLeft(0)
        self.drivetrain.setRight(0)
        return False