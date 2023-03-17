
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
# from componentsColor import ColorModule
from componentsGrabber import GrabberModule
from componentsIMU import IMUModule
from componentsHMI_xbox import XboxHMI, HMIModule
# from componentsHMI import HMIModule, FlightStickHMI
# from componentsPhotonVision import PhotonVisionModule
# from componentsLimelight import LimelightModule
from componentsElevator import ElevatorModule, ElevatorSparkMax
from componentsGrabber import GrabberModule, GrabberSparkMax, GrabberPneumatics

# Controllers
# from autonomous.controllerAprilTagPVFollower import AprilTagPVController
from autonomous.controllerScoreHigh import ScoreHigh
from autonomous.controllerScoreMid import ScoreMid
from autonomous.controllerScoreLow import ScoreLow
from autonomous.controllerStation import Station
from autonomous.controllerFloor import Floor

class MyRobot(MagicRobot):
    # High level components
    scoreHigh : ScoreHigh
    scoreMid : ScoreMid
    scoreLow : ScoreLow
    station : Station
    floor : Floor
    

    # Low level components
    drivetrain : DriveTrainModule
    # color : ColorModule
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
        self.mainLeft_motor = ComboSparkMax(2, [1], inverted=False, wheel_diameter=0.1524, gear_ratio=(52*68)/(11*30))
        self.mainRight_motor = ComboSparkMax(3, [4], inverted=True, wheel_diameter=0.1524, gear_ratio=(52*68)/(11*30))
        
        # """Sensor Setups"""
        # self.colorSensor = rev.ColorSensorV3(wpilib.I2C.Port.kOnboard)
        
        """IMU Configuration"""
        self.imuSensor = ctre.Pigeon2(15)

        """Camera Configurtation"""
        self.camera = photonvision.PhotonCamera('MSWebCam')

        """User Controller Configuration"""
        self.hmi_interface = XboxHMI(0)

        """Controllers"""
        # self.ATPVController = AprilTagPVController()
        
        pass

    def teleopInit(self):
        """Disable Autonomous Lockout of Drivetrain access to the HMI"""
        self.drivetrain.disable_autoLockout()
        self.elevator.enableBrake()
        self.grabber.enableBrake()
        self.grabber.openGrabber()
        return False

    def teleopPeriodic(self) -> None:
        """Note: drivetrain will automatically function here!"""
        # if self.hmi.getRightButton(2):
        #     if not self.drivetrain.is_lockedout():
        #         self.drivetrain.enable_autoLockout()
        #     print("L2 Pressed")
        #     # self.ATPVController.engage()

        if self.hmi.getButton('Y'): # High goal
            if not self.drivetrain.is_lockedout(): 
                #TODO: do we want to really lock out the drivetrain here or 
                # would it be better to go into some low-speed clamp mode?
                self.drivetrain.enable_autoLockout()
            self.scoreHigh.score()
            print("Y Pressed")

        if self.hmi.getButton('X'): # Mid goal
            if not self.drivetrain.is_lockedout():
                self.drivetrain.enable_autoLockout()
                print('lockout')
            self.scoreMid.score()
            print("X Pressed")

        if self.hmi.getButton('A'): #Low Goal
            if not self.drivetrain.is_lockedout():
                self.drivetrain.enable_autoLockout()
            self.scoreLow.score()
            print("A Pressed")
            
        if self.hmi.getButton('B'): #Station
            if not self.drivetrain.is_lockedout():
                self.drivetrain.enable_autoLockout()
            self.station.pickUp()
            print("B Pressed")
        
        if self.hmi.getButton('RB'): #Floor Pickup 
            if not self.drivetrain.is_lockedout():
                self.drivetrain.enable_autoLockout()
            self.floor.pickUp()
            print('RB Pressed') 
 
        else:
            self.drivetrain.disable_autoLockout()

        if self.hmi.getButton('LT'):
            self.grabber.openGrabber()
            print("LT Pressed")

        if self.hmi.getButton('RT'):
            self.grabber.closeGrabber()
            print("RT Pressed")


        #MANUAL SUPERSTRUCTURE CONTROLS
        if self.hmi.getButton('RS'):
            self.grabber.goToLevel(0)
            print("RS Pressed")
        
        if self.hmi.getButton('LS'):
            self.elevator.goToLevel(0)
            print("LS Pressed")

        if self.hmi.getButton('Select'):
            self.grabber.goToLevel(2)
            print("Select pressed")

        if self.hmi.getButton('Back'):
            self.elevator.goToLevel(3) #TODO: change to 4???
            print("Back pressed")


    def disabledPeriodic(self):
        self.elevator.disableBrake()
        self.grabber.disableBrake()
        self.grabber.openGrabber()
        

if __name__ == "__main__":

    wpilib.run(MyRobot)