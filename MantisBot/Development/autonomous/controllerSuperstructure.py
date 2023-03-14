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
    engaged = False

    def scorePosition(self, elevator_level, grabber_level):
        self.grabber_level = grabber_level
        self.elevator_level = elevator_level
        self.engaged = True
        self.engage()

    @state(first = True, must_finish=True)
    def raise_grabber(self):
        if self.elevator.goToLevel(self.elevator_level):
            self.next_state_now('extend_grabber')

    @state(must_finish=True)
    def extend_grabber(self):
        if self.grabber.goToLevel(self.grabber_level):
            self.next_state_now('wait')

    @timed_state(duration=4, must_finish=True, next_state='retract_grabber')
    def wait(self):
        imuseless = True
        # self.next_state('retract_grabber')

    @state(must_finish=True)
    def retract_grabber(self):
        if self.grabber.goToLevel(0):
            self.next_state_now('lower_grabber')  

    @state(must_finish=True)
    def lower_grabber(self):
        if self.elevator.goToLevel(0):
            self.next_state_now('wait')
    
    @state(must_finish=True)
    def wait(self):
        if self.engaged:
            self.next_state('raise grabber')

