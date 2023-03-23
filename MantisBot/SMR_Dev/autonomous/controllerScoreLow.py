from magicbot import StateMachine, timed_state, state

# this is one of your components
from componentsElevator import ElevatorModule as Elevator
from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU
# from componentsHMI import HMIModule as HMI
from componentsHMI_xbox import HMIModule as HMI



class ScoreLow(StateMachine):    
    MODE_NAME = "Score Low Contorller"
    DEFAULT = False
    elevator : Elevator
    grabber : Grabber
    imu : IMU
    hmi : HMI

    position = 0
    engaged = False

    def score(self):
        self.engage()

    @state(first= True, must_finish= True)
    def inital_raise(self):
        self.engaged = True
        if self.elevator.goToLevel(5):
            self.next_state_now('deploy_arm')

    @state(must_finish=True) #Elevator Actuation Up
    def deploy_arm(self):
        if self.elevator.goToLevel(1) and self.grabber.goToLevel(2):
            self.next_state_now('lower_arm')
             
    @state(must_finish=True)    #Elevator Actuation Down
    def lower_arm(self):
        if self.elevator.goToLevel(0):
            self.engaged = False
            self.next_state_now('open_grabber')

    @state(must_finish=True)    #Grabber Opens when Left Trigger is Pressed
    def open_grabber(self):
        if self.hmi.getButton('LT'):
            self.grabber.openGrabber()
            self.next_state_now('raise_arm')
        
    @state(must_finish=True)    #Elevator Actuation Up
    def raise_arm(self):
        if self.elevator.goToLevel(2):
            self.next_state_now('retract_grabber2')
            
    @state(must_finish=True) # Grabber Actuation In
    def retract_grabber2(self):
        if self.grabber.goToLevel(0):
            self.next_state_now('lower_grabber2')  

    @state(must_finish=True)    #Elevator Actuation Down
    def lower_grabber2(self):
        if self.elevator.goToLevel(0):
            self.engaged = False
            self.next_state_now('dormant')
    
    @state(must_finish=True) #Dormant State for Controller
    def dormant(self):
        if self.engaged:
            self.next_state_now('inital_raise')