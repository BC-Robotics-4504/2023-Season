from magicbot import AutonomousStateMachine, state, timed_state

from componentsElevator import ElevatorModule as Elevator
from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU
from componentsDrive import DriveTrainModule

class ResetStructure(AutonomousStateMachine):
   
    MODE_NAME = "Reset Structure"
    DEFAULT = False
    elevator : Elevator
    grabber : Grabber
    engaged = False
    
    def reset(self):
        self.engage

    @state(first = True, must_finish = True)
    def reset_thing(self): 
        self.engaged = True 
        if self.elevator.goToLevel(5) and self.grabber.goToLevel(0):
            self.next_state_now('dormant')

    @state(must_finish = True)
    def dormant(self):
        if self.engaged == True:
            self.next_state_now('reset')


    