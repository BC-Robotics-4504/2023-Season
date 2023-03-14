from magicbot import AutonomousStateMachine, timed_state, state

from componentsElevator import ElevatorModule as Elevator
from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU
from componentsDrive import DriveTrainModule as DriveTrain

class Superstructure(AutonomousStateMachine):
    MODE_NAME = "Auto Superstructure Controller"
    DEFAULT = False

    elevator : Elevator
    grabber : Grabber
    imu: IMU
    drivetrain = DriveTrain

    def score(self):
        self.engage()


    @state(first = True, must_finish=True)
    def raise_grabber(self):
        if self.elevator.goToLevel(3):
            self.next_state_now('extend_grabber')

    @state(must_finish=True)
    def extend_grabber(self):
        if self.grabber.goToLevel(2):
            self.next_state_now('wait')

    @timed_state(duration=4, must_finish=True, next_state='retract_grabber')
    def wait(self):
        imuseless = True

    @state(must_finish=True)
    def retract_grabber(self):
        if self.grabber.goToLevel(0):
            self.next_state_now('lower_grabber')  

    @state(must_finish=True)
    def lower_grabber(self):
        if self.elevator.goToLevel(0):
            isFinished = True #FIXME: What is this doing?
    
    # TODO: add code here to continue drivetrain routine

    # @state(must_finish=True)
    # def turn_to_charging_station(self):
    #     # TODO: Add in code here to facilitate turning a certain angle
    
    # @state(must_finish=True)
    # def move_to_charging_station(self):
    #     dist = 10
    #     self.drivetrain.setDistance(dist)
