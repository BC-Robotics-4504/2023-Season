import wpilib


class XboxHMI:
    def __init__(self, controller_id ):
        self.XboxController = wpilib.XboxController(controller_id)
        
        self.changed = True

        self.leftY = 0
        self.rightX = 0

        self.DEADZONE = .1

        self.buttons = {'LT': False,
                'LB': False,
                'LS': False,
                'Start': False,
                'Back': False,
                'A': False,
                'B': False,
                'X': False,
                'Y': False,
                'RT': False,
                'RB': False,
                'RS': False}


    def updateButtons(self):
        self.buttons['LT'] = True if self.XboxController.getLeftTriggerAxis() > 0.5 else False
        self.buttons['LB'] = self.XboxController.getLeftBumperPressed()
        self.buttons['LS'] = self.XboxController.getLeftStickButtonPressed()
        self.buttons['Start'] = self.XboxController.getStartButtonPressed()
        self.buttons['Back'] = self.XboxController.getBackButtonPressed()
        self.buttons['A'] = self.XboxController.getAButtonPressed()
        self.buttons['B'] = self.XboxController.getBButtonPressed()
        self.buttons['X'] = self.XboxController.getXButtonPressed()
        self.buttons['RT'] = True if self.XboxController.getRightTriggerAxis() > 0.5 else False
        self.buttons['RB'] = self.XboxController.getRightBumperPressed()
        self.buttons['RS'] = self.XboxController.getRightStickButtonPressed()
        return False
    
    def getButtons(self, button_id):
        value = self.buttons[button_id]
        return value
    
    
    def updateAnalogSticks(self):
        # Get input from analog sticks 
        leftY = self.XboxController.getLeftY()
        rightX = self.XboxController.getRightX()

        if abs(leftY) < self.DEADZONE:
            leftY= 0
        self.leftY = leftY
    
        if abs(rightX) < self.DEADZONE:
            rightX = 0
        self.rightX = rightX
        return False

   

    def getInput(self):

        maximum = max(abs(self.leftY), abs(self.rightX))
        total, difference = self.leftY + self.rightX, self.leftY - self.rightX

        # set speed according to the quadrant that the values are in
        if self.leftY >= 0:

            if self.rightX >= 0:  # I quadrant
                return (maximum, difference)

            else:            # II quadrant
                return (total, maximum)

        else:

            if self.rightX >= 0:  # IV quadrant
                return (total, -maximum)

            else:            # III quadrant
                return (-maximum, difference)

class HMIModule:
    hmi_interface: XboxHMI

    def __init__(self):

        self.fsL = 0
        self.fsR = 0
        self.buttons = {'LT': False,
                        'LB': False,
                        'LS': False,
                        'Start': False,
                        'Back': False,
                        'A': False,
                        'B': False,
                        'X': False,
                        'Y': False,
                        'RT': False,
                        'RB': False,
                        'RS': False}

        self.changed = False
        self.enabled = True

    def getInput(self): # fsTuple = (fsL, fsR)
        self.changed = False
        return (self.fsL, self.fsR)
    
    def getButton(self, button_id):
        if button_id in self.hmi_interface.buttons.keys():
            value = self.hmi_interface.getButtons(button_id)
            return value
        else:
            return False

    def is_changed(self):
        return self.changed
    
    def execute(self):     
        self.hmi_interface.updateButtons()     
        self.hmi_interface.updateAnalogSticks()
        (self.fsL, self.fsR) = self.hmi_interface.getInput()
        print(self.fsL, self.fsR)
        