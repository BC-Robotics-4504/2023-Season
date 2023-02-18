from magicbot import AutonomousStateMachine, state, timed_state
from wpimath.controller import PIDController

from componentsVision import VisionModule
from componentsDrive import DriveTrainModule

from controllerPVAprilTagFollower import AprilTagController

from math import sqrt

# THIS IS CODED TO WORK WITH THE PHOTONVISION MODULE, NOT THE LIMELIGHT
class AprilTagController(AutonomousStateMachine):

    MODE_NAME = "AprilTagPhotonvision"
    DEFAULT = True

    @state(first=True)
    def state_first(self):
        AprilTagController.engage()