
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
# from componentsPhotonVision import PhotonVisionModule
# from componentsLimelight import LimelightModule
from componentsElevator import ElevatorModule, ElevatorSparkMax
from componentsGrabber import GrabberModule, GrabberSparkMax, GrabberPneumatics

# from autonomous.controllerAprilTagPVFollower import AprilTagPVController

from autonomous.DriveForward import DriveForward

class MyRobot(MagicRobot):
    
    drivetrain : DriveTrainModule
    color : ColorModule
    imu : IMUModule
    hmi : HMIModule
    # vision : PhotonVisionModule
    # limelight : LimelightModule
    grabber : GrabberModule
    elevator: ElevatorModule    

    def createObjects(self):
        """Robot initialization function"""
        
        """Intake Motor Configuration"""
        self.grabber_pneumatics= GrabberPneumatics(11)
        self.grabber_motor = GrabberSparkMax(12, [], wheel_diameter=0.0508, gear_ratio=1/64)
        self.elevator_motor = ElevatorSparkMax(13, [], wheel_diameter=0.0508, gear_ratio=1/20)
        
        """Drivetrain Motor Configuration"""
        self.mainLeft_motor = ComboSparkMax(3, [4], inverted=True, wheel_diameter=0.1524, gear_ratio=30/68)
        self.mainRight_motor = ComboSparkMax(2, [1], inverted=False, wheel_diameter=0.1524, gear_ratio=30/68)
        
        """Sensor Setups"""
        self.colorSensor = rev.ColorSensorV3(wpilib.I2C.Port.kOnboard)
        
        """IMU Configuration"""
        self.imuSensor = ctre.Pigeon2(11)

        """Camera Configurtation"""
        self.camera = photonvision.PhotonCamera('MSWebCam')

        """User Controller Configuration"""
        self.hmi_interface = FlightStickHMI(1, 0)

        """Controllers"""
        # self.ATPVController = AprilTagPVController()
        
        pass

    def teleopInit(self):
        """Disable Autonomous Lockout of Drivetrain access to the HMI"""
        self.drivetrain.disable_autoLockout()
        return False

    def teleopPeriodic(self) -> None:
        """Note: drivetrain will automatically function here!"""
        if self.hmi.is_buttonPressed('R', 2):

            if not self.drivetrain.is_lockedout():
                self.drivetrain.enable_autoLockout()

            # self.ATPVController.engage()

        else:
            self.drivetrain.disable_autoLockout()
        

if __name__ == "__main__":

    wpilib.run(MyRobot)