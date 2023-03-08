from magicbot import AutonomousStateMachine, timed_state, state

# this is one of your components
from componentsDrive import DriveTrainModule as DriveTrain


class DriveForward(AutonomousStateMachine):
    # Injected from the definition in robot.py
    
    MODE_NAME = "Drive Forward"
    DEFAULT = True
    
    drivetrain: DriveTrain

    @timed_state(duration=3, first=True)
    def drive_forward(self):
        print('does this thing work?********************************************')
        self.drivetrain.setArcade(0.05, 0)

    # @state()
    # def stop_state(self):
    #     self.drivetrain.setDistance(0)

    # def on_enable(self) -> None:
    #     return None
    
    # def on_iteration(self, tm: float) -> None:
    #     return None

    # def on_disable(self) -> None:
    #     return None

