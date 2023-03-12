from magicbot import AutonomousStateMachine, timed_state, state

from componentsElevator import ElevatorModule as Elevator
from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU


class Superstructure(AutonomousStateMachine):
    MODE_NAME = "Auto Superstructure Controller"
    DEFAULT = True
    elevator : Elevator
    grabber : Grabber
    imu: IMU

    def score(self, elevator_height = 1, grabber_length = .12):
        self.elevator_height = elevator_height
        self.grabber_length = grabber_length
        self.engage()


    @state(first = True, must_finish=True)
    def raise_grabber(self):
        dist = 1.025
        self.elevator.elevator_motor.setDistance(dist)
        if abs(dist-self.elevator.elevator_motor.getDistance()) < .001:
            self.next_state_now('extend_grabber')

    @state(must_finish=True)
    def extend_grabber(self):
        dist = .12
        self.grabber.grabber_motor.setDistance(dist)
        if abs(dist-self.grabber.grabber_motor.getDistance()) < .001:
            self.next_state_now('wait')

    @timed_state(duration=4, must_finish=True, next_state='retract_grabber')
    def wait(self):
        imuseless = True


    @state(must_finish=True)
    def retract_grabber(self):
        dist = 0.0
        self.grabber.grabber_motor.setDistance(dist)
        if abs(dist-self.grabber.grabber_motor.getDistance()) < .001:
            self.next_state_now('lower_grabber')  

    @state(must_finish=True)
    def lower_grabber(self):
        self.elevator.elevator_motor.setDistance(0)
        if abs(-self.elevator.elevator_motor.getDistance()) < .001:
            isFinished = True #FIXME: What is this doing?

