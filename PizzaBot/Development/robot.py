

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
from wpilib import SmartDashboard

import rev
import ctre
import photonvision

from autonomous.controllerPVAprilTagFollowerTeleop import AprilTagPVControllerTeleop
from autonomous.controllerParkAprilTag import ParkingController
# from autonomous.controllerScoreCube import ScoreCubeController


from componentsDrive import ComboTalonSRX, DriveTrainModule, ComboSparkMax
from componentsColor import ColorModule
from componentsIMU import IMUModule
from componentsHMI import HMIModule, FlightStickHMI
from componentsPhotonVision import PhotonVisionModule
from componentsLimelight import LimelightModule


# IntakeConfig = namedtuple("IntakeConfig", ["channelA", "channelB"])

class MyRobot(MagicRobot):
    
    drivetrain : DriveTrainModule
    color : ColorModule
    imu : IMUModule
    hmi : HMIModule
    photonvision : PhotonVisionModule
    limelight : LimelightModule

    follow_controller : AprilTagPVControllerTeleop
    parking_controller : ParkingController
    # scoreCube_controller : ScoreCubeController
    # ScoreCubeController.parking_controller.MODE_NAME = 'TeleopMain>ScoreCube>ParkingController'


    # grabber: GrabberModule


    # Intake_cfg = IntakeConfig(1, 2) # TODO: this might not work... 
    

# rev._rev.CANSparkMax(8, rev._rev.CANSparkMaxLowLevel.MotorType.kBrushless)

    def createObjects(self):

        """Robot initialization function"""

        """Drivetrain Motor Configuration"""
        self.mainLeft_motor = ComboTalonSRX(6, [4,5], inverted=False)
        self.mainRight_motor = ComboTalonSRX(2, [1,3], inverted=True)

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
        self.drivetrain.resetDistance()

        # self.drivetrain.setDistance(-10)

        return False


    def teleopPeriodic(self) -> None:

        """Note: drivetrain will automatically function here!"""

        SmartDashboard.putNumber('Right Motor Revolutions = ', self.drivetrain.mainRight_motor.__getRawSensorPosition__()/4096/10)
        SmartDashboard.putNumber('Left Motor Revolutions = ', self.drivetrain.mainLeft_motor.__getRawSensorPosition__()/4096/10)

        if self.hmi.is_buttonPressed('R', 2):
            if not self.drivetrain.is_lockedout():
                self.drivetrain.enable_autoLockout()

            SmartDashboard.putString('Follower Controller State = ', self.follow_controller.current_state.title())
            self.follow_controller.engage()

        # if self.hmi.is_buttonPressed('R', 1):
        #     if not self.drivetrain.is_lockedout():
        #         self.drivetrain.enable_autoLockout()
            
        #     SmartDashboard.putString('Follower Controller State = ', self.scoreCube_controller.current_state.title())
        #     self.scoreCube_controller.engage()
            

        # TODO: Put on different button to make robot drive forward set distance
        # self.drivetrain.mainLeft_motor.setDistance(10)
        # self.drivetrain.mainRight_motor.setDistance(10)
        # print(self.drivetrain.mainLeft_motor.getDistance(), self.drivetrain.mainLeft_motor.getDistance())

        else:   
            self.drivetrain.disable_autoLockout()

if __name__ == "__main__":

    wpilib.run(MyRobot)