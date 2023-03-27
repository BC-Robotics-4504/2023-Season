from magicbot import AutonomousStateMachine, state, timed_state

# from componentsElevator import ElevatorModule as Elevator
# from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU
from componentsDrive import DriveTrainModule
from componentsElevator import ElevatorModule as Elevator
from componentsGrabber import GrabberModule as Grabber
from componentsHMI_xbox import HMIModule as HMI


class AutonomousModeLeft(AutonomousStateMachine):
    
    MODE_NAME = "Autonomous Mode Left"
    DEFAULT = False
    # elevator : Elevator
    # grabber : Grabber
    imu: IMU
    drivetrain : DriveTrainModule
    elevator : Elevator
    grabber : Grabber
    imu: IMU
    hmi : HMI

    position = 0
    
    elevator_level = 6
    grabber_level = 2
    # drive_distance = -3.2

    def start(self):
        self.drivetrain.enable_autoLockout()
        self.engage()

    @state(first= True, must_finish= True)
    def close_grabber(self):
        self.drivetrain.resetDistance()
        self.grabber.closeGrabber()
        self.next_state_now('slow_drivetrain')

    @state()
    def slow_drivetrain(self):
        self.drivetrain.setMaxAccel(500)
        self.next_state_now('short_backup')

    @state(must_finish= True)
    def short_backup(self):
        self.isEngaged = True
        if self.drivetrain.goToDistance(-.5):
            self.next_state_now('actuate_grabber_up')

    @state(must_finish=True)
    def actuate_grabber_up(self):
        # isFinished = False
        isElevatorFinished = self.elevator.goToLevel(self.elevator_level)

        if self.elevator.getDistance() >= 0.35: # Wait until grabber is slightly elevated to extend arm--this should not the affect motion profile, like a separate step would

            isGrabberFinished = self.grabber.goToLevel(self.grabber_level)

            if isElevatorFinished and isGrabberFinished:
                self.next_state_now('move_score')
    
    @state(must_finish=True)
    def move_score(self):
        if self.drivetrain.goToDistance(0):
            self.next_state_now('open_grabber')
    
    @state(must_finish = True)
    def open_grabber(self):
        self.grabber.openGrabber()
        self.next_state_now('wait')
    
    @timed_state(duration=1, must_finish= True, next_state='move_backward')
    def wait(self):
        return False

    @state(must_finish=True)
    def move_backward(self):
        self.grabber.goToLevel(0)
        self.elevator.goToLevel(5)
        if self.drivetrain.goToDistance(-3):                
            self.next_state_now('fast_drivetrain')

    @state()
    def fast_drivetrain(self):
        self.drivetrain.setMaxAccel(1500)
        self.next_state_now('dormant')
        
    @state() 
    def dormant(self):
        self.isEngaged = False
        self.drivetrain.setMaxAccel(1500)
        return False