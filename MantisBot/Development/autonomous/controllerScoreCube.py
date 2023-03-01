from math import sin, cos, pi, radians, degrees
from magicbot import StateMachine, state, AutonomousStateMachine

from componentsDrive import DriveTrainModule
from componentsPhotonVision import PhotonVisionModule
from componentsIMU import IMUModule

from autonomous.controllerParkAprilTag import ParkingController

class ScoreCubeController(StateMachine):
    photonvision : PhotonVisionModule
    drivetrain : DriveTrainModule
    imu : IMUModule

    parking_controller : ParkingController
    ParkingController.MODE_NAME = 'ScoreCube>ParkingController'
    ParkingController.DEFAULT = False

    MODE_NAME = "ScoreCube"
    DEFAULT = False
    isEngaged = False

    targetId = None
    new_target = False
    enagaged = False

    X = 0
    Y = 0
    theta = 0

    angleTolerance = 5
    motorTolerance = .2

    # 1. Align
    # 2. Move arm to desired location
    # 3. extend grabber
    # 4. drop piece
    # 5. retract grabber
    # 6. retract arm

    def score(self):
        self.engage()


    @ state(first=True, must_finish=True)
    def state_moveToGoal(self):
        self.parking_controller.park()
        # if self.parkingController.isEngaged == False:
        #     self.next_state_now('state_raiseArm')


    @ state(must_finish=True)
    def state_raiseArm(self):
        imUseless = True
        

    def is_engaged(self):
        return self.engaged

    


        
            
        

        

