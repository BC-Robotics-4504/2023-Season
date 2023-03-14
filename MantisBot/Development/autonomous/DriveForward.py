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

    @state(first=True, must_finish=True)
    def zero_drivetrain(self):
        self.drivetrain.resetDistance()
        self.next_state_now('drive_forward')
    
    @state(must_finish=True)
    def drive_forward(self):
        dist = 1
        self.drivetrain.setDistance(dist)
        if abs(dist - self.drivetrain.mainLeft_motor.getDistance()) < .001:
            self.next_state_now('turn_90')
       
    @state(must_finish=True)
    def turn_90(self):
        isFinished = False
        isFinished = self.imu.runPID(90)
        if isFinished:
            self.next_state_now('stop')

    @state(must_finish=True)
    def stop(self):
        self.drivetrain.setArcade(0,0)
        self.next_state_now('drive_forward2')

    @state(must_finish=True)
    def drive_forward2(self):
        self.drivetrain.resetDistance()
        dist = 1
        self.drivetrain.setDistance(dist)
        # if abs(3 - self.drivetrain.mainLeft_motor.getDistance()) < .001:
        #     self.next_state_now('turn_90')


        

    # @state()
    # def stop_state(self):
    #     self.drivetrain.setDistance(0)

    # def on_enable(self) -> None:
    #     return None
    
    # def on_iteration(self, tm: float) -> None:
    #     return None

    # def on_disable(self) -> None:
    #     return None

