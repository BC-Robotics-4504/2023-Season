from magicbot import StateMachine, timed_state, state

# this is one of your components
from componentsElevator import ElevatorModule as Elevator
from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU


class Superstructure(StateMachine):    
    MODE_NAME = "Superstructure Controller"
    DEFAULT = False
    elevator : Elevator
    grabber : Grabber
    imu: IMU

    position = 0

    def setScoringPosition(self, elevator_level, grabber_level):
        self.grabber_level = grabber_level
        self.elevator_level = elevator_level

    def score(self):
        self.engage()

    @state(first = True, must_finish=True)
    def raise_grabber(self):
        self.elevator.goToLevel(self.elevator_level)
        if self.elevator.isAtLevel():
            self.next_state_now('extend_grabber')

    @state(must_finish=True)
    def extend_grabber(self):
        self.grabber.goToLevel(self.grabber_level)
        if self.grabber.isAtLevel():
            self.next_state_now('wait')

    @timed_state(duration=4, must_finish=True, next_state='retract_grabber')
    def wait(self):
        imuseless = True
        # self.next_state('retract_grabber')

    @state(must_finish=True)
    def retract_grabber(self):
        self.grabber.goToLevel(0)
        if self.grabber.isAtLevel():
            self.next_state_now('lower_grabber')  

    @state(must_finish=True)
    def lower_grabber(self):
        self.elevator.goToLevel(0)
        if self.elevator.isAtLevel():
            isFinished = True # FIXME: What is this doing? This variable gets destroyed every function call during this state.

