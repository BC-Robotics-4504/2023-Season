from magicbot import AutonomousStateMachine, state, timed_state

# from autonomous.controllerPVAprilTagFollower import AprilTagPVController
# from autonomous.controllerLLAprilTagFollower import AprilTagController

from math import sqrt

# THIS IS CODED TO WORK WITH THE PHOTONVISION MODULE, NOT THE LIMELIGHT
# class AutoMainController(AutonomousStateMachine):

#     APTVController : AprilTagPVController

#     MODE_NAME = "MainAuto"
#     DEFAULT = True

#     @state(first=True)
#     def state_first(self):
#         self.APTVController.engage()