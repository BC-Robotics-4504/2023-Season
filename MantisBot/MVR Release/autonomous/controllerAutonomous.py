from magicbot import AutonomousStateMachine, state, timed_state

# from componentsElevator import ElevatorModule as Elevator
# from componentsGrabber import GrabberModule as Grabber
from componentsIMU import IMUModule as IMU
from componentsDrive import DriveTrainModule


class AutonomousMode(AutonomousStateMachine):
    
    MODE_NAME = "Autonomous Mode"
    DEFAULT = True
    # elevator : Elevator
    # grabber : Grabber
    imu: IMU
    drivetrain : DriveTrainModule

    position = 0
    
    # elevator_level = 4
    # grabber_level = 2
    drive_distance = -3.2

    def start(self):
        self.engaged = True
        self.engage()

    @state(first = True, must_finish = True)
    def drive_backwards(self):
        print('[7] Drive')
        if self.drivetrain.goToDistance(self.drive_distance):
            print('    ...completes.')
            self.next_state('stop')
        return False
        
        
    @state(must_finish=True)
    def stop(self):
        print('[8] Complete.')
        self.drivetrain.setArcade(0,0)
        return False

    # def scorePosition(self, elevator_level=4, grabber_level=2, drive_distance=-3.):
    #     self.grabber_level = grabber_level
    #     self.elevator_level = elevator_level
    #     self.drive_distance = drive_distance
    #     self.engage()

    # @state(first=True, must_finish=True)
    # def close_grabber(self):
    #     print('[0] Close Grabber')
    #     if self.grabber.closeGrabber():
    #         print('    ...complete.')
    #         self.next_state_now('raise_grabber')
            
    # @state(must_finish=True)
    # def raise_grabber(self):
    #     print('[1] Raise Grabber')
    #     if self.elevator.goToLevel(self.elevator_level):
    #         print('    ...complete.')
    #         self.next_state_now('extend_grabber')

    # @state(must_finish=True)
    # def extend_grabber(self):
    #     print('[2] Extend Grabber')
    #     if self.grabber.goToLevel(self.grabber_level):
    #         print('    ...completes.')
    #         self.next_state_now('open_grabber')
    
    # @state(must_finish=True)
    # def open_grabber(self):
    #     print('[3] Open Grabber')
    #     if self.grabber.openGrabber():
    #         print('    ...completes.')
    #         self.next_state_now('wait')

    # @timed_state(duration=3, must_finish=True, next_state='retract_grabber')
    # def wait(self):
    #     print('[4] Wait')
    #     pass

    # @state(must_finish=True)
    # def retract_grabber(self):
    #     print('[5] Retract Grabber')
    #     if self.grabber.goToLevel(0):
    #         print('    ...completes.')
    #         self.next_state_now('lower_grabber')  

    # @state(must_finish=True)
    # def lower_grabber(self):
    #     print('[6] Lower Grabber')
    #     if self.elevator.goToLevel(0):
    #         print('    ...completes.')
    #         self.next_state_now('drive_backwards')    
    
    # @state(must_finish = True)
    # def drive_backwards(self):
    #     print('[7] Drive')
    #     if self.drivetrain.goToDistance(self.drive_distance):
    #         print('    ...completes.')
    #         self.next_state_now('stop')
        
        
    # @state(must_finish=True)
    # def stop(self):
    #     print('[8] Complete.')
    #     self.drivetrain.setArcade(0,0)
    #     return False

