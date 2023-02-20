
#!/usr/bin/env python3

"""
#		    _/  _/    _/_/_/_/    _/    _/  _/   
#		   _/  _/    _/        _/  _/  _/  _/    
#		  _/_/_/_/  _/_/_/    _/  _/  _/_/_/_/   
#		     _/          _/  _/  _/      _/      
#		    _/    _/_/_/      _/        _/ 
"""

from magicbot import MagicRobot
import wpilib
import rev
import ctre
import photonvision

from componentsDrive import DriveTrainModule, ComboSparkMax
from componentsColor import ColorModule
from componentsGrabber import GrabberModule
from componentsIMU import IMUModule
from componentsHMI import HMIModule, FlightStickHMI
from componentsVision import VisionModule
from componentsLimelight import LimelightModule
from componentsElevator import ElevatorModule, ElevatorSparkMax
from componentsGrabber import GrabberModule, GrabberSparkMax

from autonomous.controllerAprilTagPVFollower import AprilTagPVController

class MyRobot(MagicRobot):
    
    drivetrain : DriveTrainModule
    color : ColorModule
    imu : IMUModule
    hmi : HMIModule
    vision : VisionModule
    limelight : LimelightModule
    grabber : GrabberModule
    elevator: ElevatorModule
    
    # intake: IntakeModule
    # Intake_cfg = IntakeConfig(1, 2) # TODO: this might not work... 
    

    def createObjects(self):
        """Robot initialization function"""
        
        """Intake Motor Configuration"""
        self.grabber_pneumatics= wpilib.PneumaticHub(11)
        self.grabber_motor = GrabberSparkMax(12, [])
        self.elevator_motor = ElevatorSparkMax(13, [])
        
        """Drivetrain Motor Configuration"""
        self.mainLeft_motor = ComboSparkMax(6, [4,5], inverted=False)
        self.mainRight_motor = ComboSparkMax(2, [1,3], inverted=True)
        
        """Sensor Setups"""
        self.colorSensor = rev.ColorSensorV3(wpilib.I2C.Port.kOnboard)
        
        """IMU Configuration"""
        self.imuSensor = ctre.Pigeon2(11)

        """Camera Configurtation"""
        self.camera = photonvision.PhotonCamera('MSWebCam')

        """User Controller Configuration"""
        self.hmi_interface = FlightStickHMI(0, 1)

        """Controllers"""
        self.ATPVController = AprilTagPVController()
        
        pass

    def teleopInit(self):
        """Disable Autonomous Lockout of Drivetrain access to the HMI"""
        self.drivetrain.disable_autoLockout()
        return False

    def teleopPeriodic(self) -> None:
        """Note: drivetrain will automatically function here!"""
        if self.hmi.is_buttonPressed():

            if not self.drivetrain.is_autoLockoutActive():
                self.drivetrain.enable_autoLockout()

            self.ATPVController.engage()

        else:
            self.drivetrain.disable_autoLockout()
        

if __name__ == "__main__":

    wpilib.run(MyRobot)