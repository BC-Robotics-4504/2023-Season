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
                'RS': False,
                'DL': False,
                'DR': False,
                'DU': False,
                'DD': False}


    def updateButtons(self):
        self.buttons['LT'] = True if self.XboxController.getLeftTriggerAxis() > 0.5 else False
        self.buttons['LB'] = self.XboxController.getLeftBumper()
        self.buttons['LS'] = self.XboxController.getLeftStickButton()
        self.buttons['Start'] = self.XboxController.getStartButton()
        self.buttons['Back'] = self.XboxController.getBackButton()
        self.buttons['A'] = self.XboxController.getAButton()
        self.buttons['B'] = self.XboxController.getBButton()
        self.buttons['X'] = self.XboxController.getXButton()
        self.buttons['Y'] = self.XboxController.getYButton()
        self.buttons['RT'] = True if self.XboxController.getRightTriggerAxis() > 0.5 else False
        self.buttons['RB'] = self.XboxController.getRightBumper()
        self.buttons['RS'] = self.XboxController.getRightStickButton()

        # Dpad handler
        self.buttons['DU'] = False
        self.buttons['DD'] = False
        self.buttons['DL'] = False
        self.buttons['DR'] = False
        rawDpad = self.XboxController.getPOV()
        if rawDpad != -1:
            if rawDpad == 0 or rawDpad == 315 or rawDpad == 45: #Dpad up
                self.buttons['DU'] = True
            if rawDpad == 45 or rawDpad == 90 or rawDpad == 135: #Dpad left
                self.buttons['DL'] = True
            if rawDpad == 135 or rawDpad == 180 or rawDpad == 225: #Dpad down
                self.buttons['DD'] = True
            if rawDpad == 225 or rawDpad == 270 or rawDpad == 315: #Dpad right
                self.buttons['DR'] = True

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
        return False

    def is_changed(self):
        return self.changed
    
    def execute(self):     
        self.hmi_interface.updateButtons()     
        self.hmi_interface.updateAnalogSticks()
        (self.fsL, self.fsR) = self.hmi_interface.getInput()
        