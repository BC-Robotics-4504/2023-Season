from magicbot import StateMachine, timed_state, state

# this is one of your components
from componentsElevator import ElevatorModule as Elevator
from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU


class MoveGrabber(StateMachine):
    # Injected from the definition in robot.py
    
    MODE_NAME = "Test Superstructure"
    DEFAULT = False
    elevator : Elevator
    grabber : Grabber
    imu: IMU

    def score(self, elevator_height = 1, grabber_length = .12):
        self.elevator_height = elevator_height
        self.grabber_length = grabber_length
        self.engage()


    @state(first = True, must_finish=True)
    def raise_grabber(self):
        dist = self.elevator_height
        self.elevator.elevator_motor.setDistance(dist)
        if abs(dist-self.elevator.elevator_motor.getDistance()) < .001:
            self.next_state_now('extend_grabber')

    @state(must_finish=True)
    def extend_grabber(self):
        dist = self.grabber_length
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

