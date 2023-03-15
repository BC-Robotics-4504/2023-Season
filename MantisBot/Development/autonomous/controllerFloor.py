from magicbot import StateMachine, timed_state, state

# this is one of your components
from componentsElevator import ElevatorModule as Elevator
from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU
from componentsHMI import HMIModule as HMI


class Floor(StateMachine):    
    MODE_NAME = "Floor Pickup Controller"
    DEFAULT = False
    elevator : Elevator
    grabber : Grabber
    imu : IMU
    hmi : HMI

    position = 0
    engaged = False

    def pickUp(self):
        self.engaged = True
        self.engage()

    @state(first = True, must_finish=True) #Elevator Actuation Up
    def raise_grabber1(self):
        if self.elevator.goToLevel(2):
            self.next_state_now('extend_grabber1')
    
    @state(must_finish=True)    #Grabber Actuation Out
    def extend_grabber1(self):
         if self.grabber.goToLevel(1):
             self.next_state_now('lower_grabber1')
             
    @state(must_finish=True)    #Elevator Actuation Down
    def lower_grabber1(self):
        if self.elevator.goToLevel(0):
            self.engaged = False
            self.next_state_now('close_grabber')

    @state(must_finish=True)    #Grabber Closes when Right Trigger is Pressed
    def close_grabber(self):
        if self.hmi.getRightButton(1):
            self.grabber.closeGrabber()
            self.next_state_now('raise_grabber2')
        
    @state(must_finish=True)    #Elevator Actuation Up
    def raise_grabber2(self):
        if self.elevator.goToLevel(2):
            self.next_state_now('retract_grabber2')
            
    @state(must_finish=True) # Grabber Actuation In
    def retract_grabber2(self):
        if self.grabber.goToLevel(0):
            self.next_state_now('lower_grabber2')  

    @state(must_finish=True)    #Elevator Actuation Down
    def lower_grabber2(self):
        if self.elevator.goToLevel(1):
            self.engaged = False
            self.next_state_now('dormant')
    
    @state(must_finish=True) #Dormant State for Controller
    def dormant(self):
        if self.engaged:
            self.next_state_now('raise_grabber1')