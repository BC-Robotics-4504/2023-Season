from magicbot import AutonomousStateMachine, timed_state, state

# this is one of your components
from componentsElevator import ElevatorModule as Elevator
from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU


class DriveForward(AutonomousStateMachine):
    # Injected from the definition in robot.py
    
    MODE_NAME = "Test Superwtructure"
    DEFAULT = True
    elevator : Elevator
    grabber : Grabber
    imu: IMU

    @state(first=True, must_finish=True)
    def zero_encoders(self):
        self.elevator.elevator_motor.resetDistance()
        self.next_state_now('raise_grabber')

    @state(must_finish=True)
    def raise_grabber(self):
        self.elevator.elevator_motor.setDistance(.5)
        if abs(.5-self.elevator.elevator_motor.getDistance()) < .001:
            self.next_state_now('extend_grabber')

    @state(must_finish=True)
    def extend_grabber(self):
        self.grabber.grabber_motor.setDistance(.05)
        if abs(.05-self.grabber.grabber_motor.getDistance()) < .001:
            self.next_state_now('wait')

    @timed_state(must_finish=True, duration=2)
    def wait(self):
        imuseless = True
        self.next_state('retract_grabber')


    @state(must_finish=True)
    def retract_grabber(self):
        self.grabber.grabber_motor.setDistance(.00)
        if abs(-self.grabber.grabber_motor.getDistance()) < .001:
            self.next_state_now('lower_grabber')  

    @state(must_finish=True)
    def lower_grabber(self):
        self.elevator.elevator_motor.setDistance(0)
        if abs(-self.elevator.elevator_motor.getDistance()) < .001:
            isFinished = True     

