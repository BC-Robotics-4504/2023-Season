import ctre
import rev

from componentsHMI import FlightStickHMI

class ComboTalonSRX:

    #: Which PID slot to pull gains from. Starting 2018, you can choose from
    #: 0,1,2 or 3. Only the first two (0,1) are visible in web-based
    #: configuration.
    kSlotIdx = 0

    #: Talon SRX/ Victor SPX will supported multiple (cascaded) PID loops. For
    #: now we just want the primary one.
    kPIDLoopIdx = 0

    #: set to zero to skip waiting for confirmation, set to nonzero to wait and
    #: report to DS if action fails.
    kTimeoutMs = 10

    def __init__(self, canID_leader, canID_followers, inverted=False):
        self.canID_leader = canID_leader
        self.canID_followers = canID_followers
        self.inverted = inverted
        self.mainMotor = None
        self.followerMotors = None

        self.mainMotor = ctre.TalonSRX(self.canID_leader)
        
        self.mainMotor.configSelectedFeedbackSensor(
            ctre._ctre.TalonSRXFeedbackDevice.QuadEncoder,
            # ctre._ctre.TalonSRXFeedbackDevice.CTRE_MagEncoder_Relative,
            self.kPIDLoopIdx,
            self.kTimeoutMs,
        )

        self.mainMotor.setInverted(self.inverted)

        self.mainMotor.configNominalOutputForward(0, self.kTimeoutMs)
        self.mainMotor.configNominalOutputReverse(0, self.kTimeoutMs)
        self.mainMotor.configPeakOutputForward(1, self.kTimeoutMs)
        self.mainMotor.configPeakOutputReverse(-1, self.kTimeoutMs)
    
        self.mainMotor.selectProfileSlot(self.kSlotIdx, self.kPIDLoopIdx)
        self.mainMotor.config_kP(self.kSlotIdx, .2)
        self.mainMotor.config_kI(self.kSlotIdx, 0.0)
        self.mainMotor.config_kD(self.kSlotIdx, 0.0)
        self.mainMotor.config_kF(self.kSlotIdx, 0.2)
        self.mainMotor.configMotionCruiseVelocity(15000, self.kTimeoutMs)
        self.mainMotor.configMotionAcceleration(6000, self.kTimeoutMs)
        self.mainMotor.setSelectedSensorPosition(0, self.kPIDLoopIdx, self.kTimeoutMs)

        if not isinstance(self.canID_followers, list):
            self.canID_followers = [self.canID_followers]
            
        self.coefficient = 1
        self.gear_ratio = 10

        followerMotors = []
        for canID in self.canID_followers:
            follower = ctre.TalonSRX(canID)
            follower.setInverted(self.inverted)
            follower.follow(self.mainMotor)                              
            followerMotors.append(follower)

        self.followerMotors = followerMotors

    def setPercent(self, value):
        self.mainMotor.set(ctre._ctre.TalonSRXControlMode.PercentOutput, value)
        return False

    def getVelocity(self):
        vel = self.mainMotor.getSelectedSensorVelocity(0)
        return vel

    def __getRawSensorPosition__(self):
        pos = self.mainMotor.getSelectedSensorPosition(0)
        return pos

    def getDistance(self):
        pos = self.__getRawSensorPosition__()*self.coefficient
        print(pos)
        return pos

    def resetDistance(self):
        self.mainMotor.setSelectedSensorPosition(0, self.kPIDLoopIdx, self.kTimeoutMs)
        return False
    
    def setDistance(self, distance):
        ticks = distance * 4096 * self.gear_ratio
        print("when will we get the robot?", distance, ticks)
        self.mainMotor.set(ctre._ctre.TalonSRXControlMode.MotionMagic, ticks)
        return False


