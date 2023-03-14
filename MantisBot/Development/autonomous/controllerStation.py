from magicbot import StateMachine, timed_state, state

# this is one of your components
from componentsElevator import ElevatorModule as Elevator
from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU
from componentsHMI import HMIModule as HMI


class Station(StateMachine):    
    MODE_NAME = "Station Controller"
    DEFAULT = False
    elevator : Elevator
    grabber : Grabber
    imu: IMU
    hmi : HMI

    position = 0
    engaged = False

    def score(self):
        self.engaged = True
        self.engage()

    @state(first= True, must_finish=True)    #Grabber opens
    def open_grabber(self):
        if self.grabber.openGrabber():
            self.next_state_now('raise_grabber')
    
    @state(must_finish=True) #Elevator Actuation Up
    def raise_grabber(self):
        if self.elevator.goToLevel(3):
            self.next_state_now('extend_grabber')

    @state(must_finish=True)    #Grabber Actuation Out
    def extend_grabber(self):
        if self.grabber.goToLevel(2):
            self.next_state_now('close_grabber')
        
    @state(must_finish=True)    #Grabber Closes when Left Button 4 is Pressed
    def close_grabber(self):
        if self.hmi.getLeftButton(4):
            self.grabber.closeGrabber()
            self.next_state_now('retract_grabber')

    @state(must_finish=True) #Grabber Actuation In
    def retract_grabber(self):
        if self.grabber.goToLevel(0):
            self.next_state_now('lower_grabber')  

    @state(must_finish=True) #Elevator Actuation Down
    def lower_grabber(self): 
        if self.elevator.goToLevel(0):
            self.engaged = False
            self.next_state_now('wait')

    @state(must_finish=True)    #Waits for Activation
    def wait(self):
        if self.engaged == True:
            self.next_state_now('extend_grabber')