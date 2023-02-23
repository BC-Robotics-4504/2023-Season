"""
#		    _/  _/    _/_/_/_/    _/    _/  _/   
#		   _/  _/    _/        _/  _/  _/  _/    
#		  _/_/_/_/  _/_/_/    _/  _/  _/_/_/_/   
#		     _/          _/  _/  _/      _/      
#		    _/    _/_/_/      _/        _/ 
"""

from re import L
import wpilib
import rev
import time, heapq
from wisdom import SHOOTER, DRIVETRAIN, CAMERA, LEDS, ELEVATOR

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        """Robot initialization function"""

        # Initialize timing heap
        self.heap = []

        # Initialize shooter mechanism
        self.shooter = SHOOTER()
        self.shooting = False
        self.shooting_spinup_time_ns = 1.0e9
        self.shooting_shoot_time_ns = 1.0e9
        self.shooting_reloading_time_ns = 0.2e9

        self.high_goal_power = .63
        self.low_goal_power = .63

        # Initialize drivetrain mechanism
        self.drivetrain = DRIVETRAIN()
        self.drivetrain_lockout = False

        # Initialize elevator mechanism
        self.elevator = ELEVATOR()
        self.elevator_moving = False
        self.elevator_move_time_ns = 1.0e9
        # self.elevator = rev.CANSparkMax(6, rev._rev.CANSparkMaxLowLevel.MotorType.kBrushless)

        # Initialize LEDs
        self.leds = LEDS()
        self.leds.setSolidColor("white")

        # Initialize camera server
        self.camera = CAMERA()

        # Initialize the controllers
        self.controller = wpilib.XboxController(0)

        # self.controller2 = wpilib.XboxController(0)
        self.leftStickHold = False
        self.leftStickCooldown = 0
        self.rightStickHold = False
        self.rightStickCooldown = 0


    def autonomousInit(self) -> None:
        self.leds.setSolidColor("violet")
        self.drivetrain.shift_down()

        current_time = time.time_ns()
        heapq.heappush(self.heap, (current_time, 'enable intake'))
        heapq.heappush(self.heap, (current_time, 'spinup'))
        heapq.heappush(self.heap, (current_time, 'move'))
        heapq.heappush(self.heap, (current_time + 6.7e9, 'launch'))
        heapq.heappush(self.heap, (current_time + 6.7e9, 'disable'))
        heapq.heappush(self.heap, (current_time + 6.8e9, 'disable'))
        heapq.heappush(self.heap, (current_time + 6.9e9, 'disable'))
        heapq.heappush(self.heap, (current_time + 7.0e9, 'disable'))
        heapq.heappush(self.heap, (current_time + 7.1e9, 'disable'))
        heapq.heappush(self.heap, (current_time + 7.2e9, 'disable'))

        return super().autonomousInit()

    def autonomousPeriodic(self) -> None:

        if len(self.heap) > 0:
            if time.time_ns() >= self.heap[0][0]:
                (*_, action) = heapq.heappop(self.heap)

                if action == 'enable intake':
                    self.shooter.set_intake_position(1)

                elif action == 'spinup':

                    # Spin-up shooter wheel
                    self.shooter.enable_shooter(self.high_goal_power)

                elif action == 'move':
                    self.drivetrain.left_drive(-0.8)
                    self.drivetrain.right_drive(-0.8)

                elif action == 'launch':

                    # Advance ball to launch it
                    self.shooter.enable_stage2()

                elif action == 'disable':

                    #Disable Intake
                    self.shooter.set_intake_position(0)

                    # Disable Drivetrain
                    self.drivetrain.left_drive(0)
                    self.drivetrain.right_drive(0)

                    # Disable stages
                    self.shooter.disable_shooter()
                    self.shooter.disable_stage2()


                    # Shift to high gear
                    self.drivetrain.shift_up()

        # If robot gets through autonomous early and has time to spare, turn red...
        else:
            if self.leds.current_color != 'red':
                self.leds.setSolidColor('red')

            else:
                pass


        return super().autonomousPeriodic()

    def teleopInit(self):
        """Executed at the start of teleop mode"""

        self.leds.setSolidColor("blue")

        # Retract intake mechanism
        self.shooter.set_intake_position(0)

        # Shut down motors
        self.drivetrain.left_drive(0)
        self.drivetrain.right_drive(0)

        # Shift to high gear
        self.drivetrain.shift_down()

        # Clear heap
        self.heap = []

        # self.myRobot.setSafetyEnabled(True)
        return super().teleopInit()

    def teleopPeriodic(self, speed_clamp=0.50):
        '''
        DRIVING CODE ==============================================================================
        '''
        if self.drivetrain_lockout == False:
            # Shift to gear based on user input
            if self.controller.getRightBumperPressed():

                # Shift to high gear
                if self.drivetrain.current_gear == 0:
                    self.drivetrain.shift_up()

                # Shift to low gear
                else:
                    self.drivetrain.shift_down()
            
            # Allow robot to go full-power
            # if self.controller.getL2Button():
            #     speed_clamp = 1.0

            # Handler for Xbox controller - Locks changes to output state for 10 duty cycles    
            self.leftStickCooldown +=1
            if self.controller.getLeftStickButton() and self.leftStickCooldown >= 10:
                if self.leftStickHold == False:
                    self.leftStickHold = True
                elif self.leftStickHold == True:
                    self.leftStickHold = False
                self.leftStickCooldown = 0

            # TANK DRIVE
            # Set left and right drive trains to input of left and right controller Y-axes, flips drive sides if L2 is held
            # REMAPPED WITH XBOX CONTROLLER (left stick button)
            # if not self.controller.getL2Button() and not self.leftStickHold:
            self.drivetrain.left_drive(self.controller.getLeftY()*speed_clamp)
            self.drivetrain.right_drive(self.controller.getRightY()*speed_clamp)

            # if self.controller.getL2Button() or self.leftStickHold:
            #     self.drivetrain.left_drive(self.controller.getRightY()*-speed_clamp)
            #     self.drivetrain.right_drive(self.controller.getLeftY()*-speed_clamp)

            # ARCADE DRIVE
            # Set left and right drive trains to input of left Y-axis minus input of left X-axis
            # self.drivetrain.left_drive((-self.controller.getLeftY() - (0.50 * self.controller.getLeftX()))*-speed_clamp)
            # self.drivetrain.right_drive((-self.controller.getLeftY() + (0.50 * self.controller.getLeftX()))*-speed_clamp)

        '''
        INTAKE CODE =============================================================================
        '''

        # Handler for Xbox controller - Locks changes to output state for 10 duty cycles
        # self.rightStickCooldown +=1
        if self.controller.getRightStickButton() and self.rightStickCooldown >= 10:
            if self.rightStickHold == False:
                self.rightStickHold = True
            elif self.rightStickHold == True:
                self.rightStickHold = False
            self.rightStickCooldown = 0

        # Lower intake stage and spin up intake motors if button is depressed
        # REMAPPED WITH XBOX CONTROLLER (Right stick button)
        # self.shooter.set_intake_position(self.controller.getL2Button())
        if self.controller.getRightStickButtonPressed() or self.rightStickHold:
            self.shooter.set_intake_position(1)
        if self.controller.getRightStickButtonReleased() or self.rightStickHold:
            self.shooter.set_intake_position(0)

        # Enables/disables stage 1 in between balls
        if self.controller.getAButtonPressed():
            self.shooter.enable_stage1()
        if self.controller.getAButtonReleased():
            self.shooter.disable_stage1()

        # Purges stage 1 if a opposite alliance's ball is in the stage
        if self.controller.getBButtonPressed():
            self.shooter.enable_stage1_purge()
        if self.controller.getBackButtonReleased():
            self.shooter.disable_stage1()

        # Purges stage 2 if the shooter jams
        if self.controller.getXButtonPressed():
            self.shooter.enable_stage2_purge()
        if self.controller.getYButtonReleased():
            self.shooter.disable_stage2()

        '''
        CLIMBING CODE =============================================================================
        '''
        # Gets individual buttons on DPad

        self.DPadUp = False
        self.DpadDown = False

        self.DPad = self.controller.getPOV()
        if self.DPad == 0:
            self.DPadUp = True
            self.DpadDown = False
        elif self.DPad == 180:
            self.DPadUp = False
            self.DpadDown = True



        # Extends or retracts elevator based on user input
        if self.DPadUp:
            self.elevator.extend_elevators(0.55)
            self.drivetrain_lockout = False

                
        elif self.DpadDown:
            self.elevator.retract_elevators(0.45)
            self.drivetrain.left_drive(-0.15)
            self.drivetrain.right_drive(-0.15)
            self.drivetrain_lockout = True


        if self.DPadUp == False and self.DpadDown == False:
            self.elevator.disable_elevators()
            self.drivetrain_lockout = False
    
        # # Emergency Stop
        # if self.controller.getTriangleButtonPressed():
        #     self.elevator.disable_elevators()

        '''
        SHOOTING CODE =============================================================================
        '''

        if self.controller.getRightBumperPressed() and self.shooting == False:

            # Get current time
            current_time = time.time_ns()
            
            # Spinup shooter
            if not self.controller.getYButton():
                self.shooter.enable_shooter(self.high_goal_power)
            else:
                self.shooter.enable_shooter(self.low_goal_power)
                heapq.heappush(self.heap, (current_time + 0.6e9, 'low_goal_spindown'))
            
            heapq.heappush(self.heap, (current_time + self.shooting_spinup_time_ns, 'launch'))
            if not self.controller.getYButton():
                heapq.heappush(self.heap, (current_time + self.shooting_spinup_time_ns + 0.5e9, 'reload'))
            heapq.heappush(self.heap, (current_time + self.shooting_spinup_time_ns + self.shooting_shoot_time_ns, 'spindown'))
            # self.shooting = True

        if self.controller.getRightBumperPressed():
            self.shooter.enable_shooter(self.high_goal_power)
            if self.controller.getBButton():
                self.shooter.enable_shooter(self.low_goal_power)
            self.shooter.enable_stage2()

        if self.controller.getRightBumperReleased():
            self.shooter.disable_shooter()
            self.shooter.disable_stage2()

        '''
        TIMED SEQUENCE HANDLER ====================================================================
        '''
        if len(self.heap) > 0:
            if time.time_ns() >= self.heap[0][0]:
                (*_, action) = heapq.heappop(self.heap)

                if action == 'launch':

                    # Advance ball to launch it
                    self.shooter.enable_stage2()

                elif action == 'reload':

                    # Push ball in stage 1 to stage 2
                    self.shooter.enable_stage1()

                elif action == 'low_goal_spindown':
                    self.shooter.disable_shooter()

                elif action == 'spindown':

                    # Disable stages
                    self.shooter.disable_shooter()
                    self.shooter.disable_stage2()
                    self.shooter.disable_stage1()
                    self.shooting = False

                elif action == 'disable_elevators':

                    # Disable elevators
                    self.elevator.disable_elevators()
                    self.elevator_moving = False
        return super().teleopPeriodic()

#%% ###########################################################################

if __name__ == "__main__":
    wpilib.run(MyRobot)