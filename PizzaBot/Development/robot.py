
#!/usr/bin/env python3

"""
#		    _/  _/    _/_/_/_/    _/    _/  _/   
#		   _/  _/    _/        _/  _/  _/  _/    
#		  _/_/_/_/  _/_/_/    _/  _/  _/_/_/_/   
#		     _/          _/  _/  _/      _/      
#		    _/    _/_/_/      _/        _/ 
"""


""""
    This is where all of our robot code 
    is pulled together from component modules to
     define the behavior of diffrent components
"""
from magicbot import MagicRobot
import wpilib
import rev
import ctre
import photonvision

from autonomous.controllerPVAprilTagFollower import AprilTagPVController

from componentsDrive import ComboTalonSRX, DriveTrainModule, ComboSparkMax
from componentsColor import ColorModule
from componentsIMU import IMUModule
from componentsHMI import HMIModule, FlightStickHMI
from componentsVision import VisionModule
from componentsLimelight import LimelightModule

# IntakeConfig = namedtuple("IntakeConfig", ["channelA", "channelB"])
class MyRobot(MagicRobot):
    
    drivetrain : DriveTrainModule
    color : ColorModule
    imu : IMUModule
    hmi : HMIModule
    vision : VisionModule
    limelight : LimelightModule
    # grabber: GrabberModule

    # Intake_cfg = IntakeConfig(1, 2) # TODO: this might not work... 
    
# rev._rev.CANSparkMax(8, rev._rev.CANSparkMaxLowLevel.MotorType.kBrushless)
    def createObjects(self):
        """Robot initialization function"""
        
        """Drivetrain Motor Configuration"""
        # self.mainLeft_motor = ComboSparkMax(6, [4,5], inverted=False)
        # self.mainRight_motor = ComboSparkMax(2, [1,3], inverted=True)
        self.mainLeft_motor = ComboTalonSRX(6, [4,5], inverted=False)
        self.mainRight_motor = ComboTalonSRX(2, [1,3], inverted=True)
        self.ATPVController = AprilTagPVController()
        
        """"Grabber Setup"""
        
        """Elevator Setup"""
        
        """Sensor Setups"""
        self.colorSensor = rev.ColorSensorV3(wpilib.I2C.Port.kOnboard)
        
        """IMU Configuration"""
        self.imuSensor = ctre.Pigeon2(11)

        """Camera Configurtation"""
        self.camera = photonvision.PhotonCamera('MSWebCam')

        """User Controller Configuration"""
        self.hmi_interface = FlightStickHMI(0, 1)
        
        pass

    def teleopInit(self):
        """Disable Autonomous Lockout of Drivetrain access to the HMI"""
        self.drivetrain.disable_autoLockout()
        return False

    def teleopPeriodic(self) -> None:
        """Note: drivetrain will automatically function here!"""
        if self.hmi.is_buttonPressed():

            if not self.drivetrain.is_lockedout():
                self.drivetrain.enable_autoLockout()

            self.ATPVController.engage()

        else:
            self.drivetrain.disable_autoLockout()

        # self.drivetrain.setLeft(self.hmi_interface.getInput()[0])   #TODO: this is a stupid fix
        # self.drivetrain.setRight(self.hmi_interface.getInput()[1])
        print(self.imu.getYPR())
        # color = self.color.getColor()
        # prox = self.color.getProximity()
        # ypr = self.imu.getYPR()
        # print(color, prox, ypr)
        

if __name__ == "__main__":
    wpilib.run(MyRobot)