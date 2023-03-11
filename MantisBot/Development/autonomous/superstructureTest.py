from magicbot import AutonomousStateMachine, timed_state, state

# this is one of your components
from componentsElevator import ElevatorModule as Elevator
from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU


class MoveGrabber(AutonomousStateMachine):
    # Injected from the definition in robot.py
    
    MODE_NAME = "Test Superstructure"
    DEFAULT = True
    elevator : Elevator
    grabber : Grabber
    imu: IMU

    @state(first=True, must_finish=True)
    def zero_encoders(self):

        self.next_state_now('raise_grabber')

    @state(must_finish=True)
    def raise_grabber(self):
        dist = 1
        self.elevator.elevator_motor.setDistance(dist)
        if abs(dist-self.elevator.elevator_motor.getDistance()) < .001:
            self.next_state_now('extend_grabber')

    @state(must_finish=True)
    def extend_grabber(self):
        dist = 0.12
        self.grabber.grabber_motor.setDistance(dist)
        if abs(dist-self.grabber.grabber_motor.getDistance()) < .001:
            self.next_state_now('wait')

    @timed_state(duration=4, must_finish=True, next_state='retract_grabber')
    def wait(self):
        imuseless = True
        # self.next_state('retract_grabber')


    @state(must_finish=True)
    def retract_grabber(self):
        dist = 0.01
        self.grabber.grabber_motor.setDistance(dist)
        if abs(dist-self.grabber.grabber_motor.getDistance()) < .001:
            self.next_state_now('lower_grabber')  

    @state(must_finish=True)
    def lower_grabber(self):
        self.elevator.elevator_motor.setDistance(0)
        if abs(-self.elevator.elevator_motor.getDistance()) < .001:
            isFinished = True     

