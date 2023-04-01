from magicbot import AutonomousStateMachine, state, timed_state

from componentsElevator import ElevatorModule as Elevator
from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU
from componentsDrive import DriveTrainModule


class AutonomousMode(AutonomousStateMachine):
    
    MODE_NAME = "Autonomous Mode"
    DEFAULT = True
    elevator : Elevator
    grabber : Grabber
    imu: IMU
    drivetrain : DriveTrainModule

    position = 0
    
    elevator_level = 3
    grabber_level = 2

    def scorePosition(self, elevator_level=4, grabber_level=2):
        self.grabber_level = grabber_level
        self.elevator_level = elevator_level
        self.engage()
        


    # @state(must_finish=True)
    # def turn_90(self):
    #     isFinished = False
    #     isFinished = self.imu.runPID(self, 90)
    #     if isFinished:
    #         self.next_state_now('zero_encoder')
    #         self.cycles+=1


    @state(first = True, must_finish=True)
    def raise_grabber(self):
        if self.elevator.goToLevel(self.elevator_level):
            self.next_state_now('extend_grabber')


    @state(must_finish=True)
    def extend_grabber(self):
        if self.grabber.goToLevel(self.grabber_level):
            self.next_state_now('wait')
    
    @state(must_finish=True)
    def open_grabber(self):
        if self.grabber.openGrabber():
            self.next_state_now('wait')


    @timed_state(duration=3, must_finish=True, next_state='retract_grabber')
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
            self.next_state_now('drive_forward')
            isFinished = True # FIXME: What is this doing? This variable gets destroyed every function call during this state.
    
    
    @state(must_finish = True)
    def drive_forward(self):
        self.drivetrain.setDistance(-3)
        if abs(-3 - self.drivetrain.mainLeft_motor.getDistance()) < .001:
            self.next_state_now('stop')
        
        
    @state(must_finish=True)
    def stop(self):
        self.drivetrain.setArcade(0,0)
        return False

