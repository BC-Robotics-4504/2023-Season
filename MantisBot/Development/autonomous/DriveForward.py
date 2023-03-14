from magicbot import AutonomousStateMachine, timed_state, state

# this is one of your components
from componentsDrive import DriveTrainModule as DriveTrain
from componentsIMU import IMUModule as IMU


class DriveForward(AutonomousStateMachine):
    # Injected from the definition in robot.py
    
    MODE_NAME = "Drive Forward"
    DEFAULT = False
    drivetrain: DriveTrain
    imu: IMU

    def setup(self):
        self.drivetrain.resetDistance()

    @state(first=True, must_finish=True)
    def zero_encoder(self):
        self.drivetrain.resetDistance()
        self.next_state_now('drive_forward')

    @state(must_finish=True)
    def drive_forward(self):
        if self.drivetrain.goToDistance(3):
            self.next_state_now('turn_90')

    @state(must_finish=True)
    def turn_90(self):
        if self.imu.goToAngle(90):
            self.next_state_now('zero_encoder')
            self.cycles+=1


        

    # @state()
    # def stop_state(self):
    #     self.drivetrain.setDistance(0)

    # def on_enable(self) -> None:
    #     return None
    
    # def on_iteration(self, tm: float) -> None:
    #     return None

    # def on_disable(self) -> None:
    #     return None

