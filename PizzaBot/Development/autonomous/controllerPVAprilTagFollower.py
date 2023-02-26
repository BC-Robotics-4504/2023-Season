from magicbot import state, timed_state, StateMachine, AutonomousStateMachine
from wpimath.controller import PIDController

from componentsPhotonVision import PhotonVisionModule
from componentsDrive import DriveTrainModule

from math import sqrt

# THIS IS CODED TO WORK WITH THE PHOTONVISION MODULE, NOT THE LIMELIGHT
class PVAprilTagFollowerController(AutonomousStateMachine):

    MODE_NAME = "AprilTagPhotonVision"
    DEFAULT = False
    isEngaged = False

    drivetrain : DriveTrainModule
    photonvision : PhotonVisionModule

    def setup(self, tagID=3, goalRange=1):
        self.goalRange = goalRange
        self.tagID = tagID

    @state(first=True)
    def follow(self):
        self.isEngaged = True
        isFinished = False
        if self.photonvision.hasTargets():
            self.drivetrain.enable_autoLockout()
            self.photonvision.runAnglePID(5, .1)
            isFinished = self.photonvision.runLinearPID(self.goalRange, .2, .3)
            # print(self.drivetrain.getArcadeLinear(), self.drivetrain.getArcadeRotation())
            # print(self.photonvision.getYaw(), self.photonvision.getRange(), self.goalRange)
        
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
        # print("fin")
        # print(self.photonvision.getX())
        return False