class ComboSparkMax:
    def __init__(self, canID_leader, canID_followers, motorType='brushless', inverted=False):
        self.canID_leader = canID_leader
        self.canID_followers = canID_followers
        self.inverted = inverted
        self.mainMotor = None
        self.followerMotors = None

        if motorType == 'brushless':
            mtype = rev.CANSparkMaxLowLevel.MotorType.kBrushless
            
        else:
            mtype = rev.CANSparkMaxLowLevel.MotorType.kBrushed # FIXME!: Is this right? 

        self.mainMotor = rev.CANSparkMax(canID_leader, mtype)
        self.mainMotor.setInverted(self.inverted)
        self.mainEncoder = self.mainMotor.getEncoder(rev.SparkMaxRelativeEncoder.Type.kHallSensor, 42)

        followerMotors = []
        for canID in self.canID_followers:
            follower = rev.CANSparkMax(canID, mtype)
            follower.setInverted(self.inverted)
            follower.follow(self.mainMotor)                              
            followerMotors.append(follower)

        self.followerMotors = followerMotors

    def setPercent(self, value):
        self.mainMotor.set(value)
        return False

    def getVelocity(self):
        vel = self.mainEncoder.getVelocity() #rpm
        return vel

class DriveTrainModule:
    mainLeft_motor: ComboTalonSRX
    mainRight_motor: ComboTalonSRX
    hmi_interface: FlightStickHMI

    def __init__(self):
        self.leftSpeed = 0
        self.leftSpeedChanged = False
        
        self.rightSpeed = 0
        self.rightSpeedChanged = False  

        self.arcadeSpeed = [0,0]    

        self.autoLockout = True

    def setLeft(self, value):
        self.leftSpeed = value         
        self.leftSpeedChanged = True
        
    def setRight(self, value):
        self.rightSpeed = value
        self.rightSpeedChanged = True

    def resetDistance(self):
        self.mainRight_motor.resetDistance()
        self.mainLeft_motor.resetDistance()

    def setDistance(self, value):
        self.mainRight_motor.setDistance(value)
        self.mainLeft_motor.setDistance(value)
        print(value)
        return False
        
    def is_leftChanged(self):
        return self.leftSpeedChanged
    
    def is_rightChanged(self):
        return self.rightSpeedChanged

    def enable_autoLockout(self):
        self.autoLockout = True
        return False

    def disable_autoLockout(self):
        self.autoLockout = False
        return False

    def is_lockedout(self):
        return self.autoLockout

    # Arcade drive code from https://xiaoxiae.github.io/Robotics-Simplified-Website/drivetrain-control/arcade-drive/
    def setArcade(self, drive, rotate):
        self.arcadeSpeed = [drive, rotate]
        """Drives the robot using arcade drive."""
        # variables to determine the quadrants
        maximum = max(abs(drive), abs(rotate))
        total, difference = drive + rotate, drive - rotate

        # set speed according to the quadrant that the values are in
        if drive >= 0:
            if rotate >= 0:  # I quadrant
                self.setLeft(maximum)
                self.setRight(difference)
            else:            # II quadrant
                self.setLeft(total)
                self.setRight(maximum)
        else:
            if rotate >= 0:  # IV quadrant
                self.setLeft(total)
                self.setRight(-maximum)
            else:            # III quadrant
                self.setLeft(-maximum)
                self.setRight(difference)
    
    def getArcadeLinear(self):
        return self.arcadeSpeed[0]
    
    def getArcadeRotation(self):
        return self.arcadeSpeed[1]

    def check_hmi(self):
        (leftSpeed, rightSpeed) = self.hmi_interface.getInput()
        self.setLeft(leftSpeed)
        self.setRight(rightSpeed)
        return False
    
    def clamp(self, num, min_value, max_value):
        return max(min(num, max_value), min_value)

    def execute(self):

        if not self.autoLockout:
            self.check_hmi()

        '''This gets called at the end of the control loop'''
        if self.is_leftChanged():
            self.mainLeft_motor.setPercent(self.leftSpeed)
            self.leftSpeedChanged = False

        if self.is_rightChanged():
            self.mainRight_motor.setPercent(self.rightSpeed)
            self.rightSpeedChanged = False