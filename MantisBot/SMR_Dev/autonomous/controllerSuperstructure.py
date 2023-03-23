from magicbot import StateMachine, timed_state, state

# this is one of your components
from componentsElevator import ElevatorModule as Elevator
from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU
# from componentsHMI import HMIModule as HMI
from componentsHMI_xbox import HMIModule as HMI



class Superstructure(StateMachine):    
    MODE_NAME = "Superstructure Controller"
    DEFAULT = False
    elevator : Elevator
    grabber : Grabber
    imu: IMU
    hmi : HMI

    position = 0
    engaged = False

    def actuate(self, elevator_level, grabber_level):
        self.grabber_level = grabber_level
        self.elevator_level = elevator_level
        self.engage()

    @state(first= True, must_finish= True)
    def clear_bumper(self):
        self.engaged = True
        isFinished = False
        if self.elevator.getDistance() >= 0.35:
            self.next_state_now('actuate_grabber')
        self.elevator.goToLevel(2)


    @state(must_finish=True)
    def actuate_grabber(self):
        if self.elevator.goToLevel(self.elevator_level) and self.grabber.goToLevel(self.grabber_level):
         self.next_state_now('dormant')

    @state(must_finish=True)    #Waits For Activation
    def dormant(self):
        print("Superstructure in dormant state")
        if self.engaged == True:
            self.next_state_now('clear_bumper')