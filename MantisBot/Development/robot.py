
#!/usr/bin/env python3

"""
#		    _/  _/    _/_/_/_/    _/    _/  _/   
#		   _/  _/    _/        _/  _/  _/  _/    
#		  _/_/_/_/  _/_/_/    _/  _/  _/_/_/_/   
#		     _/          _/  _/  _/      _/      
#		    _/    _/_/_/      _/        _/ 
"""

# Libraries 
from magicbot import MagicRobot
import wpilib
import rev
import ctre
import photonvision

# Components
from componentsDrive import DriveTrainModule, ComboSparkMax
from componentsColor import ColorModule
from componentsGrabber import GrabberModule
from componentsIMU import IMUModule
from componentsHMI import HMIModule, FlightStickHMI
# from componentsPhotonVision import PhotonVisionModule
# from componentsLimelight import LimelightModule
from componentsElevator import ElevatorModule, ElevatorSparkMax
from componentsGrabber import GrabberModule, GrabberSparkMax, GrabberPneumatics

# Controllers
# from autonomous.controllerAprilTagPVFollower import AprilTagPVController
from autonomous.DriveForward import DriveForward
from autonomous.controllerSuperstructure import Superstructure
from autonomous.controllerScoreLow import ScoreLow

class MyRobot(MagicRobot):
    # High level components
    superstructure : Superstructure
    scoreLow : ScoreLow

    # Low level components
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
        self.grabber_motor = GrabberSparkMax(12, [], wheel_diameter=0.0762, gear_ratio=64/1)
        self.elevator_motor = ElevatorSparkMax(13, [], wheel_diameter=0.0382, gear_ratio=10/1)
        
        """Drivetrain Motor Configuration"""
        self.mainLeft_motor = ComboSparkMax(3, [4], inverted=True, wheel_diameter=0.1524, gear_ratio=(52*68)/(11*30))
        self.mainRight_motor = ComboSparkMax(2, [1], inverted=False, wheel_diameter=0.1524, gear_ratio=(52*68)/(11*30))
        
        """Sensor Setups"""
        self.colorSensor = rev.ColorSensorV3(wpilib.I2C.Port.kOnboard)
        
        """IMU Configuration"""
        self.imuSensor = ctre.Pigeon2(15)

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
        if self.hmi.getRightButton(2):

            if not self.drivetrain.is_lockedout():
                self.drivetrain.enable_autoLockout()
            
            # self.ATPVController.engage()

        if self.hmi.getLeftButton(3): # High goal
            if not self.drivetrain.is_lockedout(): 
                #TODO: do we want to really lock out the drivetrain here or 
                # would it be better to go into some low-speed clamp mode?
                self.drivetrain.enable_autoLockout()
            self.superstructure.scorePosition(elevator_level=3, grabber_level=2)
            print("L3 Pressed")

        if self.hmi.getLeftButton(2): # Mid goal
            if not self.drivetrain.is_lockedout():
                self.drivetrain.enable_autoLockout()
                print('lockout')
            self.superstructure.scorePosition(elevator_level=2, grabber_level=1)
            print("L2 Pressed")

        if self.hmi.getLeftButton(4): #Low Goal
            if not self.drivetrain.is_lockedout():
                self.drivetrain.enable_autoLockout()
            self.scoreLow.scoreLow()
            print("L4 Pressed")
 
        else:
            self.drivetrain.disable_autoLockout()

        

if __name__ == "__main__":

    wpilib.run(MyRobot)