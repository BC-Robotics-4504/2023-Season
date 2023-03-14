from magicbot import StateMachine, timed_state, state

# this is one of your components
from componentsElevator import ElevatorModule as Elevator
from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU
from componentsHMI import HMIModule as HMI


class ScoreHigh(StateMachine):    
    MODE_NAME = "Score High Controller"
    DEFAULT = False
    elevator : Elevator
    grabber : Grabber
    imu: IMU
    hmi : HMI

    position = 0
    engaged = False

    def score(self):
        self.grabber_level = 2
        self.elevator_level = 3
        self.engaged = True
        self.engage()

    @state(first = True, must_finish=True)  #Elevator Actuation Up
    def raise_grabber(self):
        if self.elevator.goToLevel(self.elevator_level):
            self.next_state_now('extend_grabber')

    @state(must_finish=True)    #Grabber Actuation Out
    def extend_grabber(self):
        if self.grabber.goToLevel(self.grabber_level):
            self.next_state_now('wait_for_confirm')

    @state(must_finish=True)    #Grabber Opens when left trigger is Pressed
    def wait_for_confirm(self):
        if self.hmi.getLeftButton(1):
            self.grabber.openGrabber()
            self.next_state('retract_grabber')

    @state(must_finish=True)    #Grabber Actuation In
    def retract_grabber(self):
        if self.grabber.goToLevel(0):
            self.next_state_now('lower_grabber')  

    @state(must_finish=True)    #Elevator Actuation Down
    def lower_grabber(self):
        if self.elevator.goToLevel(0):
            self.engaged = False
            self.next_state_now('dormant')

    @state(must_finish=True)    #Waits For Activation
    def dormant(self):
        if self.engaged == True:
            self.next_state_now('raise_grabber')