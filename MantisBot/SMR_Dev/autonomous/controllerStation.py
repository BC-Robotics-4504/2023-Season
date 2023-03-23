from magicbot import StateMachine, timed_state, state

# this is one of your components
from componentsElevator import ElevatorModule as Elevator
from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU
# from componentsHMI import HMIModule as HMI
from componentsHMI_xbox import HMIModule as HMI



class Station(StateMachine):    
    MODE_NAME = "Station Controller"
    DEFAULT = False
    elevator : Elevator
    grabber : Grabber
    imu: IMU
    hmi : HMI

    position = 0
    engaged = False

    def pickUp(self):
        self.engage()

    @state(first= True, must_finish= True)
    def inital_raise(self):
        self.engaged = True
        if self.elevator.goToLevel(5):
            self.next_state_now('open_grabber')

    @state(must_finish=True)    #Grabber opens
    def open_grabber(self):
        self.grabber.openGrabber()
        self.next_state_now('raise_structure')
    
    @state(must_finish=True) #Elevator Actuation Up
    def raise_structure(self):
        if self.elevator.goToLevel(3) and self.grabber.goToLevel(2):
            self.next_state_now('close_grabber')
        
    @state(must_finish=True)    #Grabber Closes when Right Trigger is Pressed
    def close_grabber(self):
        if self.hmi.getButton('RT'):
            self.grabber.closeGrabber()
            self.next_state_now('dormant')

    # @timed_state(duration=3, must_finish=True, next_state='retract_grabber')
    # def wait(self):
    #     imuseless = True

    # @state(must_finish=True) #Grabber Actuation In
    # def retract_structure(self):
    #     if self.grabber.goToLevel(0) and self.grabber.goToLevel(0):
    #         self.engaged = False
    #         self.next_state_now('dormant')  

    @state(must_finish=True)    #Waits for Activation
    def dormant(self):
        if self.engaged == True:
            self.next_state_now('inital_raise')