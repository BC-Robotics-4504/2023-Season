from magicbot import StateMachine, timed_state, state

# this is one of your components
from componentsElevator import ElevatorModule as Elevator
from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU


class ScoreLow(StateMachine):    
    MODE_NAME = "Score Low Contorller"
    DEFAULT = False
    elevator : Elevator
    grabber : Grabber
    imu: IMU

    position = 0
    engaged = False

    def scoreLow(self):
        self.engaged = True
        self.engage()

    @state(first = True, must_finish=True)
    def raise_grabber1(self):
        if self.elevator.goToLevel(1):
            self.next_state_now('extend_grabber1')

    @state(must_finish=True)
    def extend_grabber1(self):
         if self.grabber.goToLevel(1):
             self.next_state_now('lower_grabber1')
             
    @state(must_finish=True)
    def lower_grabber1(self):
        if self.elevator.goToLevel(0):
            self.engaged = False
            self.next_state_now('wait')
            
    @timed_state(duration=2, must_finish=True, next_state='raise_grabber2')
    def wait(self):
        imuseless = True

    @state(must_finish=True)
    def close_grabber(self):
        self.grabber.closeGrabber()
        self.next_state_now('raise_grabber2')
        
    @state(must_finish=True)
    def raise_grabber2(self):
        if self.elevator.goToLevel(1):
            self.next_state_now('retract_grabber2')
            
    @state(must_finish=True)
    def retract_grabber2(self):
        if self.grabber.goToLevel(0):
            self.next_state_now('lower_grabber2')  

    @state(must_finish=True)
    def lower_grabber2(self):
        if self.elevator.goToLevel(0):
            self.engaged = False
            self.next_state_now('dormant')
    
    @state(must_finish=True)
    def dormant(self):
        if self.engaged:
            self.next_state_now('raise_grabber1')