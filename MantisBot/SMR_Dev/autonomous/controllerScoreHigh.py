from magicbot import StateMachine, timed_state, state

# this is one of your components
from componentsElevator import ElevatorModule as Elevator
from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU
# from componentsHMI import HMIModule as HMI
from componentsHMI_xbox import HMIModule as HMI



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
        self.elevator_level = 4
        self.engage()

    @state(first= True, must_finish= True)
    def inital_raise(self):
        self.engaged = True
        if self.elevator.goToLevel(5):
            self.next_state_now('raise_structure')

    @state(must_finish=True) #Elevator Actuation Up
    def raise_structure(self):
        if self.elevator.goToLevel(self.elevator_level) and self.grabber.goToLevel(self.grabber_level):
         self.next_state_now('wait_for_confirm')

    @state(must_finish=True)    #Grabber Opens when left trigger is Pressed
    def wait_for_confirm(self):
        if self.hmi.getButton('LT'):
            self.grabber.openGrabber()
            self.next_state('dormant')

    # @state(must_finish=True) #Elevator Actuation Up
    # def lower_structure(self):
    #  if self.elevator.goToLevel(0) and self.grabber.goToLevel(0):
    #     self.engaged = False 
    #     self.next_state_now('dormant')

    @state(must_finish=True)    #Waits For Activation
    def dormant(self):
        if self.engaged == True:
            self.next_state_now('inital_raise')