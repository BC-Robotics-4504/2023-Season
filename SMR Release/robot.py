
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
# import ctre
# import photonvision

# Components
from componentsDrive import DriveTrainModule, ComboSparkMax
# from componentsColor import ColorModule
from componentsGrabber import GrabberModule
# from componentsIMU import IMUModule
from componentsHMI_xbox import XboxHMI, HMIModule
# from componentsHMI import HMIModule, FlightStickHMI
# from componentsPhotonVision import PhotonVisionModule
# from componentsLimelight import LimelightModule
from componentsElevator import ElevatorModule, ElevatorSparkMax
from componentsGrabber import GrabberModule, GrabberSparkMax, GrabberPneumatics

# Controllers
# from autonomous.controllerAprilTagPVFollower import AprilTagPVController
from autonomous.controllerSuperstructure import Superstructure

class MyRobot(MagicRobot):
    # High level components
    # scoreHigh : ScoreHigh
    # scoreMid : ScoreMid
    # scoreLow : ScoreLow
    # station : Station
    # floor : Floor
    superstructure : Superstructure
    

    # Low level components
    drivetrain : DriveTrainModule
    # color : ColorModule
    # imu : IMUModule
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
        
        # """IMU Configuration"""
        # self.imuSensor = ctre.Pigeon2(15)

        # """Camera Configurtation"""
        # self.camera = photonvision.PhotonCamera('MSWebCam')

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

        self.elevator.goToLevel(2)
        self.grabber.goToLevel(0)
        return False

    def teleopPeriodic(self) -> None:
        """Note: drivetrain will automatically function here!"""
        # if self.hmi.getRightButton(2):
        #     if not self.drivetrain.is_lockedout():
        #         self.drivetrain.enable_autoLockout()
        #     print("L2 Pressed")
        #     # self.ATPVController.engage()

        # if self.hmi.getButton('B'): # High goal
        #     if not self.drivetrain.is_lockedout(): 
        #         #TODO: do we want to really lock out the drivetrain here or 
        #         # would it be better to go into some low-speed clamp mode?
        #         self.drivetrain.enable_autoLockout()
        #     self.scoreHigh.score()
        #     print("[+] High Goal (B) ===============================")

        # if self.hmi.getButton('X'): # Mid goal
        #     if not self.drivetrain.is_lockedout():
        #         self.drivetrain.enable_autoLockout()
        #     self.scoreMid.score()
        #     print("[+] Mid Goal (X) ===============================")

        # if self.hmi.getButton('Y'): #Low Goal
        #     if not self.drivetrain.is_lockedout():
        #         self.drivetrain.enable_autoLockout()
        #     self.scoreLow.score()
        #     print("[+] Low Goal (Y) ===============================")
            
        # if self.hmi.getButton('A'): #Station
        #     if not self.drivetrain.is_lockedout():
        #         self.drivetrain.enable_autoLockout()
        #     self.station.pickUp()
        #     print("[+] Station Pickup (A) ===============================")
        
        # if self.hmi.getButton('RB'): #Floor Pickup 
        #     if not self.drivetrain.is_lockedout():
        #         self.drivetrain.enable_autoLockout()
        #     self.floor.pickUp()
        #     print('[+] Floor Pickup (RB) ===============================') 
 
        # else:
        #     self.drivetrain.disable_autoLockout()

        if self.hmi.getButton('RT'): #! Opens Grabber
            self.grabber.openGrabber()
            print("[+] Grabber Opened ===============================")

        if self.hmi.getButton('LT'): #! Closes Grabber
            self.grabber.closeGrabber()
            print("[+] Grabber Closed ===============================")
        
        # if self.hmi.getButton('Back'):
        #     if not self.drivetrain.is_lockedout():
        #         self.drivetrain.enable_autoLockout()
        #     self.reset.reset()
        #     print("[+] Resetting Structure... ===============================")


        # #MANUAL SUPERSTRUCTURE CONTROLS
        # if self.hmi.getButton('Start'):
        #     self.grabber.goToLevel(0)
        #     print("[+] Grabber Retracting ===============================")
        
        # if self.hmi.getButton('Back'):
        #     self.elevator.goToLevel(0)
        #     self.grabber.goToLevel(0)
        #     print("[+] Elevator Lowering ===============================")


        if self.hmi.getButton('Y'): #! High Goal
            self.superstructure.actuate(8,2)
            
        if self.hmi.getButton('DU'): #! Station Pickup
            self.superstructure.actuate(7,2)
        
        if self.hmi.getButton('B'): #! Mid Goal  
            self.superstructure.actuate(4,1)
        
        if self.hmi.getButton('A'): #! Go to default state. (Slightly above bumper)
            self.elevator.goToLevel(1)
            self.grabber.goToLevel(0)
        
        if self.hmi.getButton('Start'): #! Resets superstructure to ground state
            self.grabber.openGrabber()
            if self.elevator.getDistance() >=.3:
                print(self.elevator.getDistance(), self.grabber.getDistance())
                self.grabber.goToLevel(3)
            self.elevator.goToLevel(0)

        if self.hmi.getButton('Back'): #! Resets superstructure to ground state and disable brake. 
            self.elevator.disableBrake()
            self.grabber.disableBrake()
            self.grabber.openGrabber()
            if self.elevator.getDistance() >=.3:
                print(self.elevator.getDistance(), self.grabber.getDistance())
                self.grabber.goToLevel(3)
            self.elevator.goToLevel(0)
        

if __name__ == "__main__":

    wpilib.run(MyRobot)